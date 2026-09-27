import json
import urllib.request
import urllib.error
import re
from django.conf import settings

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


def extract_json(raw_text):
    """Extrae y repara objetos JSON de respuestas LLM."""
    if not raw_text:
        return None
    text = raw_text.strip()
    text = re.sub(r'<think>[\s\S]*?</think>', '', text).strip()

    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r'(\{[\s\S]*\})', text)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass

    return None


def query_deepseek(messages, timeout=10):
    """
    Envía una petición a la API oficial de DeepSeek (https://api.deepseek.com/chat/completions).
    """
    api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
    if not api_key:
        return None

    model = getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat')
    url = "https://api.deepseek.com/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"}
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                resp_body = response.read().decode('utf-8')
                result = json.loads(resp_body)
                return result['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode('utf-8')
        except Exception:
            pass
        if e.code == 402:
            print(f"[DeepSeek] Código 402: Saldo insuficiente en la cuenta de DeepSeek (Insufficient Balance). Activando respaldo.")
        else:
            print(f"[DeepSeek] Error HTTP {e.code}: {error_body}")
    except Exception as e:
        print(f"[DeepSeek] Error de conexión: {e}")

    return None


def generate_deepseek_response(user_text, door_state):
    """
    Genera la respuesta del prospecto y la evaluación del coach usando la API de DeepSeek.
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
LUGAR: Estás en tu casa en Texas. Un asesor comercial en puerta de TXU ENERGY acaba de tocar a tu puerta para ofrecerte planes de energía (Season Pass 50% de descuento en verano/invierno, Free Nights 8PM-6AM, Clear Deal y tarifa protegida).

REGLAS DE IDENTIDAD VITALES:
1. TÚ ERES EL CLIENTE/RESIDENTE ({resident_name}). TÚ NO ERES EL ASESOR DE TXU.
2. NUNCA le llames "{resident_name}" al vendedor; ese es TU nombre.
3. NUNCA OFREZCAS CITAS, NI PROPUESTAS, NI PAQUETES TÚ. Tú solo decides si escuchas, si muestras tu factura de luz, si compras o si cierras la puerta.
4. PERFIL DEL PROSPECTO:
   - Tipo de residente: {archetype_title}
   - Contexto del hogar: {archetype_desc}
   - Observación visible en tu entrada: {porch_obs}
   - Tu Paciencia actual: {patience}%
   - Tu Interés actual: {interest}%

FLEXIBILIDAD Y PERSONALIDAD DEL VENDEDOR:
- Cada vendedor tiene su propio carisma y estilo (humor, empatía genuina, preguntas abiertas, calidez humana). No exijas un libreto rígido.
- Si el vendedor es amable, bromea con el calor o hace preguntas inteligentes, responde con apertura humana.
- La paciencia y el interés no bajan por saludar o romper el hielo. Solo disminuyen por agresividad o falta de respeto.
- Acepta cerrar ('SALE_CLOSED') o agendar cita ('APPOINTMENT') cuando el vendedor genere confianza y aborde tus dudas de consumo.
- El coach debe aplaudir el rapport y la autenticidad personal.
5. CERO EMOJIS: Estrictamente prohibido usar emojis en todo el texto.
6. Tu respuesta hablada ('reply') debe ser corta (1 a 2 oraciones), natural, como alguien hablando desde su puerta.

FORMATO DE SALIDA (ESTRICTAMENTE JSON):
{{
  "reply": "Tu respuesta hablada como {resident_name} en la puerta (sin emojis)",
  "patience_change": entero entre -15 y +15,
  "interest_change": entero entre -15 y +25,
  "coach_critique": "Análisis del coach comercial evaluando la técnica del asesor de energía (sin emojis)",
  "status": "IN_PROGRESS" | "SALE_CLOSED" | "APPOINTMENT" | "REJECTED",
  "suggestions": [
     "Frase o idea que el vendedor puede decir",
     "Segunda frase o idea que el vendedor puede decir",
     "Tercera frase o idea que el vendedor puede decir"
  ]
}}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"HISTORIAL EN LA PUERTA:\n{conversation_history}\n\nEL VENDEDOR EN PUERTA DICE:\n\"{user_text}\"\n\nResponde como {resident_name} (el cliente) en formato JSON estricto."}
    ]

    raw_response = query_deepseek(messages)
    if raw_response:
        data = extract_json(raw_response)
        if data and isinstance(data, dict) and "reply" in data:
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
                "suggestions": suggestions[:3]
            }

    return None
