import json
import urllib.request
import urllib.error
import re
from django.conf import settings

# Modelos disponibles en Google Gemini con orden de prioridad y tolerancia a picos 503
# Modelos disponibles en Google Gemini con orden de prioridad y tolerancia a picos 503/429
GEMINI_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
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


def query_gemini(system_prompt, user_prompt, timeout=15):
    """
    Envía una petición al endpoint oficial de Google Gemini usando la API Key configurada.
    Itera por los modelos disponibles si alguno presenta alta demanda temporal (códigos 429 o 5xx).
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return None, None

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
            print(f"[Gemini] Código {e.code} en modelo {model}")
            if e.code in (429, 500, 502, 503, 504):
                # Cuota temporal o sobrecarga, probar con el siguiente modelo de la lista
                continue
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

    porch_obs = door_state.get('porch_observation', 'En la puerta de su casa observando al asesor.')

    history_snippets = []
    for msg in door_state.get('messages', []):
        sender = f"Residente ({resident_name})" if msg['sender'] == 'prospect' else "Vendedor en puerta"
        history_snippets.append(f"{sender}: {msg['text']}")

    conversation_history = "\n".join(history_snippets)

    system_prompt = f"""ESTÁS EN EL ROL DE: {resident_name}, {resident_role}.
LUGAR: Estás en tu casa en Texas. Un asesor comercial en puerta de TXU ENERGY (proveedor líder de electricidad en Texas) acaba de tocar a tu puerta en frío para ofrecerte planes de energía (Season Pass 50% de descuento en verano/invierno, Free Nights 8PM-6AM, Clear Deal con crédito en factura o tarifa fija protegida).

REGLAS DE IDENTIDAD VITALES:
1. TÚ ERES EL CLIENTE/RESIDENTE ({resident_name}). TÚ NO ERES EL ASESOR DE TXU.
2. NUNCA le llames "{resident_name}" al vendedor; ese es TU nombre. El vendedor es un desconocido.
3. NUNCA OFREZCAS CITAS, NI PROPUESTAS, NI PAQUETES TÚ. Tú solo decides si escuchas, si muestras tu factura de luz, si aceptas el cambio o si cierras la puerta.
4. PERFIL DEL PROSPECTO:
   - Tipo de residente: {archetype_title}
   - Contexto del hogar: {archetype_desc}
   - Lo que el vendedor observa en tu entrada: {porch_obs}
   - Tu Paciencia actual: {patience}%
   - Tu Interés actual: {interest}%

FLEXIBILIDAD, HUMANIDAD Y PERSONALIDAD DEL VENDEDOR:
- En la prospección real en frío en Texas, cada vendedor tiene su propia personalidad, tono y estilo (humor, empatía genuina, preguntas abiertas, conversación amistosa, técnica consultiva, calidez).
- NO OBLIGUES al vendedor a seguir un guion rígido ni a recitar palabras mágicas obligatorias.
- Si el vendedor es educado, hace una broma sobre el calor, saluda con calidez, pregunta cómo está el vecino, o hace preguntas abiertas inteligentes sobre su servicio de luz: RECONÓCELO Y RESPONDE CON APERTURA HUMANA.
- REGLA CRUCIAL PARA SALUDOS VACÍOS O MONOSÍLABOS:
  * Un simple "hola", "buenas" o saludo aislado de 1 a 3 palabras SIN presentación, SIN decir la empresa (TXU Energy), SIN motivo de visita y SIN gancho comercial NO ES UN GANCHO COMERCIAL.
  * Si el vendedor dice solo "hola", "buenas tardes" o similar sin decir a qué viene: el residente (especialmente si es HOSTIL, OCUPADO o DESCONFIADO) debe reaccionar extrañado, frío o impaciente ("¿Sí? ¿Quién es y qué se le ofrece?", "¿Qué quiere? Voy de salida", o "¿Quién es usted?").
  * En un cliente HOSTIL, un simple "hola" le hace perder el tiempo con el calor de Texas, por lo que su paciencia e interés DEBEN DISMINUIR (-10% a -15% de paciencia). NUNCA elogies ni recompenses un monosílabo seco.
  * El coach comercial ('coach_critique') DEBE corregir al vendedor: señalar que un saludo seco sin identificación corporativa ni motivo de visita genera desconfianza y molestia en puerta fría.
