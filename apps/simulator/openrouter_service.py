import json
import urllib.request
import urllib.error
import re
from django.conf import settings

# Modelos gratuitos activos verificados en OpenRouter con capacidades de razonamiento
FREE_MODELS = [
    "dots-studio/dots-3-note-preview:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "liquid/lfm-2.5-2.6b:free",
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


def extract_json(raw_text):
    """
    Extrae y repara objetos JSON de respuestas de modelos LLM,
    eliminando bloques de razonamiento (<think>...</think>) y delimitadores markdown.
    """
    if not raw_text:
        return None

    text = raw_text.strip()

    # Remover bloques de razonamiento interno de modelos como Nemotron o DeepSeek
    text = re.sub(r'<think>[\s\S]*?</think>', '', text).strip()

    # Si viene envuelto en markdown ```json ... ```
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()

    # Intento 1: Parseo directo
    try:
        return json.loads(text)
    except Exception:
        pass

    # Intento 2: Buscar el bloque delimitado por llaves { ... }
    match = re.search(r'(\{[\s\S]*\})', text)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass

    # Intento 3: Reparar cierre si fue truncado por longitud
    if "{" in text:
        candidate = text[text.find("{"):]
        if candidate.count('"') % 2 != 0:
            candidate += '"'
        open_braces = candidate.count('{')
        close_braces = candidate.count('}')
        if close_braces < open_braces:
            candidate += '}' * (open_braces - close_braces)
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


def query_openrouter(messages, model=None, timeout=10):
    """
    Envía una petición al endpoint de OpenRouter usando la API Key configurada.
    """
    api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
    if not api_key:
        return None

    target_model = model or getattr(settings, 'OPENROUTER_MODEL', FREE_MODELS[0])
    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": target_model,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 1200,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "DoorPro Canvassing Simulator",
        "User-Agent": "DoorPro-Simulator/1.0"
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                resp_body = response.read().decode('utf-8')
                result = json.loads(resp_body)
                content = result['choices'][0]['message']['content']
                return content
    except urllib.error.HTTPError as e:
        print(f"[OpenRouter] Modelo {target_model} retornó código HTTP {e.code}")
    except Exception as e:
        print(f"[OpenRouter] Error al consultar {target_model}: {e}")

    return None


def generate_llm_response(user_text, door_state):
    """
    Construye el prompt de prospección comercial en puerta y consulta a OpenRouter.
    Si falla o no hay conexión, retorna None para usar el motor local.
    """
    archetype_title = door_state.get('archetype_title', 'Residente')
    archetype_desc = door_state.get('archetype_description', '')
    resident_name = door_state.get('resident_name', 'Residente')
    resident_role = door_state.get('resident_role', 'Dueño de casa')
    patience = door_state.get('patience', 50)
    interest = door_state.get('interest', 20)

    porch_obs = door_state.get('porch_observation', 'En la puerta de su casa observando al asesor.')

    # Historial de conversación
    history_snippets = []
    for msg in door_state.get('messages', []):
        sender = f"Residente ({resident_name})" if msg['sender'] == 'prospect' else "Vendedor en puerta"
        history_snippets.append(f"{sender}: {msg['text']}")

    conversation_history = "\n".join(history_snippets)

    system_prompt = f"""ESTÁS EN EL ROL DE: {resident_name}, {resident_role}.
LUGAR: Estás en tu casa en Texas. Un asesor comercial en puerta de TXU ENERGY acaba de tocar a tu puerta para ofrecerte planes de energía eléctrica (Season Pass 50% descuento en verano/invierno, Free Nights 8PM-6AM, Clear Deal y tarifa protegida).

REGLAS DE IDENTIDAD VITALES:
1. TÚ ERES EL CLIENTE/RESIDENTE ({resident_name}). TÚ NO ERES EL VENDEDOR.
2. NUNCA le llames "{resident_name}" al vendedor; ese es TU nombre. El vendedor es un desconocido.
3. NUNCA OFREZCAS CITAS, NI PROPUESTAS, NI PAQUETES TÚ. Tú solo decides si escuchas, si compras o si cierras la puerta.
4. PERFIL DEL PROSPECTO:
   - Tipo de residente: {archetype_title}
   - Contexto del hogar: {archetype_desc}
   - Lo que el vendedor observa en tu entrada: {porch_obs}
   - Tu Paciencia actual: {patience}%
   - Tu Interés actual: {interest}%

FLEXIBILIDAD Y PERSONALIDAD DEL VENDEDOR:
- Cada vendedor tiene su propio estilo y carisma (humor, calidez, empatía sincera, preguntas abiertas). NO exijas un libreto rígido.
- Si el vendedor es educado, hace una broma sobre el calor o hace preguntas de diagnóstico, responde con apertura humana.
- La paciencia y el interés no disminuyen por saludar o romper el hielo con naturalidad.
- Puedes cerrar ('SALE_CLOSED') o agendar cita ('APPOINTMENT') con cualquier estilo comercial sólido que transmita confianza y ahorro.
- El coach comercial debe evaluar con flexibilidad, premiando el rapport y la autenticidad.
5. CERO EMOJIS: Estrictamente prohibido usar emojis en todo el texto.
6. Tu respuesta hablada ('reply') debe ser corta (1 a 2 oraciones), natural, como alguien hablando desde su puerta.

FORMATO DE SALIDA (ESTRICTAMENTE JSON):
{{
  "reply": "Tu respuesta hablada como {resident_name} en la puerta (sin emojis)",
  "patience_change": entero entre -15 y +15,
  "interest_change": entero entre -15 y +25,
  "coach_critique": "Análisis del coach comercial evaluando la técnica del vendedor (sin emojis)",
  "status": "IN_PROGRESS" | "SALE_CLOSED" | "APPOINTMENT" | "REJECTED",
  "suggestions": [
     "Frase o idea que el vendedor puede decir",
     "Segunda frase o idea que el vendedor puede decir",
     "Tercera frase o idea que el vendedor puede decir"
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
            f"2. En 'coach_critique', evalúa específicamente la efectividad técnica del gancho de apertura inicial (empatía, claridad, gancho de tiempo, impacto en los primeros 15 segundos).\n"
            f"3. En 'suggestions', sugiere 3 alternativas sólidas para continuar la conversación hacia la factura o el sondeo de necesidades.\n"
            f"Responde como {resident_name} en formato JSON estricto."
        )
    else:
        user_prompt = f"HISTORIAL EN LA PUERTA:\n{conversation_history}\n\nEL VENDEDOR EN PUERTA DICE:\n\"{user_text}\"\n\nResponde como {resident_name} (el cliente) en formato JSON estricto."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Modelos gratuitos en orden de prioridad
    active_model = getattr(settings, 'OPENROUTER_MODEL', FREE_MODELS[0])
    models_to_try = [active_model] + [m for m in FREE_MODELS if m != active_model]

    for model_name in models_to_try:
        raw_response = query_openrouter(messages, model=model_name)
        if raw_response:
            data = extract_json(raw_response)
            if data and isinstance(data, dict) and "reply" in data:
                reply = clean_no_emojis(data.get("reply", ""))
                coach = clean_no_emojis(data.get("coach_critique", ""))
                
                # Asegurar que las sugerencias sean frases textuales limpias
                raw_suggestions = data.get("suggestions", [])
                suggestions = []
                for s in raw_suggestions:
                    clean_s = clean_no_emojis(str(s)).strip()
                    if clean_s:
                        # Si venía entrecomillada, limpiar comillas externas
                        clean_s = clean_s.strip('"\'')
                        suggestions.append(clean_s)

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
