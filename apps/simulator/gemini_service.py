import json
import urllib.request
import urllib.error
import re
from django.conf import settings

# Modelos disponibles en Google Gemini con orden de prioridad y tolerancia a picos 503
GEMINI_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
]


def clean_no_emojis(text):
    """Elimina cualquier emoji para cumplir estrictamente con el diseño sin emojis."""
    if not text:
        return text
    emoji_pattern = re.compile(
        "["
        "\U00010000-\U0010ffff"
        "\u2600-\u27bf"
        "\u2300-\u23ff"
        "\u2b50"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub("", text).strip()


def query_gemini(system_prompt, user_prompt, timeout=8):
    """
    Envía una petición al endpoint oficial de Google Gemini usando la API Key configurada.
    Itera por los modelos disponibles si alguno presenta alta demanda temporal (código 503).
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return None

    configured_model = getattr(settings, 'GEMINI_MODEL', GEMINI_MODELS[0])
    models_to_try = [configured_model] + [m for m in GEMINI_MODELS if m != configured_model]

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.6,
            "responseMimeType": "application/json",
            "maxOutputTokens": 1200
        }
    }

    data = json.dumps(payload).encode('utf-8')

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    resp_body = response.read().decode('utf-8')
                    result = json.loads(resp_body)
                    candidates = result.get('candidates', [])
                    if candidates:
                        content_parts = candidates[0].get('content', {}).get('parts', [])
                        if content_parts:
                            return content_parts[0].get('text', ''), model
        except urllib.error.HTTPError as e:
            if e.code == 503:
                # Pico temporal de demanda en este modelo, probar siguiente
                continue
            else:
                print(f"[Gemini] Código {e.code} en modelo {model}")
        except Exception as e:
            print(f"[Gemini] Error en {model}: {e}")

    return None, None


def generate_gemini_response(user_text, door_state):
    """
    Genera la respuesta del prospecto y la evaluación del coach usando Google Gemini.
    """
    archetype_title = door_state.get('archetype_title', 'Residente')
    archetype_desc = door_state.get('archetype_description', '')
    resident_name = door_state.get('resident_name', 'Residente')
    resident_role = door_state.get('resident_role', 'Dueño de casa')
    patience = door_state.get('patience', 50)
    interest = door_state.get('interest', 20)

    history_snippets = []
    for msg in door_state.get('messages', []):
        sender = f"Residente ({resident_name})" if msg['sender'] == 'prospect' else "Vendedor en puerta"
        history_snippets.append(f"{sender}: {msg['text']}")

    conversation_history = "\n".join(history_snippets)

    system_prompt = f"""ESTÁS EN EL ROL DE: {resident_name}, {resident_role}.
LUGAR: Estás adentro de tu casa en Texas. Un asesor comercial en puerta de TXU ENERGY (proveedor líder de electricidad residencial) acaba de tocar a tu puerta en frío para ofrecerte planes de energía (Season Pass 50% descuento en verano/invierno, Free Nights 8PM-6AM, Clear Deal con crédito en factura y tarifa fija protegida).

REGLAS DE IDENTIDAD VITALES (NO CONFUNDIR ROLES):
1. TÚ ERES EL CLIENTE/RESIDENTE ({resident_name}). TÚ NO ERES EL ASESOR DE TXU.
2. NUNCA le llames "{resident_name}" al vendedor; ese es TU nombre. El vendedor es un desconocido.
3. NUNCA OFREZCAS CITAS, NI PROPUESTAS, NI PAQUETES TÚ. Tú solo decides si escuchas, si muestras tu factura de luz, si aceptas el cambio o si cierras la puerta.
4. PERSONALIDAD: {archetype_title} ({archetype_desc}).
   - Tu Paciencia actual: {patience}%
   - Tu Interés actual: {interest}%
   - Si eres 'El Ocupado': tienes prisa, vas de salida; rechazas discursos largos; aceptas ganchos de 15 segundos sobre el 50% de descuento en verano o una cita breve en la tarde.
   - Si eres 'El Desconfiado': temes al 'slamming' (cambio no autorizado de proveedor con tu recibo); exiges gafete oficial de TXU Energy; te abres si respetan tu precaución, no exigen el recibo de golpe y citan a tus vecinos.
   - Si eres 'El Amable Evasivo': intentas despedirte pidiendo un folleto; si te hacen una buena pregunta sobre tu recibo alto por el aire acondicionado o consumo en kWh, confiesas el problema.
   - Si eres 'El Hostil': estás enojado por el calor o harto de interrupciones; solo te calmas si el vendedor se disculpa con empatía sincera y respeto absoluto. Si te dice 'cálmese', te enfadas más.
   - Si eres 'El Prospecto Calificado': tu compañía de luz actual te cobró una factura exorbitante en verano por tarifa variable; estás listo para cambiarte a TXU Season Pass si te congelan la tarifa por 24 meses y te dan el 50% de descuento.
   - Si eres 'El Cazador de Descuentos': buscas centavos por kWh netos en la etiqueta EFL; exiges claridad en cargos de Oncor y créditos en factura (como el crédito de $30 de Clear Deal).
   - Si eres 'El No Decide (Familiar)': no eres el titular de la cuenta ante ERCOT; si insisten en venderte a ti te aburres, pero facilitas el horario del titular si te lo piden amablemente.
   - Si eres 'El Casado con la Competencia': llevas años con Reliant u otra empresa por inercia; temes quedarte sin luz; te convence que Oncor sigue entregando los cables, no hay cortes y TXU ofrece 60 días de garantía sin penalización.
   - Si eres 'El Propietario con Auto Eléctrico (EV)': tienes vehículo eléctrico o casa inteligente; te convence el plan Free Nights & Solar Days (8:00 PM a 6:00 AM electricidad gratis a costo cero para recarga y aire acondicionado nocturno).
5. CERO EMOJIS: Estrictamente prohibido usar emojis en todo el texto.
6. Tu respuesta hablada ('reply') debe ser corta (1 a 2 oraciones), natural, como alguien hablando desde su puerta en Texas.
7. El coach comercial ('coach_critique') debe evaluar la técnica del asesor de energía (manejo del recibo, explicación de planes de TXU, desescalada y cierre asertivo).
8. Las 3 sugerencias ('suggestions') deben ser frases textuales que un asesor de TXU Energy puede decir en primera persona en ese instante.

FORMATO DE SALIDA (ESTRICTAMENTE JSON):
{{
  "reply": "Tu respuesta hablada como {resident_name} en la puerta (sin emojis)",
  "patience_change": entero entre -20 y +15,
  "interest_change": entero entre -20 y +25,
  "coach_critique": "Análisis del coach comercial evaluando la técnica del asesor de energía (sin emojis)",
  "status": "IN_PROGRESS" | "SALE_CLOSED" | "APPOINTMENT" | "REJECTED",
  "suggestions": [
     "Frase textual que el asesor de TXU puede decir",
     "Segunda frase textual que el asesor de TXU puede decir",
     "Tercera frase textual que el asesor de TXU puede decir"
  ]
}}"""

    user_prompt = f"HISTORIAL EN LA PUERTA:\n{conversation_history}\n\nEL VENDEDOR EN PUERTA DICE:\n\"{user_text}\"\n\nResponde como {resident_name} (el cliente) en formato JSON estricto."

    raw_response, model_used = query_gemini(system_prompt, user_prompt)
    if raw_response:
        try:
            data = json.loads(raw_response)
            if isinstance(data, dict) and "reply" in data:
                reply = clean_no_emojis(data.get("reply", ""))
                coach = clean_no_emojis(data.get("coach_critique", ""))
                
                raw_suggestions = data.get("suggestions", [])
                suggestions = [clean_no_emojis(str(s)).strip().strip('"\'') for s in raw_suggestions if s]

                patience_change = int(data.get("patience_change", 0))
                interest_change = int(data.get("interest_change", 0))
                status = data.get("status", "IN_PROGRESS")
                if status not in ["IN_PROGRESS", "SALE_CLOSED", "APPOINTMENT", "REJECTED"]:
                    status = "IN_PROGRESS"

                return {
                    "reply": reply,
                    "patience_change": patience_change,
                    "interest_change": interest_change,
                    "coach": coach,
                    "status": status,
                    "suggestions": suggestions[:3],
                    "engine": f"Google Gemini ({model_used})"
                }
        except Exception as parse_err:
            print(f"[Gemini] Error al parsear JSON: {parse_err}")

    return None