- El cliente puede cerrar la venta ('SALE_CLOSED') o agendar cita ('APPOINTMENT') con cualquier estilo comercial sólido (consultivo, amistoso, directo, enfocado en ahorro) siempre que haya transmitido confianza y abordado la inquietud del prospecto.
- El coach comercial ('coach_critique') debe evaluar con flexibilidad: aplaudir el rapport, la espontaneidad y la empatía, aconsejando mejoras sin forzar a repetir frases prefabricadas.
5. CERO EMOJIS: Estrictamente prohibido usar emojis en todo el texto.
6. Tu respuesta ('reply') se pronuncia en voz alta al vendedor (tipo conversación viva en la puerta). Debe ser corta (1 a 2 oraciones), directa, en lenguaje oral natural y fluido, SIN viñetas, SIN asteriscos, SIN caracteres especiales ni abreviaturas que entorpezcan la lectura de voz.
7. Las 3 sugerencias ('suggestions') deben ser ideas inspiradoras que el asesor de TXU Energy puede decir o adaptar con sus propias palabras.

FORMATO DE SALIDA (ESTRICTAMENTE JSON):
{{
  "reply": "Tu respuesta hablada como {resident_name} en la puerta (sin emojis)",
  "patience_change": entero entre -15 y +15,
  "interest_change": entero entre -15 y +25,
  "coach_critique": "Análisis del coach comercial evaluando la técnica del asesor de energía (sin emojis)",
  "status": "IN_PROGRESS" | "SALE_CLOSED" | "APPOINTMENT" | "REJECTED",
  "suggestions": [
     "Frase o idea que el asesor de TXU puede decir",
     "Segunda frase o idea que el asesor de TXU puede decir",
     "Tercera frase o idea que el asesor de TXU puede decir"
  ]
}}"""

    is_opening_turn = len(door_state.get('messages', [])) == 0
    if is_opening_turn:
        user_prompt = (
            f"SITUACIÓN EN LA PUERTA:\n"
            f"El timbre acaba de sonar en tu casa. Abres la puerta y el asesor comercial de TXU Energy te dice de inmediato como gancho de apertura:\n"
            f"\"{user_text}\"\n\n"
            f"INSTRUCCIONES PARA ESTE PRIMER TURNO:\n"
            f"1. Abre la puerta y reacciona a su gancho de apertura según tu arquetipo ({archetype_title}).\n"
            f"   NOTA VITAL: Si el vendedor dijo únicamente 'hola', 'buenas' o un saludo seco de 1 a 3 palabras sin identificarse ni decir a qué viene, reacciona extrañado o molesto según tu arquetipo, y NO des premios de paciencia ni interés.\n"
            f"2. En 'coach_critique', evalúa específicamente la efectividad técnica del gancho de apertura inicial (empatía, claridad, gancho de tiempo, impacto en los primeros 15 segundos).\n"
            f"3. En 'suggestions', sugiere 3 alternativas sólidas para continuar la conversación hacia la factura o el sondeo de necesidades.\n"
            f"Responde como {resident_name} en formato JSON estricto."
        )
    else:
        user_prompt = (
            f"HISTORIAL EN LA PUERTA:\n{conversation_history}\n\n"
            f"EL VENDEDOR EN PUERTA DICE:\n\"{user_text}\"\n\n"
            f"INSTRUCCIONES PARA ESTE TURNO EN CURSO (NO ES LA APERTURA):\n"
            f"1. La conversación YA ESTÁ EN CURSO. NUNCA saludes de nuevo ('Buenas tardes', 'Hola', etc.) ni preguntes de nuevo quién es o de dónde viene. Responde con naturalidad a lo que acaba de decir el vendedor basándote en el historial.\n"
            f"2. En 'coach_critique', evalúa la técnica del asesor en esta etapa intermedia o de cierre (manejo de objeción, profundización, propuesta de valor, conexión empática o cierre), NUNCA lo trates como gancho de apertura.\n"
            f"3. Responde como {resident_name} en formato JSON estricto."
        )

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
