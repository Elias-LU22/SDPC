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


def generate_gemini_response(user_text, door_state, lang="es"):
    """
    Genera la respuesta del prospecto y la evaluación del coach usando Google Gemini
    en el idioma configurado (Español o Inglés).
    """
    active_lang = (lang or door_state.get('language', 'es')).lower()
    is_english = active_lang.startswith('en')

    archetype_title = door_state.get('archetype_title', 'Resident' if is_english else 'Residente')
    archetype_desc = door_state.get('archetype_description', '')
    resident_name = door_state.get('resident_name', 'Resident' if is_english else 'Residente')
    resident_role = door_state.get('resident_role', 'Homeowner' if is_english else 'Dueño de casa')
    patience = door_state.get('patience', 50)
    interest = door_state.get('interest', 20)

    default_obs = 'At the front door observing the sales advisor.' if is_english else 'En la puerta de su casa observando al asesor.'
    porch_obs = door_state.get('porch_observation', default_obs)

    encounter_type = door_state.get('encounter_type', 'DOOR')
    location_name = door_state.get('location_name', 'Texas')

    history_snippets = []
    for msg in door_state.get('messages', []):
        if is_english:
            sender = f"Customer ({resident_name})" if msg['sender'] == 'prospect' else ("Store Advisor" if encounter_type == 'STORE' else "Door Rep")
        else:
            sender = f"Cliente ({resident_name})" if msg['sender'] == 'prospect' else ("Asesor en tienda" if encounter_type == 'STORE' else "Vendedor en puerta")
        history_snippets.append(f"{sender}: {msg['text']}")

    conversation_history = "\n".join(history_snippets)

    if is_english:
        if encounter_type == 'STORE':
            lugar_context = (
                f"LOCATION: You are at a retail store in Texas ({location_name}). "
                f"You are entering to shop or heading out toward the parking lot with groceries. "
                f"A commercial sales rep from TXU ENERGY (leading Texas electricity provider) at the official store kiosk "
                f"approaches you to offer energy savings (Season Pass 50% discount in summer/winter, Free Nights 8PM-6AM, Clear Deal with bill credits, or store gift cards)."
            )
            observacion_label = f"What the sales rep observes about you: {porch_obs}"
        else:
            lugar_context = (
                f"LOCATION: You are at your home in Texas ({location_name}). "
                f"A door-to-door commercial rep from TXU ENERGY (leading Texas electricity provider) "
                f"just knocked on your door to offer energy advice and plans "
                f"(Season Pass 50% discount in summer/winter, Free Nights 8PM-6AM, Clear Deal bill credits, or protected fixed rates)."
            )
            observacion_label = f"What the sales rep observes at your door: {porch_obs}"

        system_prompt = f"""YOU ARE IN THE ROLE OF: {resident_name}, {resident_role}.
{lugar_context}

CRITICAL IDENTITY RULES:
1. YOU ARE THE CUSTOMER/SHOPPER ({resident_name}). YOU ARE NOT THE TXU REP.
2. NEVER call the sales rep "{resident_name}"; that is YOUR name. The rep is a stranger.
3. NEVER OFFER APPOINTMENTS OR PROPOSALS YOURSELF. You only decide whether to listen, share bill details, switch, or walk away.
4. PROSPECT PROFILE:
   - Archetype: {archetype_title}
   - Context: {archetype_desc}
   - {observacion_label}
   - Current Patience: {patience}%
   - Current Interest: {interest}%

SALES REP HUMANITY, STYLE AND EVALUATION:
- Sales reps have diverse authentic styles (humor, warmth, empathy, diagnostic inquiry, consultative approach).
- DO NOT force the sales rep into an inflexible script.
- If the rep is courteous, acknowledges the Texas heat, asks thoughtful diagnostic questions about your utility bills: ACKNOWLEDGE IT AND ENGAGE POSITIVELY.
- RULE FOR EMPTY BARE GREETINGS:
  * A dry "hello", "hi", or bare 1-to-3 word greeting with NO intro, NO company name (TXU Energy), and NO value hook is NOT a commercial hook.
  * If the rep only says "hi" or "hello": react puzzled, cold, or impatient ("Yes? Who are you?", "What's this about? I'm in a rush").
  * For BUSY or HOSTILE prospects, empty greetings waste time: decrease patience (-10% to -15%).
  * The sales coach ('coach_critique') MUST correct the rep: note that a bare greeting without corporate identity causes instant skepticism.
5. ZERO EMOJIS: Strictly forbidden to use emojis in all text.
6. Spoken reply ('reply') must be concise (1-2 sentences), conversational, natural oral English, WITHOUT markdown, asterisks, or bullet points.
7. The 3 suggestions ('suggestions') must be inspiring sales ideas in English that the TXU rep can say.

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "reply": "Your spoken reply as {resident_name} in conversational English (no emojis)",
  "patience_change": integer between -15 and +15,
  "interest_change": integer between -15 and +25,
  "coach_critique": "Commercial coach critique evaluating the sales technique in professional English (no emojis)",
  "status": "IN_PROGRESS" | "SALE_CLOSED" | "APPOINTMENT" | "REJECTED",
  "suggestions": [
     "First phrase or hook in English",
     "Second phrase or hook in English",
     "Third phrase or hook in English"
  ]
}}"""
    else:
        if encounter_type == 'STORE':
            lugar_context = (
                f"LUGAR: Estás en una gran tienda en Texas ({location_name}). "
                f"Vas entrando a hacer compras o saliendo hacia el estacionamiento con tus compras o víveres. "
                f"Un asesor comercial de TXU ENERGY (proveedor líder de electricidad en Texas) ubicado en el kiosco oficial "
                f"en la entrada/salida de la tienda te aborda directamente para ofrecerte asesoría y planes de energía "
                f"(Season Pass 50% de descuento en verano/invierno, Free Nights 8PM-6AM, Clear Deal o tarjetas de regalo de tienda)."
            )
            observacion_label = f"Lo que el asesor observa de ti en la tienda: {porch_obs}"
        else:
            lugar_context = (
                f"LUGAR: Estás en tu casa en Texas ({location_name}). "
                f"Un asesor comercial en puerta de TXU ENERGY (proveedor líder de electricidad en Texas) "
                f"acaba de tocar a tu puerta directamente para ofrecerte asesoría y planes de energía "
                f"(Season Pass 50% de descuento en verano/invierno, Free Nights 8PM-6AM, Clear Deal con crédito en factura o tarifa fija protegida)."
            )
            observacion_label = f"Lo que el vendedor observa en tu entrada: {porch_obs}"

        system_prompt = f"""ESTÁS EN EL ROL DE: {resident_name}, {resident_role}.
{lugar_context}

REGLAS DE IDENTIDAD VITALES:
1. TÚ ERES EL CLIENTE/COMPRADOR ({resident_name}). TÚ NO ERES EL ASESOR DE TXU.
2. NUNCA le llames "{resident_name}" al vendedor; ese es TU nombre. El vendedor es un desconocido.
3. NUNCA OFREZCAS CITAS, NI PROPUESTAS, NI PAQUETES TÚ. Tú solo decides si escuchas, si muestras tu factura de luz, si aceptas el cambio o si continúas tu camino.
4. PERFIL DEL PROSPECTO:
   - Tipo de perfil: {archetype_title}
   - Contexto: {archetype_desc}
   - {observacion_label}
   - Tu Paciencia actual: {patience}%
   - Tu Interés actual: {interest}%

FLEXIBILIDAD, HUMANIDAD Y PERSONALIDAD DEL VENDEDOR:
- En la asesoría y venta directa en Texas (tanto en puerta residencial como en kiosco de tienda), cada vendedor tiene su propia personalidad, tono y estilo (humor, empatía genuina, preguntas abiertas, conversación amistosa, técnica consultiva, calidez).
- NO OBLIGUES al vendedor a seguir un guion rígido ni a recitar palabras mágicas obligatorias.
- Si el vendedor es educado, hace una broma sobre el calor, saluda con calidez, pregunta cómo está el cliente, o hace preguntas abiertas inteligentes sobre su servicio de luz: RECONÓCELO Y RESPONDE CON APERTURA HUMANA.
- REGLA CRUCIAL PARA SALUDOS VACÍOS O MONOSÍLABOS:
  * Un simple "hola", "buenas" o saludo aislado de 1 a 3 palabras SIN presentación, SIN decir la empresa (TXU Energy), SIN motivo de visita y SIN gancho comercial NO ES UN GANCHO COMERCIAL.
  * Si el vendedor dice solo "hola", "buenas tardes" o similar sin decir a qué viene: el prospecto (especialmente si es HOSTIL, OCUPADO o DESCONFIADO) debe reaccionar extrañado, frío o impaciente ("¿Sí? ¿Quién es y qué se le ofrece?", "¿Qué quiere? Voy de salida", o "¿Quién es usted?").
  * En un cliente HOSTIL u OCUPADO, un simple "hola" le hace perder el tiempo o se le derrite el hielo del súper, por lo que su paciencia e interés DEBEN DISMINUIR (-10% a -15% de paciencia). NUNCA elogies ni recompenses un monosílabo seco.
  * El coach comercial ('coach_critique') DEBE corregir al vendedor: señalar que un saludo seco sin identificación corporativa ni motivo de visita genera desconfianza y molestia.
5. CERO EMOJIS: Estrictamente prohibido usar emojis en todo el texto.
6. Tu respuesta ('reply') se pronuncia en voz alta al vendedor (tipo conversación viva). Debe ser corta (1 a 2 oraciones), directa, en lenguaje oral natural y fluido, SIN viñetas, SIN asteriscos, SIN caracteres especiales ni abreviaturas que entorpezcan la lectura de voz.
7. Las 3 sugerencias ('suggestions') deben ser ideas inspiradoras que el asesor de TXU Energy puede decir o adaptar con sus propias palabras.

FORMATO DE SALIDA (ESTRICTAMENTE JSON):
{{
  "reply": "Tu respuesta hablada como {resident_name} (sin emojis)",
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
        if is_english:
            if encounter_type == 'STORE':
                user_prompt = (
                    f"STORE ENCOUNTER:\n"
                    f"You are passing the entrance/exit of {location_name} and the TXU Energy rep at the kiosk approaches you saying as an opening hook:\n"
                    f"\"{user_text}\"\n\n"
                    f"INSTRUCTIONS FOR FIRST TURN:\n"
                    f"1. React to the hook according to your archetype ({archetype_title}) and store situation.\n"
                    f"   VITAL NOTE: If the rep said only 'hi', 'hello' or a bare 1-3 word greeting without identifying themselves, react annoyed or puzzled, and DO NOT reward patience or interest.\n"
                    f"2. In 'coach_critique', evaluate the approach hook effectiveness (impact in first 10 seconds, not blocking path, savings benefit or gift card).\n"
                    f"3. In 'suggestions', provide 3 solid English alternatives to steer conversation toward bill comparison.\n"
                    f"Respond as {resident_name} in strict JSON format."
                )
            else:
                user_prompt = (
                    f"DOORBELL ENCOUNTER:\n"
                    f"The doorbell just rang at your home. You open the door and the TXU Energy advisor says as an opening hook:\n"
                    f"\"{user_text}\"\n\n"
                    f"INSTRUCTIONS FOR FIRST TURN:\n"
                    f"1. Open the door and react according to your archetype ({archetype_title}).\n"
                    f"   VITAL NOTE: If the rep said only 'hi', 'hello' or a bare greeting without identifying themselves, react guarded or impatient, and DO NOT reward patience or interest.\n"
                    f"2. In 'coach_critique', evaluate opening hook effectiveness (empathy, clarity, 15-second frame, impact in Texas heat).\n"
                    f"3. In 'suggestions', provide 3 solid English alternatives to advance to a bill comparison.\n"
                    f"Respond as {resident_name} in strict JSON format."
                )
        else:
            if encounter_type == 'STORE':
                user_prompt = (
                    f"SITUACIÓN EN LA TIENDA:\n"
                    f"Vas pasando por la entrada o salida de {location_name} y el asesor comercial de TXU Energy en el kiosco te aborda de inmediato diciendo como gancho de apertura:\n"
                    f"\"{user_text}\"\n\n"
                    f"INSTRUCCIONES PARA ESTE PRIMER TURNO:\n"
                    f"1. Reacciona a su gancho de abordaje según tu arquetipo ({archetype_title}) y contexto en la tienda.\n"
                    f"   NOTA VITAL: Si el vendedor dijo únicamente 'hola', 'buenas' o un saludo seco de 1 a 3 palabras sin identificarse ni decir a qué viene, reacciona extrañado o molesto según tu arquetipo, y NO des premios de paciencia ni interés.\n"
                    f"2. En 'coach_critique', evalúa específicamente la efectividad técnica del gancho de abordaje en tienda (impacto en los primeros 10 segundos, no estorbar el paso, beneficio de ahorro o tarjeta de regalo).\n"
                    f"3. En 'suggestions', sugiere 3 alternativas sólidas para continuar la conversación hacia la factura o el sondeo de necesidades.\n"
                    f"Responde como {resident_name} en formato JSON estricto."
                )
            else:
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
        if is_english:
            user_prompt = (
                f"CONVERSATION HISTORY:\n{conversation_history}\n\n"
                f"THE SALES ADVISOR SAYS:\n\"{user_text}\"\n\n"
                f"INSTRUCTIONS FOR ONGOING TURN:\n"
                f"1. The conversation IS ALREADY UNDERWAY. NEVER greet again ('Hello', 'Good afternoon', etc.) nor ask who they are. Respond naturally to what the rep just said based on history.\n"
                f"2. In 'coach_critique', evaluate the advisor's technique at this ongoing stage (objection handling, value proposition, rapport, or closing), NEVER treat it as an opening hook.\n"
                f"3. Respond as {resident_name} in strict JSON format."
            )
        else:
            user_prompt = (
                f"HISTORIAL DE LA CONVERSACIÓN:\n{conversation_history}\n\n"
                f"EL ASESOR COMERCIAL DICE:\n\"{user_text}\"\n\n"
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
