import random
import re

RESIDENTS = [
    {"name": "Fernando López", "role": "Propietario / Casa 2 pisos en Dallas", "archetype": "BUSY", "gender": "M"},
    {"name": "Carmen Morales", "role": "Ama de casa / Familia en Houston", "archetype": "POLITE_EVASIVE", "gender": "F"},
    {"name": "Roberto Garza", "role": "Ingeniero / Residente en Frisco", "archetype": "SKEPTICAL", "gender": "M"},
    {"name": "Patricia Ortiz", "role": "Dueña de negocio / Casa en Fort Worth", "archetype": "HOSTILE", "gender": "F"},
    {"name": "Javier Treviño", "role": "Profesionista / Recibo de $380 en verano", "archetype": "IDEAL_LEAD", "gender": "M"},
    {"name": "Ricardo Fuentes", "role": "Contador / Compara centavos por kWh", "archetype": "BARGAIN_HUNTER", "gender": "M"},
    {"name": "Andrea Salazar", "role": "Inquilina en Plano / Vive en pareja", "archetype": "NON_DECISION_MAKER", "gender": "F"},
    {"name": "Gonzalo Villagrán", "role": "Jubilado / 12 años con Reliant Energy", "archetype": "LOYALIST", "gender": "M"},
    {"name": "Mauricio Alatorre", "role": "Dueño de Tesla / Carga nocturna", "archetype": "TECH_SAVVY", "gender": "M"},
    {"name": "Beatriz Luna", "role": "Residente en Arlington / Teme al slamming", "archetype": "SKEPTICAL", "gender": "F"},
    {"name": "Carlos Méndez", "role": "Empresario / Alto consumo de aire acondicionado", "archetype": "BUSY", "gender": "M"},
    {"name": "Elena Ramos", "role": "Jubilada / Presupuesto fijo en Garland", "archetype": "POLITE_EVASIVE", "gender": "F"},
    {"name": "Gabriel Domínguez", "role": "Ingeniero TI / Casa inteligente en Irving", "archetype": "TECH_SAVVY", "gender": "M"},
    {"name": "Valeria Ríos", "role": "Estudiante universitaria / Renta cuarto", "archetype": "NON_DECISION_MAKER", "gender": "F"},
    {"name": "Armando Cárdenas", "role": "Administrador / Busca crédito en factura", "archetype": "BARGAIN_HUNTER", "gender": "M"},
    {"name": "Esteban Navarro", "role": "Propietario en Mesquite / Fiel a Direct Energy", "archetype": "LOYALIST", "gender": "M"},
]

ARCHETYPE_DETAILS = {
    "BUSY": {
        "title": "El Ocupado (Prisa con el A/C)",
        "description": "Tiene prisa evidente y va de salida. Valora la brevedad, empatía y respetar su tiempo.",
        "porch_observation": "Llaves del auto en mano, portafolio y mirada atenta al reloj.",
        "initial_patience": 55,
        "initial_interest": 20,
        "initial_message": "Dígame rápido por favor, voy de salida al trabajo. Con este calor de Texas nadie quiere estar en la puerta. ¿Qué se le ofrece?",
        "opening_hooks": [
            "Buenas tardes vecino, disculpe la interrupción rápida: solo le robo 15 segundos antes de que salga para comentarle del 50% de descuento en verano de TXU.",
            "Hola, buenas tardes. Sé que va con prisa, solo una pregunta rápida: ¿a qué hora le encuentro en la tarde para revisar su recibo de luz en 2 minutos?",
            "Buenas tardes, vecino. Noté los aires acondicionados encendidos a todo lo que dan; con este calor de Texas queríamos avisarle del programa de ahorro de TXU."
        ],
        "suggestions": [
            "Solo 15 segundos mientras sale: con este calor el aire acondicionado dispara las facturas. TXU le da 50% de descuento en verano con Season Pass. ¿Cuánto pagó el mes pasado?",
            "Sé que va con prisa. ¿A qué hora le encuentro en la tarde para mostrarle el comparativo de su recibo en 2 minutos?",
            "Vengo a explicarle la historia de la desregulación eléctrica de Texas y todas las opciones de kilovatios."
        ]
    },
    "SKEPTICAL": {
        "title": "El Desconfiado (Teme al Slamming)",
        "description": "Teme estafas y el cambio no autorizado de proveedor (slamming). Se abre si validan su precaución y muestran gafete oficial.",
        "porch_observation": "Entreabre la puerta con la cadena puesta; observa con cautela a través de la mirilla.",
        "initial_patience": 60,
        "initial_interest": 15,
        "initial_message": "¿Quién es usted? No le muestro mi recibo de luz a nadie en la puerta, andan muchos estafadores cambiando contratos sin permiso.",
        "opening_hooks": [
            "Buenas tardes vecino, mi nombre es asesor oficial de TXU Energy, mire mi gafete. Sé que hay mucha precaución con los estafadores en Texas, no vengo a pedirle datos personales.",
            "Hola vecino, disculpe la molestia. Antes que nada, le muestro mi identificación oficial; solo estamos validando si sus vecinos ya congelaron su tarifa contra los picos de verano.",
            "Buenas tardes. Como vecino prevenido hace muy bien en verificar quién toca su puerta; venimos directamente de TXU Energy con tarifas fijas protegidas."
        ],
        "suggestions": [
            "Tiene toda la razón y hace bien en protegerse; nunca muestre su número ESI ID a extraños. Soy asesor oficial de TXU Energy, mire mi gafete. No le pido su recibo hoy, solo una pregunta: ¿su tarifa actual es fija o variable?",
            "Soy representante oficial de la empresa, mire mi credencial, no tiene nada de qué desconfiar.",
            "A sus vecinos de la casa de al lado les ayudamos a bloquear su tarifa en centavos fijos para protegerse de los picos de verano."
        ]
    },
    "POLITE_EVASIVE": {
        "title": "El Amable Evasivo",
        "description": "Amable y sonriente, busca despedirse pidiendo un folleto. Valora preguntas de diagnóstico sobre su consumo en verano.",
        "porch_observation": "Sonrisa amable pero cuerpo orientado hacia el interior de la casa.",
        "initial_patience": 70,
        "initial_interest": 20,
        "initial_message": "Buenas tardes joven. Se ve interesante lo que trae de TXU, pero ando ocupada. ¿Por qué no me deja su folleto y si me interesa yo les hablo?",
        "opening_hooks": [
            "Buenas tardes vecina, disculpe que la interrumpa un momento. Estamos pasando con los vecinos de la cuadra para revisar el impacto del aire acondicionado en el recibo de luz.",
            "Hola vecina, qué gusto saludarla. Rápido, antes de dejarle cualquier información en papel: ¿su factura suele superar los $200 dólares en los meses de calor?",
            "Buenas tardes, solo una consulta breve de 30 segundos sobre el subsidio de verano de TXU Energy para los hogares de esta calle."
        ],
        "suggestions": [
            "Con mucho gusto se lo dejo. Solo para saber cuál dejarle: ¿su factura de luz suele superar los $250 dólares en julio y agosto?",
            "Claro que sí, tenga el volante. Ahí viene el teléfono de TXU Energy para cuando guste marcar.",
            "No puedo dejar folletos por política de la empresa, necesito que me escuche ahora mismo."
        ]
    },
    "HOSTILE": {
        "title": "El Hostil",
        "description": "Irritable y a la defensiva por el calor o vendedores ambulantes. Se desarma con respeto genuino, disculpas sinceras y empatía.",
        "porch_observation": "Expresión tensa y sudor en la frente por el calor; sostiene la puerta con firmeza.",
        "initial_patience": 35,
        "initial_interest": 10,
        "initial_message": "¡Otra vez tocando la puerta! Con 100 grados de calor afuera lo último que quiero es que vengan a molestar con la luz. ¡No me interesa nada!",
        "opening_hooks": [
            "Buenas tardes señor, una disculpa sincera por tocar a su puerta con este calor de 100 grados. Solo quería dejarle un saludo respetuoso de TXU Energy.",
            "Hola, buenas tardes. Sé que es molesto que toquen la puerta a esta hora; prometo ser extremadamente breve si me permite solo 20 segundos.",
            "Buenas tardes vecino, disculpe la interrupción en su descanso. Me retiro de inmediato si está ocupado, solo pasábamos a verificar el servicio en la cuadra."
        ],
        "suggestions": [
            "Tiene toda la razón señor, una disculpa sincera por interrumpirlo. Con este calor nadie quiere que le toquen la puerta. Me retiro de inmediato, que pase buena tarde.",
            "Cálmese señor, no se enoje por nada, solo le vengo a ofrecer una tarifa de TXU que le va a convenir.",
            "La banqueta es pública y solo estoy haciendo mi trabajo con TXU Energy."
        ]
    },
    "IDEAL_LEAD": {
        "title": "El Prospecto Calificado (Recibo Disparado)",
        "description": "Su contrato anterior venció y la tarifa variable disparó su recibo; busca alivio y tarifa fija de inmediato.",
        "porch_observation": "Sobre de correspondencia abierto en la mano con el recibo de electricidad visible.",
        "initial_patience": 70,
        "initial_interest": 50,
        "initial_message": "Buenas tardes. Qué bueno que pasa de TXU. El mes pasado mi compañía me cobró casi $400 dólares por el puro aire acondicionado. Esto es un abuso y quiero cambiarme ya.",
        "opening_hooks": [
            "Buenas tardes vecino, venimos de TXU Energy. Varios vecinos de la calle nos comentaron que el recibo de luz se les disparó a más de $350 este verano, ¿a ustedes también les afectó?",
            "Hola, buenas tardes. Estamos ayudando a las familias de la colonia cuyos contratos vencieron para blindar su tarifa con el 50% de descuento de Season Pass.",
            "Buenas tardes vecino, disculpe la molestia. ¿Ha notado cobros excesivos por el aire acondicionado en su última factura de electricidad?"
        ],
        "suggestions": [
            "Le entiendo perfecto, muchos vecinos sufrieron ese golpe porque su contrato venció y entraron a tarifa variable. Con TXU Season Pass le damos 50% de descuento en verano y tarifa protegida. ¿Tiene su factura a mano para calcular su ahorro?",
            "Tenemos paquetes con muchas tarifas, opciones solares, planes nocturnos y términos variables...",
            "Si le garantizamos bloquear su precio por 24 meses y reducir su factura de verano a la mitad, ¿hacemos el registro hoy mismo sin cortes?"
        ]
    },
    "BARGAIN_HUNTER": {
        "title": "El Cazador de Descuentos (Centavos por kWh)",
        "description": "Compara centavos por kWh y créditos en factura; premia transparencia en números y cargos de distribución.",
        "porch_observation": "Celular en mano con la calculadora abierta o revisando facturas anteriores.",
        "initial_patience": 60,
        "initial_interest": 40,
        "initial_message": "A ver joven de TXU, ¿a cuántos centavos el kWh viene el plan? Pero dígame el promedio real a 1,000 kWh en la etiqueta EFL, no me disfrace los cargos de Oncor.",
        "opening_hooks": [
            "Buenas tardes vecino, asesor oficial de TXU Energy. Estamos comparando tarifas en centavos por kWh con total transparencia de la etiqueta EFL para esta zona.",
            "Hola, buenas tardes. Si revisamos su consumo promedio a 1,000 kWh, podemos mostrarle cómo el crédito de $30 de Clear Deal reduce su costo por kWh.",
            "Buenas tardes. Venimos desglosando los cargos reales de energía frente a los cargos de Oncor para encontrar el precio por kilovatio más bajo."
        ],
        "suggestions": [
            "En el plan Clear Deal el promedio a 1,000 kWh queda en 12.8 centavos con el crédito automático de $30 dólares de TXU incluido, todo desglosado en la EFL. ¿Cuánto le cobran hoy?",
            "Depende de cuánto consuma cada mes, las tarifas de electricidad van variando en Texas según el clima.",
            "Con nosotros se ahorra una fortuna garantizada, somos la compañía de luz más barata de Texas."
        ]
    },
    "NON_DECISION_MAKER": {
        "title": "El No Decide (Familiar)",
        "description": "Familiar o inquilino en la vivienda; no es titular del contrato ante ERCOT pero puede facilitar el contacto.",
        "porch_observation": "Se asoma con curiosidad informal; viste ropa de estar en casa.",
        "initial_patience": 65,
        "initial_interest": 30,
        "initial_message": "Buenas tardes. Sí nos llega caro el recibo de la luz, pero de eso se encarga mi pareja. Yo aquí no tomo decisiones de contratos.",
        "opening_hooks": [
            "Buenas tardes, disculpe la molestia. Vengo de TXU Energy con información importante sobre el ahorro de verano en la electricidad para los propietarios del hogar.",
            "Hola, buenas tardes. ¿Se encontrará el titular de la casa o la persona encargada de ver las facturas de luz para entregarle un comparativo breve?",
            "Buenas tardes vecina. Estamos compartiendo las nuevas tarifas de energía fija para la colonia, ¿a qué hora suele estar quien revisa los contratos del hogar?"
        ],
        "suggestions": [
            "Comprendo totalmente. ¿A qué hora llega su pareja para pasar 3 minutos y entregarle la comparativa de ahorro de verano directamente?",
            "No se preocupe, fírmeme usted y ya luego le avisa cuando llegue el cambio de TXU en su recibo.",
            "¿Me permitiría dejarle una nota breve con el comparativo de TXU Season Pass para que lo platiquen en la noche?"
        ]
    },
    "LOYALIST": {
        "title": "El Casado con la Competencia (Reliant / Direct Energy)",
        "description": "Lleva años con su compañía por inercia; se convence al saber que Oncor mantiene los cables y no hay cortes.",
        "porch_observation": "Residente en su porche descansando, cómodo con su rutina diaria.",
        "initial_patience": 60,
        "initial_interest": 15,
        "initial_message": "Llevo más de 10 años con Reliant y no me gusta andar cambiando de compañía. Aunque paguemos bastante, ya los conozco y no quiero problemas.",
        "opening_hooks": [
            "Buenas tardes vecino, represento a TXU Energy. Estamos informando a los vecinos de la cuadra que Oncor mantiene los mismos postes pero con tarifas más económicas.",
            "Hola, buenas tardes. Muchos vecinos que llevaban años con Reliant se sorprendieron al ver cuánto podían ahorrar cambiando a TXU sin cortes de luz.",
            "Buenas tardes. Respetamos mucho a quienes tienen contratos de años con su compañía; solo venimos a validar si le han actualizado su precio este año."
        ],
        "suggestions": [
            "Es muy respetable su lealtad, Reliant es una empresa conocida. Pero en Texas, Oncor sigue siendo quien entrega la energía física; no hay corte ni por un segundo. Solo por curiosidad: ¿hace cuánto que no le revisan la tarifa para bajarle el costo?",
            "Reliant es carísima y se aprovechan de los clientes viejos que no se fijan en el recibo.",
            "TXU le ofrece 60 días de garantía total: si no ve el ahorro en su primer recibo, puede cambiar de plan sin penalización."
        ]
    },
    "TECH_SAVVY": {
        "title": "El Propietario con Auto Eléctrico (EV) / Casa Inteligente",
        "description": "Tiene vehículo eléctrico o termostato inteligente; busca el plan Free Nights & Solar Days.",
        "porch_observation": "Estación de carga de auto eléctrico en la cochera y timbre inteligente con cámara.",
        "initial_patience": 55,
        "initial_interest": 45,
        "initial_message": "¿TXU maneja el plan de Noches Gratis (Free Nights)? Acabamos de comprar un auto eléctrico y tenemos termostato inteligente, me interesa cargar el carro a costo cero.",
        "opening_hooks": [
            "Buenas tardes vecino. Noté su auto eléctrico en la cochera, ¿ya conoce el plan Free Nights de TXU Energy para cargarlo a costo cero de 8 PM a 6 AM?",
            "Hola, buenas tardes. Vengo de TXU Energy; estamos activando planes especiales para casas inteligentes con termostatos conectados y vehículos eléctricos.",
            "Buenas tardes. Para hogares con alto consumo nocturno y tecnología conectada, tenemos electricidad 100% gratuita por contrato durante las noches."
        ],
        "suggestions": [
            "Exactamente, con Free Nights & Solar Days toda la electricidad de 8:00 PM a 6:00 AM es 100% gratuita. Puede cargar su auto eléctrico y enfriar su casa toda la noche sin pagar un centavo de energía. ¿A qué hora suele enchufar su vehículo?",
            "Sí tenemos ese plan, pero le conviene más el paquete estándar para toda la casa que usan todos los clientes.",
            "De día la energía es 100% solar y de noche es gratis por contrato. ¿Revisamos su consumo mensual para confirmar si es el plan óptimo para su perfil?"
        ]
    }
}


def create_new_door(exclude_name=None, exclude_archetype=None, visited_names=None, current_door_num=None):
    """
    Genera un nuevo prospecto garantizando variedad en residentes y arquetipos,
    evitando repetir el mismo prospecto o el mismo tema inmediatamente.
    Inicia en la puerta sin mensajes previos, requiriendo tocar el timbre.
    """
    if visited_names is None:
        visited_names = []

    # 1. Filtrar prospectos no visitados en la rotación actual
    unvisited = [r for r in RESIDENTS if r["name"] not in visited_names and r["name"] != exclude_name]

    # Si ya se recorrieron todos los residentes, reiniciar ciclo excluyendo únicamente el actual
    if not unvisited:
        unvisited = [r for r in RESIDENTS if r["name"] != exclude_name]
        if not unvisited:
            unvisited = list(RESIDENTS)

    # 2. Priorizar un arquetipo diferente al de la puerta anterior
    different_archetype = [r for r in unvisited if r["archetype"] != exclude_archetype]
    candidates = different_archetype if different_archetype else unvisited

    resident = random.choice(candidates)
    archetype_key = resident["archetype"]
    archetype_data = ARCHETYPE_DETAILS[archetype_key]

    # Número de puerta realista y secuencial en la misma calle residencial
    if current_door_num and isinstance(current_door_num, int) and 100 <= current_door_num <= 890:
        door_num = current_door_num + random.choice([2, 4, 6])
    else:
        door_num = random.choice([102, 104, 106, 108, 110, 114, 116])

    return {
        "door_number": door_num,
        "resident_name": resident["name"],
        "resident_role": resident["role"],
        "resident_gender": resident.get("gender", "M"),
        "archetype": archetype_key,
        "archetype_title": archetype_data["title"],
        "archetype_description": archetype_data["description"],
        "porch_observation": archetype_data.get("porch_observation", "En su puerta residencial observando al asesor."),
        "patience": archetype_data["initial_patience"],
        "interest": archetype_data["initial_interest"],
        "status": "IN_PROGRESS",  # IN_PROGRESS, SALE_CLOSED, APPOINTMENT, REJECTED
        "turn": 0,
        "doorbell_rung": False,
        "messages": [],
        "suggestions": archetype_data.get("opening_hooks", archetype_data["suggestions"]),
    }


def evaluate_response_local(user_text, door_state):
    """
    Evalúa la respuesta del asesor comercial de TXU Energy usando el motor
    local de respaldo con reglas de prospección y arquetipos residenciales.
    Diferencia con precisión entre el gancho de apertura (Turno 0) y los
    turnos intermedios o de cierre (Turno >= 1) para evitar confusiones de contexto.
    """
    text = user_text.lower().strip()
    archetype = door_state["archetype"]
    turn = door_state.get("turn", 0)
    messages = door_state.get("messages", [])
    is_opening_turn = (len(messages) == 0) or (turn == 0)

    # Detección de patrones en contexto de energía eléctrica TXU
    has_time_hook = bool(re.search(r'(15 segundo|r[aá]pido|no le quito tiempo|solo un minuto|un momento|de pasada|10 segundo)', text))
    has_pain_probe = bool(re.search(r'(cu[aá]nto paga|recibo|factura|cobro|luz|electricidad|verano|calor|aire acondicionado|a/c|clima|subi[oó]|car[oa]|tarifa variable|consum)', text))
    has_neighbor_social_proof = bool(re.search(r'(vecin|cuadra|manzana|al lado|don |do[nñ]a |aqu[ií] enfrente|calle)', text))
    has_close_attempt = bool(re.search(r'(recibo|factura|compar|revis|hacer el cambio|enrol|registr|cambiarnos|apart|firm|contrat|cambio digital|paso a las|vemos a las|agend)', text))
    has_flyer_surrender = bool(re.search(r'(tenga el folleto|tenga el volante|ah[ií] le dejo|ah[ií] viene mi n[uú]mero|le dejo la tarjeta|1-800)', text))
    has_flyer_redirect = bool(re.search(r'(con gusto|con mucho gusto|se lo dejo pero|antes de dej[aá]rselo|para saber si vale la pena|para saber cu[aá]l|foll|volant)', text))
    has_defensive_claim = bool(re.search(r'(no desconf[ií]e|soy honesto|no soy delincuente|c[aá]lmese|no se enoje)', text))
    has_apology_respect = bool(re.search(r'(disculp|raz[oó]n|respet|permiso|buena tarde|no quise molestar|me retiro|con este calor|comet[ií] un error|mi error)', text))
    has_season_pass = bool(re.search(r'(season pass|50%|cincuenta por ciento|descuento en verano|verano.*gratis|veranos gratis|julio y agosto|invierno|mitad)', text))
    has_free_nights = bool(re.search(r'(noches gratis|free nights|8.*6|costo cero|gratis de noche|cargar|tesla|auto el[eé]ctrico|veh[ií]culo el[eé]ctrico|ev)', text))
    has_cents_kwh = bool(re.search(r'(centavo|\d+\s*centavo|\d+\.\d+\s*centavo|kwh|efl|etiqueta|cr[eé]dito de \$30|clear deal|tarifa fija)', text))
    has_oncor_guarantee = bool(re.search(r'(oncor|centerpoint|cables|postes|no hay corte|no se le va la luz|cero cortes|mismo cableado|distribuidora)', text))
    has_decision_maker_probe = bool(re.search(r'(a qu[eé] hora llega|a qu[eé] hora est[aá]|titular|espos|pap[aá]|mam[aá]|qui[eé]n se encarga|regres|vuelvo|tarde|noche)', text))
    has_attack_competitor = bool(re.search(r'(no sirve|p[eé]sim|obsolet|mentiros|chatarra|porquer[ií]a|robo|abus|se aprovechan)', text))
    has_slamming_assurance = bool(re.search(r'(gafete|oficial|100 a[nñ]os|proteger|esi id|no le pido firmas|no le pido su recibo)', text))
    is_too_long = len(text) > 300

    # Detección de rapport humano, empatía, humor y preguntas abiertas (Flexibilidad conversacional con sustancia)
    has_rapport_greeting = bool(re.search(r'(hola|buen[oa]s\s*(d[ií]as|tardes|noches)|qu[eé]\s*tal|c[oó]mo\s*(est[aá]|le\s*va|anda)|mucho\s*gusto|vecin[oa]|disculpe|calor[oó]n|qu[eé]\s*calor|tremendo\s*calor|vengo\s*pasando)', text))
    has_open_question = bool(re.search(r'(\?|c[oó]mo\s*(le|ve|suele)|cu[aá]nto\s*(paga|le\s*llega)|qu[eé]\s*le\s*parece|le\s*gustar[ií]a|ha\s*(notado|tenido|visto)|usted\s*(suele|paga|tiene)|sabe\s*si|le\s*ha\s*tocado)', text))
    has_empathy_reassurance = bool(re.search(r'(no\s*le\s*quito|no\s*se\s*preocupe|lo\s*entiendo|le\s*entiendo|tiene\s*raz[oó]n|a\s*todos\s*nos|s[eé]\s*que|tranquil[oa]|para\s*servirle|con\s*gusto|sin\s*compromiso|jaja|entiendo\s*perfectamente)', text))

    words = [w for w in re.split(r'\s+', text) if w]
    # Detección de saludos secos o monosílabos sin gancho comercial (ej. "hola", "buenas", "buenas tardes", "hey", "saludos", "disculpe")
    is_bare_greeting = len(words) <= 3 and bool(re.search(r'^(hola|buen[oa]s(\s*(d[ií]as|tardes|noches))?|buen\s*d[ií]a|qu[eé]\s*tal|buenas|hey|saludos|disculpe)(\s*vecin[oa])?[\.\!\?]*$', text))
    is_meaningless_opening = is_opening_turn and len(words) <= 2 and not (has_pain_probe or has_season_pass or has_time_hook or has_open_question or has_close_attempt or has_cents_kwh or has_neighbor_social_proof)

    has_natural_personality = (has_rapport_greeting or has_open_question or has_empathy_reassurance) and not (is_bare_greeting or is_meaningless_opening)

    patience_change = 0
    interest_change = 0
    reply = ""
    coach = ""
    new_suggestions = []

    # ==========================
    # MANEJO DE SALUDOS SECOS O MONOSÍLABOS (SIN GANCHO COMERCIAL)
    # ==========================
    if is_bare_greeting or is_meaningless_opening:
        if is_opening_turn:
            BARE_OPENING_RESPONSES = {
                "HOSTILE": {
                    "patience": -15, "interest": -5,
                    "reply": "¿Sí? ¿Quién es usted y qué se le ofrece? No me haga salir a la puerta con este calorón para decirme solo 'hola'.",
                    "coach": "Un simple saludo no es un gancho comercial. En prospección en frío, dejar vacíos de información ante un prospecto hostil dispara su impaciencia. Debes presentarte con tu nombre, la empresa (TXU Energy) y un marco de tiempo de inmediato.",
                    "suggestions": [
                        "Una disculpa por la interrupción: soy asesor oficial de TXU Energy, solo 15 segundos para no quitarle tiempo con este calor.",
                        "Buenas tardes, disculpe la molestia. Vengo de TXU Energy con los vecinos para revisar el impacto del calor en el recibo de luz."
                    ]
                },
                "BUSY": {
                    "patience": -10, "interest": 0,
                    "reply": "Buenas tardes... dígame rápido joven que voy de salida con el tiempo medido. ¿Qué se le ofrece?",
                    "coach": "Falta de gancho de tiempo y motivo. Un cliente con prisa necesita saber en los primeros 5 segundos quién eres y qué beneficio concreto le ofreces.",
                    "suggestions": [
                        "Solo 15 segundos porque veo que va saliendo: TXU da 50% de descuento en luz en verano. ¿A qué hora le encuentro para hacer el cálculo?",
                        "Una disculpa, voy directo al grano en 10 segundos: represento a TXU Energy para proteger su tarifa de verano."
                    ]
                },
                "SKEPTICAL": {
                    "patience": -5, "interest": -5,
                    "reply": "¿Sí? ¿Quién es usted y de parte de quién viene? No acostumbro abrirle a desconocidos.",
                    "coach": "Alerta de desconfianza. Sin identificación corporativa ni gafete a la vista, el cliente escéptico asume que se trata de un desconocido sospechoso.",
                    "suggestions": [
                        "Buenas tardes señor, asesor oficial de TXU Energy con gafete verificado. No le pido firmas ni datos hoy, solo informarle de la tarifa protegida.",
                        "Buenas tardes, represento a TXU Energy en esta cuadra. ¿Cómo le ha ido con el recibo en estos meses de calor?"
                    ]
                },
                "POLITE_EVASIVE": {
                    "patience": 0, "interest": 0,
                    "reply": "Buenas tardes... dígame, ¿en qué le puedo ayudar? Si viene a vender algo, ¿tiene algún folleto que me deje para revisarlo luego?",
                    "coach": "Saludo cortés pero inerte. Sin una presentación clara ni pregunta de diagnóstico sobre su factura, el prospecto evasivo toma el control para despedirte con el folleto.",
                    "suggestions": [
                        "Con gusto vecina, soy de TXU Energy. Solo una pregunta rápida antes de dejárselo: ¿su recibo suele subir mucho en julio?",
                        "Buenas tardes Doña Elena, vengo de TXU Energy para revisar si califica al 50% de descuento en verano con Season Pass."
                    ]
                },
                "IDEAL_LEAD": {
                    "patience": 0, "interest": +5,
                    "reply": "Buenas tardes. Dígame, ¿de qué empresa viene o qué se le ofrece?",
                    "coach": "El prospecto es accesible pero necesitas presentarte y abrir con el motivo de visita para despertar su interés en el ahorro.",
                    "suggestions": [
                        "Buenas tardes, represento a TXU Energy. Vengo porque con este calor los recibos de luz se están disparando en la colonia.",
                        "Soy asesor de TXU Energy, ¿su última factura de luz vino muy alta por el aire acondicionado?"
                    ]
                },
                "BARGAIN_HUNTER": {
                    "patience": 0, "interest": 0,
                    "reply": "Buenas tardes. ¿De qué compañía es y qué producto trae?",
                    "coach": "Presenta tu empresa y el beneficio financiero de entrada. El cliente analítico necesita saber rápidamente de qué se trata.",
                    "suggestions": [
                        "Buenas tardes, soy asesor de TXU Energy. Estamos ofreciendo planes con tarifa fija protegida desde 12.8 centavos por kWh.",
                        "De TXU Energy, con 50% de descuento en luz en verano. ¿Cuánto paga actualmente por kWh?"
                    ]
                },
                "NON_DECISION_MAKER": {
                    "patience": 0, "interest": 0,
                    "reply": "Buenas tardes... dígame, ¿qué necesita?",
                    "coach": "Identifícate con cordialidad para no intimidar a quien no toma las decisiones en el hogar.",
                    "suggestions": [
                        "Buenas tardes, vengo de TXU Energy con información del ahorro de verano para los vecinos de la cuadra.",
                        "Buenas tardes, solo una pregunta rápida: ¿a qué hora suele estar el titular de la cuenta de luz para dejarle un comparativo?"
                    ]
                },
                "LOYALIST": {
                    "patience": 0, "interest": 0,
                    "reply": "Buenas tardes joven. ¿Qué se le ofrece por aquí?",
                    "coach": "Presenta a TXU Energy con respeto para no activar de inmediato su barrera de fidelidad hacia su proveedor actual.",
                    "suggestions": [
                        "Buenas tardes señor, soy asesor de TXU Energy. Vengo informando a los vecinos sobre cómo proteger la tarifa con Oncor en verano.",
                        "Buenas tardes vecino, disculpe la molestia. ¿Cómo le ha ido con el servicio de electricidad en esta temporada?"
                    ]
                },
                "TECH_SAVVY": {
                    "patience": 0, "interest": 0,
                    "reply": "Buenas tardes. ¿Quién es y qué servicio promueve?",
                    "coach": "Presentación incompleta. Un perfil técnico valora la precisión y directriz inmediata.",
                    "suggestions": [
                        "Buenas tardes, soy de TXU Energy. Traemos el plan Free Nights con electricidad 100% gratuita de noche.",
                        "Buenas tardes, asesor oficial de TXU Energy con planes para hogares inteligentes y vehículos eléctricos."
                    ]
                },
            }
            res_data = BARE_OPENING_RESPONSES.get(archetype, BARE_OPENING_RESPONSES["POLITE_EVASIVE"])
            patience_change = res_data["patience"]
            interest_change = res_data["interest"]
            reply = res_data["reply"]
            coach = res_data["coach"]
            new_suggestions = res_data["suggestions"]
        else:
            # En turnos posteriores (turn >= 1), el vendedor repitió un saludo o se quedó en blanco
            if archetype == "HOSTILE":
                patience_change = -15
                interest_change = -5
                reply = "¿Me va a decir a qué vino o solo va a seguir saludando? No me haga perder el tiempo con este calor."
                coach = "Evita quedarte sin argumentos en medio de la conversación. Plantea de inmediato la solución de Season Pass o retírate con respeto."
                new_suggestions = [
                    "Tiene toda la razón, disculpe: TXU le da 50% de descuento en luz en verano. ¿Cuánto le cobraron el mes pasado?",
                    "Una disculpa señor. Si me regala 1 minuto le digo cuánto le ahorra Season Pass en verano."
                ]
            elif archetype == "BUSY":
                patience_change = -10
                interest_change = 0
                reply = "Joven, ya nos saludamos. Dígame rápido qué trae de TXU o me tengo que ir."
                coach = "No repitas saludos en media conversación con un cliente con prisa. Ve directo a agendar hora o dar una cifra de ahorro."
                new_suggestions = [
                    "Tiene toda la razón: paso a las 6:30 PM a mostrarle el cálculo de ahorro en 2 minutos.",
                    "Una disculpa: TXU da 50% de descuento en verano. ¿A qué hora le encuentro para hacer el cálculo?"
                ]
            else:
                patience_change = -5
                interest_change = 0
                reply = "Sí, dígame... lo sigo escuchando. ¿Qué me decía de TXU?"
                coach = "No te detengas en saludos repetidos a mitad de la plática. Continúa con una pregunta de diagnóstico o tu propuesta de valor."
                new_suggestions = [
                    "Con Season Pass le descontamos el 50% en los meses de calor. ¿Cuánto suele pagar en julio?",
                    "Le protegemos la tarifa fija para que el aire no le dé sorpresas. ¿Le gustaría ver la comparativa?"
                ]

    # ==========================
    # EVALUACIÓN POR ARQUETIPO (TXU ENERGY)
    # ==========================
    elif archetype == "BUSY":
        if is_opening_turn:
            if has_time_hook and (has_pain_probe or has_season_pass or has_neighbor_social_proof):
                patience_change = +15
                interest_change = +30
                reply = "Pues mire, la verdad sí, el mes pasado me llegaron casi $350 dólares de pura luz por tener el aire prendido día y noche. Pero ya tengo el carro encendido."
                coach = "Excelente apertura. Reconociste su prisa, pusiste un marco breve y tocaste el impacto del calor en la factura."
                new_suggestions = [
                    "No le quito más tiempo hoy: ¿a qué hora llega en la tarde para mostrarle el comparativo con Season Pass en 2 minutos?",
                    "¿Le dejo un comparativo con su vecino de al lado para que lo revise con calma?",
                    "¿A las 6:30 PM le queda cómodo que pase a mostrarle el cálculo?"
                ]
            elif has_close_attempt or has_decision_maker_probe:
                patience_change = +15
                interest_change = +25
                door_state["status"] = "APPOINTMENT"
                reply = "Llego a las 6:30 PM. Si pasa a esa hora puntual con gusto le muestro la factura de luz para ver si es cierto el descuento, pero ahorita ya me voy."
                coach = "Aseguramiento de cita exitoso. Concretaste una hora precisa respetando su agenda sin forzarlo."
                new_suggestions = [
                    "A las 6:30 PM puntual estaré aquí. Excelente día de trabajo.",
                    "Perfecto, anotado en mi agenda a las 6:30 PM. Hasta la tarde."
                ]
            elif has_natural_personality:
                patience_change = +10
                interest_change = +15
                reply = "Buenas tardes. Sí, el calor está tremendo hoy, pero de verdad voy de salida. Si es sobre el recibo de luz dígame en dos palabras qué traen o a qué hora me busca."
                coach = "Buen contacto humano. Tu saludo natural y empatía evitaron el portazo inicial. Ahora ve al grano o acuerda una hora."
                new_suggestions = [
                    "Solo 15 segundos: TXU da 50% de descuento en luz en verano. ¿A qué hora le encuentro para hacer el cálculo?",
                    "Sé que va saliendo. ¿Paso a las 6:30 PM a mostrarle la comparativa?"
                ]
            elif is_too_long or has_defensive_claim:
                patience_change = -20
                interest_change = -5
                reply = "No tengo tiempo para discursos largos joven, ya voy tarde al trabajo. Con permiso. [Comienza a cerrar la puerta]"
                coach = "Cuidado con la longitud. Con prospectos con prisa, la brevedad y el respeto al tiempo son tus mejores aliados."
                new_suggestions = [
                    "Una disculpa, solo dígame si le encuentro a las 6:30 PM para revisar su tarifa sin compromiso.",
                    "Tiene toda la razón, que tenga excelente día de trabajo."
                ]
            else:
                patience_change = 0
                interest_change = +10
                reply = "Mire, voy de salida. Si es sobre la luz o el aire acondicionado, dígame rápido qué traen de TXU antes de que me suba al coche."
                coach = "El prospecto te da una pequeña ventana de oportunidad. Menciona el 50% de descuento de Season Pass o agenda hora."
                new_suggestions = [
                    "TXU le da 50% de descuento en verano en los cargos de luz. ¿A qué hora le encuentro para hacer el cálculo?",
                    "¿Cuánto pagó en su última factura para decirle si califica al descuento?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_close_attempt or has_decision_maker_probe:
                patience_change = +15
                interest_change = +25
                door_state["status"] = "APPOINTMENT"
                reply = "Llego a las 6:30 PM. Si pasa a esa hora puntual con gusto sacamos el recibo y hacemos la comparación rápida en 2 minutos."
                coach = "Excelente manejo de la prisa. Aseguraste la cita para la tarde respetando su tiempo."
                new_suggestions = [
                    "A las 6:30 PM en punto estaré aquí con los números listos. Buen camino Don Javier.",
                    "Excelente Don Javier, le anoto a las 6:30 PM. Que tenga productivo día."
                ]
            elif has_season_pass or has_cents_kwh or has_pain_probe:
                patience_change = +10
                interest_change = +25
                reply = "Ese 50% de descuento en verano sí me interesa porque el aire no para. ¿A qué hora me dijo que regresa en la tarde para revisarlo?"
                coach = "Propuesta de valor asimilada. El prospecto valida el beneficio y te pide agendar el horario."
                new_suggestions = [
                    "Regreso a las 6:30 PM en punto. Solo tenga su recibo a mano para calcular el ahorro exacto.",
                    "Paso a las 7:00 PM si le queda más cómodo para que alcancen a cenar tranquilos."
                ]
            elif has_natural_personality:
                patience_change = +10
                interest_change = +15
                reply = "Le agradezco la amabilidad, pero de verdad ya tengo que subirme al coche. Dígame en una sola frase cómo le hacemos para verlo más tarde."
                coach = "Rapport efectivo sin perder el objetivo. Mantén la brevedad y fija la hora de la cita."
                new_suggestions = [
                    "A las 6:30 PM regreso 3 minutos y le muestro el ahorro de su recibo. ¿Le parece bien?",
                    "Paso a las 7:00 PM cuando ya esté desocupado. Buen camino Don Javier."
                ]
            elif is_too_long:
                patience_change = -20
                interest_change = -5
                reply = "Joven, ya le dije que voy tardísimo. Déjeme un papel o pase en la tarde porque ahorita no me puedo quedar. [Cierra la puerta]"
                coach = "Exceso de discurso ante un cliente apurado. Sé sintético y ve directo a la hora de visita."
                new_suggestions = [
                    "Disculpe la molestia, paso a las 6:30 PM. Buen día.",
                ]
            else:
                patience_change = 0
                interest_change = +10
                reply = "Bueno, le entiendo la idea de TXU. ¿A qué hora pasa en la tarde para revisar la factura con calma?"
                coach = "Ventana de oportunidad activa. Concreta la hora exacta antes de que se marche."
                new_suggestions = [
                    "A las 6:30 PM puntual paso con el comparativo listo. Que tenga excelente tarde.",
                ]

    elif archetype == "SKEPTICAL":
        if is_opening_turn:
            if has_apology_respect or has_slamming_assurance or (has_neighbor_social_proof and not has_close_attempt):
                patience_change = +20
                interest_change = +30
                reply = "Bueno... los vecinos sí me dijeron que andaban de TXU Energy. Es que con tantos estafadores uno desconfía. ¿Qué plan tienen para proteger la tarifa?"
                coach = "Gran manejo de la desconfianza. Validar su derecho a proteger su cuenta sin presionar genera credibilidad inmediata."
                new_suggestions = [
                    "Tenemos la promesa Price Protect: tarifa fija por contrato sin aumentos en olas de calor. ¿Sabe si hoy su tarifa es fija o variable?",
                    "Si me permite su última factura 1 minuto, le calculo exactamente cuánto se ahorraría con tarifa protegida.",
                    "En TXU Energy garantizamos por escrito que Oncor mantiene el servicio sin cortes ni trámites raros."
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +20
                reply = "Buenas tardes. Pues sí, con tanto calor uno anda vigilando todo, y aquí seguido pasan a ofrecer cosas raras. ¿Usted viene directo de TXU Energy?"
                coach = "Excelente apertura conversacional. Tu tono relajado y educado generó cercanía sin disparar sospechas."
                new_suggestions = [
                    "Sí señor, asesor oficial de TXU Energy. No vengo a pedirle firmas ni su recibo hoy, solo a informarle de la tarifa protegida.",
                    "Totalmente de TXU Energy, mire mi gafete. ¿Cómo le ha ido con el recibo en estos meses de calor?"
                ]
            elif has_pain_probe or has_cents_kwh:
                patience_change = +15
                interest_change = +25
                reply = "Con la compañía que tengo ahorita nos suben los centavos en verano sin avisar. El recibo se fue a las nubes."
                coach = "Indagación exitosa. Descubriste que sufre por tarifas variables no reguladas. Presenta la promesa Price Protect de TXU."
                new_suggestions = [
                    "Con TXU su tarifa queda congelada por contrato por 24 meses sin sorpresas. ¿Le gustaría que le deje reservado el plan?",
                    "Por esa misma tarifa le damos 50% de descuento en verano y garantía de 60 días. ¿Qué le parecería probarlo?"
                ]
            elif has_close_attempt:
                patience_change = +15
                interest_change = +30
                reply = "Si la tarifa queda firmada por contrato en centavos fijos por 24 meses y no hay letras chiquitas, sí me interesa compararlo."
                coach = "Señal de compra clara. El cliente escéptico necesita garantías contractuales por escrito para cerrar."
                new_suggestions = [
                    "Totalmente garantizado por escrito en la EFL y sin corte de luz. ¿Registramos la cuenta para el próximo ciclo?"
                ]
            elif has_defensive_claim:
                patience_change = -20
                interest_change = -15
                reply = "Gafetes cualquiera los imprime. No le voy a mostrar ningún recibo, por favor retírese de mi propiedad."
                coach = "Evita sonar a la defensiva. En vez de 'no desconfíe', valida su precaución ('hace muy bien en protegerse')."
                new_suggestions = [
                    "Comprendo su precaución y tiene toda la razón. No le pido datos hoy. Le dejo el número oficial de TXU Energy para que verifique cuando guste.",
                    "Disculpe la molestia, que tenga buen día."
                ]
            else:
                patience_change = 0
                interest_change = +10
                reply = "A ver... cuénteme cómo funciona eso de TXU, pero sin compromisos de firma hoy."
                coach = "El cliente baja la guardia. Explica la tarifa fija protegida o la garantía de satisfacción de 60 días."
                new_suggestions = [
                    "TXU le da 60 días de prueba sin penalización: si no le convence el ahorro, puede cambiar de plan libremente. ¿Le parece justo?",
                    "¿Cuánto pagó en su última factura para demostrarle la diferencia exacta en dólares?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_oncor_guarantee or has_cents_kwh or has_season_pass:
                patience_change = +20
                interest_change = +30
                reply = "Eso de que Oncor sigue con los mismos postes y que la tarifa viene fija en la EFL me da más tranquilidad. ¿Y si al mes no veo el ahorro me cobran multa por salirme?"
                coach = "Excelente desactivación de objeción técnica. El cliente pide garantías; presenta los 60 días de prueba de TXU sin penalización."
                new_suggestions = [
                    "Tiene 60 días de garantía total: si no está 100% satisfecho, se cambia sin pagar un solo dólar de penalización. ¿Revisamos su factura?",
                    "Exactamente cero penalización en los primeros 60 días. Vamos a checar el consumo en su recibo para comprobar el ahorro."
                ]
            elif has_close_attempt:
                patience_change = +15
                interest_change = +30
                reply = "Mire, si la tarifa queda fijada en el contrato tal como dice y tengo los 60 días de garantía, vamos a checar esa factura a ver si de verdad conviene."
                coach = "Señal de cierre lograda con un cliente analítico y desconfiado. Pide amablemente la factura para identificar el ESI ID."
                new_suggestions = [
                    "Trato hecho Don Roberto. Con su factura a mano le muestro en 1 minuto la diferencia en centavos.",
                    "Excelente, revisamos juntos renglón por renglón para que no quede ninguna duda."
                ]
            elif has_natural_personality:
                patience_change = +10
                interest_change = +15
                reply = "Mire, le reconozco que habla con franqueza y sin presiones. Pero dígame: ¿esa tarifa protegida cuánto tiempo dura garantizada?"
                coach = "Confianza ganada. Tu postura transparente desarmó las sospechas. Confirma la vigencia contractual de 12 o 24 meses."
                new_suggestions = [
                    "Dura 12 o 24 meses completos por contrato, garantizado ante la PUC de Texas. ¿Revisamos su recibo?",
                    "Queda congelada por 2 años sin importar cuánto suba la luz en Texas. ¿Le gustaría apartar esa protección?"
                ]
            elif has_defensive_claim:
                patience_change = -20
                interest_change = -15
                reply = "Ya empezó a justificarse. Si tanto insiste en que confíe en usted, menos le voy a enseñar ningún papel. Buenas tardes."
                coach = "Alerta defensiva. Valida siempre la prudencia del prospecto sin forzar confianza."
                new_suggestions = [
                    "Tiene toda la razón, disculpe si sonó insistente. Que pase muy buena tarde.",
                ]
            else:
                patience_change = 0
                interest_change = +10
                reply = "Sigo escuchando, pero quiero ver dónde dice por escrito que la tarifa no va a subir cuando llegue la ola de calor."
                coach = "Objeción de seguridad. Refuerza la EFL (Electricity Facts Label) regulada por el estado de Texas."
                new_suggestions = [
                    "Todo viene certificado en la EFL regulada por el estado de Texas. ¿Me permite mostrarle un ejemplo con su última factura?",
                ]

    elif archetype == "POLITE_EVASIVE":
        if is_opening_turn:
            if has_flyer_redirect and has_pain_probe:
                patience_change = +10
                interest_change = +35
                reply = "Pues mire... la verdad el mes pasado pagué casi $320 dólares y casi ni estamos en el día. No entiendo por qué subió tanto."
                coach = "Excelente técnica 'Acepta y Redirige'. Concediste la petición del folleto pero aislaste el problema real de su factura."
                new_suggestions = [
                    "Podemos aplicarle el plan Season Pass para que en julio y agosto pague la mitad de energía. ¿A qué hora está su familia para revisarlo juntos?",
                    "Si le consigo el crédito automático de $30 dólares en factura, ¿le aparto su registro hoy mismo?"
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +25
                reply = "Buenas tardes joven. Sí, tremendo calorón hoy. Oiga, y esa propuesta de TXU, ¿de verdad le ha bajado el recibo a la gente de esta cuadra?"
                coach = "Muy buen rapport. Tu personalidad amable y cercana rompió la barrera de evasión inicial."
                new_suggestions = [
                    "A los vecinos les ahorramos hasta 50% en verano con Season Pass. ¿Su último recibo superó los $250 dólares?",
                    "Con gusto le muestro el folleto, solo dígame si su tarifa actual es fija o variable para saber cuál dejarle."
                ]
            elif has_flyer_surrender:
                patience_change = 0
                interest_change = -15
                reply = "Muchas gracias joven, que le vaya muy bien y venda mucho. [Cierra la puerta amablemente con el volante en la mano]"
                coach = "Alerta de folleto. Entregar el volante sin hacer una pregunta de diagnóstico suele terminar la conversación."
                new_suggestions = [
                    "¡Solo una pregunta rápida antes de que entre vecina! ¿Su recibo suele subir mucho en julio?",
                    "Agradecer amablemente y pasar a la siguiente puerta."
                ]
            elif has_close_attempt or has_decision_maker_probe:
                patience_change = +10
                interest_change = +25
                reply = "A las 6:30 ya llega mi esposo de trabajar y podemos sacar la factura para revisarla juntos si gusta pasar a esa hora."
                coach = "Aseguramiento de tomador de decisiones. Gran paso para revisar la factura con la familia completa."
                new_suggestions = [
                    "Excelente, a las 6:30 PM en punto regreso para platicarlo con los dos. Gracias Doña Elena."
                ]
            else:
                patience_change = 0
                interest_change = +10
                reply = "Buenas tardes, sí dígame... ¿Tiene algún folleto que me deje para revisarlo con calma? Es que ando algo ocupada."
                coach = "Objeción evasiva típica. Aplica 'Acepta y Redirige': valida el folleto pero haz una pregunta sobre el costo del aire acondicionado."
                new_suggestions = [
                    "Con gusto le dejo el folleto Doña Elena, pero para saber cuál le conviene: ¿su recibo subió mucho por el aire este mes?",
                    "Claro que sí, se lo dejo. Solo una pregunta rápida: ¿sabe cuántos centavos le cobran ahorita por kWh?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_season_pass or (has_pain_probe and ("verano" in text or "gratis" in text)):
                patience_change = +15
                interest_change = +30
                reply = "Eso de tener 50% de descuento o veranos con beneficio suena de verdad muy tentador porque el aire no para. ¿Pero cómo funciona el contrato, no me obligan a quedarme si no me gusta?"
                coach = "Excelente avance en la propuesta de valor. Conectaste la solución con su preocupación real del calor. Presenta la garantía de satisfacción de 60 días."
                new_suggestions = [
                    "TXU le da 60 días de garantía total sin penalización para que compruebe el ahorro. ¿Tiene su factura para calcular la diferencia?",
                    "No hay ataduras a ciegas: tiene 60 días de prueba y Oncor mantiene los mismos cables sin cortes de luz. ¿Revisamos su recibo?"
                ]
            elif has_close_attempt:
                patience_change = +15
                interest_change = +35
                reply = "Mire, me convence lo que me dice y la verdad sí necesitamos bajar ese recibo. Aquí tengo la última factura en la mesa, déjeme traerla para que la comparemos."
                coach = "Excelente cierre de diagnóstico. Conseguiste que la clienta evasiva vaya por su factura con total confianza."
                new_suggestions = [
                    "Perfecto Doña Elena, le espero aquí mismo. Revisamos el cargo por kWh y calculamos su ahorro en 1 minuto.",
                    "Muchas gracias Doña Elena, con su recibo validamos si califica al crédito de $30 dólares de inmediato."
                ]
            elif has_natural_personality or has_apology_respect:
                patience_change = +10
                interest_change = +20
                reply = "Tiene mucha razón con lo del calor, aquí en Texas no se puede vivir sin el clima encendido y da pendiente ver llegar el cobro. A ver, cuénteme bien cómo le haríamos para comparar."
                coach = "Excelente fluidez conversacional. Mantienes la cercanía humana y guías a la clienta hacia el diagnóstico de su factura sin que se cierre."
                new_suggestions = [
                    "Con Season Pass le descontamos el 50% en los meses de calor. ¿Tiene su factura a la mano para ver cuánto pagó el mes pasado?",
                    "Solo comparamos el cobro de energía de su último recibo y si no le conviene nos despedimos como amigos. ¿Le parece?"
                ]
            elif has_flyer_surrender:
                patience_change = 0
                interest_change = -15
                reply = "Muchas gracias joven, que le vaya muy bien y venda mucho. [Cierra la puerta amablemente con el volante en la mano]"
                coach = "Alerta de folleto. Entregar el volante sin hacer una pregunta de diagnóstico terminó la conversación."
                new_suggestions = [
                    "¡Solo una pregunta rápida antes de que entre vecina! ¿Su recibo suele subir mucho en julio?",
                    "Agradecer amablemente y pasar a la siguiente puerta."
                ]
            elif has_decision_maker_probe:
                patience_change = +10
                interest_change = +25
                reply = "A las 6:30 ya llega mi esposo de trabajar y podemos sacar la factura para revisarla juntos si gusta pasar a esa hora."
                coach = "Aseguramiento de tomador de decisiones. Gran paso para revisar la factura con la familia completa."
                new_suggestions = [
                    "Excelente, a las 6:30 PM en punto regreso para platicarlo con los dos. Gracias Doña Elena."
                ]
            else:
                patience_change = +5
                interest_change = +15
                reply = "Sí suena interesante lo de TXU, pero cuénteme un poco más: ¿cuánto paga la gente normalmente con ustedes en estos meses de calor?"
                coach = "Interés creciente. Plantea una cifra de ahorro o el plan Season Pass para afianzar el avance."
                new_suggestions = [
                    "Con Season Pass los meses de calor tienen 50% de descuento. ¿Cuánto le llegó el mes pasado?",
                    "En promedio pagan entre 12 y 13 centavos fijos. ¿Le gustaría comparar su tarifa?"
                ]

    elif archetype == "HOSTILE":
        if is_opening_turn:
            if has_apology_respect or has_empathy_reassurance:
                patience_change = +30
                interest_change = +25
                reply = "[Baja el tono, sorprendido por su educación] ... Bueno, es que han pasado como cuatro hoy a molestar con este calor. Mire, discúlpeme el tono. ¿Dice que viene de TXU Energy?"
                coach = "Desescalada magistral. La empatía genuina y el respeto desarman la irritabilidad mucho mejor que cualquier discurso de ventas."
                new_suggestions = [
                    "Lo entiendo perfectamente señor, con este calor cualquiera se molesta. En TXU solo buscamos que no pague de más por el aire acondicionado.",
                    "Una disculpa nuevamente. Si me regala 1 minuto le digo cuánto le ahorra Season Pass en verano."
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +20
                reply = "Mire joven, ando de malas con este calorón, pero al menos usted habla con respeto. A ver, dígame rápido qué es lo que traen de TXU."
                coach = "Excelente actitud humana. Tu serenidad y compostura transformaron un momento hostil en una oportunidad."
                new_suggestions = [
                    "TXU Season Pass da 50% de descuento en luz en los meses de calor. ¿Cuánto le cobraron el mes pasado?",
                    "Solo 30 segundos: si su factura superó los $300 dólares, podemos congelarle la tarifa a la mitad en verano."
                ]
            elif has_defensive_claim:
                patience_change = -30
                interest_change = -20
                reply = "¡¿Qué me calme?! ¡Aprenda a respetar propiedad privada o llamo a la policía! [Portazo fuerte]"
                coach = "Decir 'cálmese' a una persona molesta siempre aumenta la fricción. La humildad y disculpa sincera siempre ganan."
                new_suggestions = [
                    "Retirarse con calma y continuar en la siguiente puerta."
                ]
            elif has_pain_probe or has_season_pass:
                patience_change = +15
                interest_change = +25
                reply = "Los de mi compañía me cobraron $420 dólares el mes pasado y no me quisieron hacer ningún ajuste. ¿Ustedes de verdad tienen descuento o es el mismo cuento?"
                coach = "El cliente reveló la verdadera causa de su enojo: una factura desmedida. Presenta el alivio de Season Pass."
                new_suggestions = [
                    "Le entiendo completamente. En TXU Season Pass le descontamos el 50% en los meses de calor. ¿Revisamos su factura para corregirlo?"
                ]
            else:
                patience_change = 0
                interest_change = +5
                reply = "Bueno, ya está aquí. Dígame rápido de qué se trata antes de que me meta."
                coach = "Ocasión abierta. Ve directo al beneficio principal de verano sin rodeos corporativos."
                new_suggestions = [
                    "TXU le da 50% de descuento en verano y tarifa fija protegida. ¿Cuánto pagó el mes pasado de luz?",
                    "¿Le gustaría congelar su tarifa para que el aire acondicionado no le dispare el recibo?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_pain_probe or has_season_pass:
                patience_change = +20
                interest_change = +30
                reply = "Los de mi compañía me clavaron más de $400 el mes pasado. Si con ese Season Pass de verdad me bajan la mitad en julio y agosto, tráigame los números."
                coach = "El cliente hostil encuentra una razón de peso para escuchar. Dirige la conversación a revisar el recibo para constatar el ahorro."
                new_suggestions = [
                    "Con su factura en mano le digo en 1 minuto los dólares exactos de ahorro con Season Pass. ¿La tiene a mano?",
                    "Le calculo la diferencia de inmediato Don Carlos, para que compruebe que no son promesas al aire."
                ]
            elif has_close_attempt:
                patience_change = +20
                interest_change = +35
                reply = "Mire, si me garantiza por contrato que no hay cuotas raras y la tarifa queda protegida, déjeme traer la factura para ver la diferencia."
                coach = "Victoria en puerta difícil. Convertiste a un cliente enfurecido en un prospecto dispuesto a comparar su recibo."
                new_suggestions = [
                    "Excelente Don Carlos, aquí le espero. Comprobamos la tarifa centavo por centavo.",
                ]
            elif has_natural_personality or has_apology_respect:
                patience_change = +15
                interest_change = +20
                reply = "Mire, reconozco que tiene temple y educación para tratar a la gente. Pero dígame en concreto: ¿cuánto me voy a ahorrar si me cambio con ustedes?"
                coach = "Desescalada exitosa. El cliente bajó la hostilidad y ahora pide una respuesta concreta a su problema de facturación."
                new_suggestions = [
                    "Con Season Pass se ahorra 50% en energía de verano. ¿Cuánto le cobraron el mes pasado?",
                    "En promedio nuestros clientes ahorran entre $80 y $120 al mes en verano. ¿Comparamos su tarifa actual?"
                ]
            elif has_defensive_claim:
                patience_change = -30
                interest_change = -20
                reply = "¡No me diga qué hacer en mi propia casa! Con permiso. [Portazo fuerte]"
                coach = "Evita justificaciones defensivas ante clientes irritables. La disculpa breve es la única salida."
                new_suggestions = [
                    "Retirarse con calma y continuar en la siguiente puerta."
                ]
            else:
                patience_change = +5
                interest_change = +10
                reply = "Sigo esperando que me diga los números sin rodeos. ¿Cuánto cuesta el servicio con ustedes?"
                coach = "El prospecto hostil exige hechos concretos. Explica la tarifa en centavos por kWh y el beneficio de verano."
                new_suggestions = [
                    "Son 12.8 centavos con crédito de $30 dólares incluido y tarifa fija por 24 meses. ¿Revisamos su consumo?",
                ]

    elif archetype == "IDEAL_LEAD":
        if is_opening_turn:
            patience_change = +15
            interest_change = +35
            reply = "Buenas tardes. Qué bueno que pasa de TXU, fíjese que el mes pasado me cobraron casi $400 dólares de luz y ando buscando opciones. ¿Qué planes tienen?"
            coach = "Excelente apertura. El prospecto tiene una necesidad inmediata de ahorro; presenta Season Pass o Clear Deal."
            new_suggestions = [
                "TXU Season Pass le da 50% de descuento en verano y tarifa congelada. ¿Tiene su última factura para ver cuánto le ahorraría?",
                "Podemos aplicarle una tarifa fija protegida desde 12.8 centavos con crédito de $30 dólares. ¿Le gustaría revisarlo?"
            ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_close_attempt or has_season_pass or has_cents_kwh or has_natural_personality:
                patience_change = +15
                interest_change = +40
                reply = "El mes pasado pagué casi $400 dólares. Si con TXU Season Pass me dan el 50% de descuento en verano y precio congelado, me cambio hoy mismo. ¿Qué necesita para el trámite?"
                coach = "Cliente ideal listo para la firma. Pide su última factura para ingresar el número ESI ID en el sistema."
                new_suggestions = [
                    "Trato hecho Doña Sofía. Tomo los datos de su recibo y queda registrada en TXU hoy mismo sin cortes de luz. ¿A qué nombre elaboro el contrato?",
                    "Solo necesitamos su factura a la mano para validar su número ESI ID y activar el plan."
                ]
            elif is_too_long:
                patience_change = -10
                interest_change = 0
                reply = "Son demasiadas opciones joven. Solo dígame cuánto me voy a ahorrar en verano y cómo hacemos el cambio de una vez."
                coach = "Simplifica el proceso: el prospecto ya quiere comprar, facilítale el trámite de inmediato."
                new_suggestions = [
                    "Con Season Pass se ahorra la mitad en cargos de energía en verano. ¿Hacemos el registro en 2 minutos?"
                ]
            else:
                patience_change = +10
                interest_change = +25
                reply = "Ahorita estoy pagando casi 18 centavos con la otra compañía y me sube en verano. ¿A cuánto me quedaría con TXU?"
                coach = "Señal de compra evidente. Plantea el precio protegido con Season Pass o Clear Deal."
                new_suggestions = [
                    "Con nosotros la tarifa queda protegida desde 12.8 centavos con crédito incluido. ¿Revisamos su factura de una vez?"
                ]

    elif archetype == "BARGAIN_HUNTER":
        if is_opening_turn:
            if has_cents_kwh or has_season_pass:
                patience_change = +15
                interest_change = +35
                reply = "A 12.8 centavos promedio con el crédito de $30 de TXU y 50% de descuento en verano, los números sí me cuadran. ¿Qué documentos necesita para el trámite?"
                coach = "Gran apertura analítica. El prospecto comprobó los números netos sin sorpresas."
                new_suggestions = [
                    "Solo su última factura para ingresar su ESI ID y programar el cambio en Oncor sin cortes. ¿A qué nombre elaboro el registro?",
                    "¿Prefiere el plan a 12 meses o a 24 meses con tarifa protegida?"
                ]
            elif has_natural_personality:
                patience_change = +10
                interest_change = +20
                reply = "Buenas tardes. Mire, me gusta la gente clara y directa. ¿Cuánto me cobra TXU en centavos por kWh si consumo unos 1,200 kWh al mes?"
                coach = "Buen contacto inicial. Tu actitud segura y relajada abrió una conversación productiva sobre costos."
                new_suggestions = [
                    "En Clear Deal le queda en 12.8 centavos netos con el crédito de $30 dólares de TXU incluido. ¿Revisamos su factura?",
                    "Depende de si prefiere crédito en factura con Clear Deal o 50% de descuento en verano con Season Pass. ¿Cuál le llama más?"
                ]
            elif is_too_long:
                patience_change = -15
                interest_change = -5
                reply = "Puro rollo y no me dijo el precio exacto por kWh en la EFL a 1,000 kWh. Si no me da números claros no me haga perder el tiempo."
                coach = "Al cliente analítico dale números concretos: centavos por kWh y créditos desglosados."
                new_suggestions = [
                    "Son 12.8 centavos netos por kWh en la EFL a 1,000 kWh con crédito de $30 dólares. ¿Le aparto el registro?",
                    "Una disculpa, voy al grano: Clear Deal a 12.8 centavos fijos. ¿Le conviene?"
                ]
            else:
                patience_change = 0
                interest_change = +15
                reply = "¿Y ese plan tiene cargo base mensual o penalización si gasto menos de 1,000 kWh? Quiero ver la etiqueta EFL."
                coach = "Objeción técnica de costos. Explica la transparencia de la EFL y los créditos de TXU."
                new_suggestions = [
                    "La EFL desglosa cargo de energía y cargo TDU de Oncor con total transparencia. ¿Revisamos su consumo mensual?",
                    "¿Cuánto consume en kWh al mes para calcularle el costo neto exacto en dólares?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_cents_kwh or has_season_pass or has_close_attempt:
                patience_change = +20
                interest_change = +35
                reply = "A 12.8 centavos netos con el crédito de $30 de TXU y el 50% de descuento en verano, la matemática me da a favor. Déjeme sacar el recibo para cotejar el ESI ID."
                coach = "Cierre analítico consumado. El prospecto validó las cuentas y busca su factura para formalizar el registro."
                new_suggestions = [
                    "Excelente Don Andrés. Con el ESI ID dejamos el trámite programado hoy mismo.",
                    "Perfecto, aquí le espero para ingresar los datos en el sistema."
                ]
            elif has_natural_personality:
                patience_change = +10
                interest_change = +15
                reply = "Se oye bien, pero a ver: hágame la matemática rápida con números reales. ¿Cuánto me saldría el kWh neto ya sumando los cargos de Oncor y el crédito de $30?"
                coach = "Conversación analítica de alto nivel. Responde con precisión de centavos para consolidar el cierre técnico."
                new_suggestions = [
                    "Son 12.8 centavos por kWh neto en base a 1,000 kWh de consumo mensual con crédito de $30. ¿Comparamos con su recibo?",
                ]
            elif is_too_long:
                patience_change = -15
                interest_change = -5
                reply = "Demasiado rodeo para una pregunta de centavos. Si no tiene la cifra neta exacta en mente, mejor ni le mueva."
                coach = "Sé directo con clientes calculadores: tarifa neta, crédito y vigencia."
                new_suggestions = [
                    "Son 12.8 centavos netos fijos por contrato de 24 meses. ¿Le interesa checarlo en su factura?",
                ]
            else:
                patience_change = +5
                interest_change = +15
                reply = "¿Y la etiqueta EFL cuánto marca en el nivel de 2,000 kWh? Porque en verano mi consumo sube bastante."
                coach = "Análisis de consumo intensivo. Muestra el comportamiento de la tarifa en consumos altos."
                new_suggestions = [
                    "A 2,000 kWh la tarifa se mantiene muy competitiva y el 50% de Season Pass amortigua el pico. ¿Revisamos su factura?",
                ]

    elif archetype == "NON_DECISION_MAKER":
        if is_opening_turn:
            if has_decision_maker_probe:
                patience_change = +25
                interest_change = +25
                door_state["status"] = "APPOINTMENT"
                reply = "Mi pareja llega a las 7:00 PM del trabajo. Si pasa a esa hora puntual con gusto sacamos la factura de luz y lo revisan."
                coach = "Excelente calificación de rol. En cambaceo es clave no desgastar la oferta con quien no es titular de la cuenta ante ERCOT."
                new_suggestions = [
                    "A las 7:00 PM en punto estaré aquí para revisar la factura con ustedes en 3 minutos. Muchas gracias.",
                    "Perfecto, anotado en mi agenda a las 7:00 PM. Que pase buena tarde."
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +20
                reply = "Hola buenas tardes. Sí, la verdad el aire acondicionado no para en todo el día con este calor. ¿A qué hora dijo que convenía que pase para que esté mi pareja?"
                coach = "Gran empatía. Conversar amablemente sin presionar a firmar hace que el familiar facilite el horario del titular con gusto."
                new_suggestions = [
                    "¿Le acomoda que pase a las 6:30 o 7:00 PM cuando ya estén más tranquilos?",
                    "¿Me permitiría dejarle una nota breve con el comparativo de TXU Season Pass para que lo platiquen en la noche?"
                ]
            elif is_too_long or has_close_attempt:
                patience_change = -20
                interest_change = -10
                reply = "Joven, ya le dije que la cuenta de luz está a nombre de mi pareja y yo aquí no firmo nada. No insista conmigo por favor."
                coach = "Recuerda no presionar a firmar a quien no es titular. Enfócate en obtener el horario de quien decide."
                new_suggestions = [
                    "Tiene toda la razón, una disculpa. Solo dígame a qué hora llega el titular para pasar brevemente.",
                    "Disculpe la molestia, que tenga muy buena tarde."
                ]
            else:
                patience_change = 0
                interest_change = +10
                reply = "Pues se oye bien lo de TXU, pero como le digo, quien paga y decide eso es mi familiar cuando llegue."
                coach = "Identificación de rol. Solicita amablemente a qué hora está en casa el titular de la factura."
                new_suggestions = [
                    "Entiendo perfectamente. ¿A qué hora le encuentro hoy por la tarde para dejarle la propuesta en sus manos?",
                    "¿Le puedo dejar una nota con el cálculo de ahorro de verano para que lo platiquen en familia?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_decision_maker_probe:
                patience_change = +25
                interest_change = +30
                door_state["status"] = "APPOINTMENT"
                reply = "Mi pareja llega a las 7:00 PM del trabajo. Si pasa a esa hora puntual con gusto sacamos la factura de luz y lo checamos con los dos."
                coach = "Excelente gestión de cita. Aseguraste el horario en que estará presente la persona que toma las decisiones financieras."
                new_suggestions = [
                    "A las 7:00 PM en punto estaré aquí para revisar la factura con ustedes en 3 minutos. Muchas gracias.",
                    "Perfecto, anotado en mi agenda a las 7:00 PM. Que tengan muy buena tarde."
                ]
            elif has_close_attempt:
                patience_change = -10
                interest_change = 0
                reply = "Como le comenté, yo no tomo esa decisión sola. Pero si regresa a las 7:00 PM que ya esté mi pareja, con gusto lo vemos."
                coach = "Reiteración de rol. No presiones a cerrar a quien no es titular; cierra la cita con ambos presentes."
                new_suggestions = [
                    "Tiene toda la razón. A las 7:00 PM en punto regreso para mostrárselo a los dos. Gracias.",
                ]
            elif has_natural_personality or has_season_pass:
                patience_change = +15
                interest_change = +20
                reply = "Tiene mucha razón, a los dos nos preocupa lo que llega en la factura de la luz. Si gusta dígame a qué hora regresa para que mi pareja lo atienda con gusto."
                coach = "Rapport excelente. El familiar se convierte en tu aliado interno; coordina la hora exacta de visita con el titular."
                new_suggestions = [
                    "¿Le acomoda que pase a las 7:00 PM cuando ya estén más tranquilos?",
                    "Paso a las 7:00 PM en punto y les explico en 2 minutos cómo funciona Season Pass. Gracias."
                ]
            else:
                patience_change = +5
                interest_change = +10
                reply = "Mire, le voy a comentar a mi pareja lo que me dijo del ahorro de verano. ¿A qué hora le dijo que convenía que regrese?"
                coach = "Alianza con el no-decisor lograda. Define la hora exacta para cerrar la cita."
                new_suggestions = [
                    "Regreso a las 7:00 PM con la propuesta lista. Que tenga bonita tarde.",
                ]

    elif archetype == "LOYALIST":
        if is_opening_turn:
            if has_oncor_guarantee or has_season_pass:
                patience_change = +20
                interest_change = +35
                reply = "¿O sea que Oncor sigue entregando la luz por los mismos cables y no hay ningún corte? Si no me arriesgo a quedarme sin aire acondicionado, vale la pena checarlo."
                coach = "Excelente desactivación de miedo. Aclarar que Oncor mantiene los cables físicos disipa el temor al cambio."
                new_suggestions = [
                    "Exactamente, cero minutos sin servicio garantizado. ¿Revisamos su factura para calcular la diferencia con Season Pass?",
                    "Totalmente garantizado. ¿A qué hora le acomoda que le deje el comparativo impreso?"
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +20
                reply = "Buenas tardes vecino. Sí, qué calorón. Mire, yo llevo años con Reliant por costumbre, pero dígame la verdad: ¿cuánto se ahorra realmente uno con TXU?"
                coach = "Gran rapport. Tu respeto y calidez abrieron el interés de un cliente tradicionalmente fiel a su empresa."
                new_suggestions = [
                    "Con Season Pass se ahorra la mitad de la energía en julio y agosto, y Oncor sigue entregando el servicio sin cortes. ¿Comparamos su factura?",
                    "Reliant es una buena compañía, pero TXU le da 60 días de garantía total para probar el ahorro sin compromiso. ¿Qué le parecería?"
                ]
            elif has_attack_competitor:
                patience_change = -25
                interest_change = -20
                reply = "A mí Reliant me ha cumplido bien todos estos años y no me gusta que vengan a hablar mal de ellos a mi puerta. Buenas tardes."
                coach = "Nunca hables mal del proveedor actual. Valida su lealtad y enfócate en las ventajas objetivas de TXU."
                new_suggestions = [
                    "Tiene toda la razón y una disculpa por el comentario. Respeto su lealtad con su empresa. Que pase buena tarde."
                ]
            else:
                patience_change = 0
                interest_change = +15
                reply = "Es que ya estoy acostumbrado a ellos. Cambiarme de compañía de luz siempre se me hace un lío de trámites."
                coach = "Objeción de inercia. Explica que la migración es 100% digital a través del medidor inteligente sin trámites."
                new_suggestions = [
                    "El cambio a TXU es 100% digital por su medidor inteligente, sin papeleos ni cortes de energía. ¿Hacemos la prueba?",
                    "¿Hace cuánto que Reliant no le ajusta la tarifa para compensar el consumo de verano?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_oncor_guarantee or has_season_pass:
                patience_change = +20
                interest_change = +35
                reply = "Si Oncor sigue a cargo de los cables y el cambio es en automático por el medidor sin que me corten la luz, entonces sí vale la pena revisarlo. ¿Cuánto tardaría el trámite?"
                coach = "Miedo al cambio superado por completo. Concreta el proceso explicando que toma 2 minutos con su número ESI ID."
                new_suggestions = [
                    "Toma exactamente 2 minutos: solo ingresamos su ESI ID y Oncor hace la transición digital. ¿Revisamos su factura?",
                    "Es inmediato y sin interrupciones. Con su factura a mano le muestro el ahorro exacto."
                ]
            elif has_close_attempt:
                patience_change = +15
                interest_change = +35
                reply = "Mire, me convence lo de los 60 días de prueba y el 50% en verano. Déjeme traer el recibo para ver la diferencia de tarifas."
                coach = "Cierre de inercia conseguido. El cliente tradicionalmente fiel accede a contrastar su cuenta."
                new_suggestions = [
                    "Excelente Don Fernando, aquí le espero para hacer la comparativa con total transparencia.",
                ]
            elif has_natural_personality:
                patience_change = +10
                interest_change = +20
                reply = "Mire que me cuesta trabajo cambiar tras tantos años, pero con lo que me cuenta del 50% de descuento en verano da para pensarlo. ¿Y si no me convence el cambio me cobran penalización?"
                coach = "Rompiste la inercia del cliente leal. Explica la garantía de satisfacción de 60 días de TXU sin penalización."
                new_suggestions = [
                    "Tiene 60 días de garantía total: si no le convence, puede cambiarse sin pagar penalización. ¿Le gustaría probarlo?",
                ]
            elif has_attack_competitor:
                patience_change = -25
                interest_change = -20
                reply = "No me gusta que hablen mal de la compañía que he tenido 10 años. Gracias, pero no me interesa. [Cierra la puerta]"
                coach = "Respetar la elección pasada del cliente es fundamental para no generar rechazo."
                new_suggestions = [
                    "Disculpe la molestia Don Fernando, que tenga buena tarde.",
                ]
            else:
                patience_change = +5
                interest_change = +15
                reply = "Bueno, le entiendo. Pero a ver: ¿qué garantía tengo de que TXU no me va a subir la tarifa a los tres meses?"
                coach = "Objeción de seguridad. Explica la tarifa fija por contrato con la promesa Price Protect."
                new_suggestions = [
                    "Queda protegida por contrato legal por 12 o 24 meses sin variaciones. ¿Comparamos su factura?",
                ]

    elif archetype == "TECH_SAVVY":
        if is_opening_turn:
            if has_free_nights or has_cents_kwh:
                patience_change = +25
                interest_change = +40
                reply = "Electricidad 100% gratuita de 8:00 PM a 6:00 AM para cargar el auto y enfriar la casa a costo cero me parece ideal. ¿Cómo registramos el plan?"
                coach = "Conexión técnica perfecta. Alineaste Free Nights & Solar Days con su alta demanda nocturna de energía."
                new_suggestions = [
                    "Solo ingresamos su número ESI ID y correo para activar Free Nights en su próximo ciclo. ¿A qué nombre elaboro el registro?",
                    "¿Tiene su recibo a la mano para confirmar que su medidor inteligente esté listo para Free Nights?"
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +25
                reply = "Buenas tardes. Sí, con este calor y cargando el auto eléctrico la factura se va al cielo. Oiga, ¿TXU tiene planes con tarifa cero de noche?"
                coach = "Excelente entrada. Tu naturalidad invitó al prospecto a expresar su principal interés tecnológico de inmediato."
                new_suggestions = [
                    "Sí señor, el plan Free Nights & Solar Days le da energía 100% gratuita de 8:00 PM a 6:00 AM todos los días. ¿Le conviene para su auto?",
                    "Con termostato inteligente y auto eléctrico, Free Nights le ahorra cientos de dólares al año. ¿Revisamos su recibo?"
                ]
            elif has_flyer_surrender or is_too_long:
                patience_change = -15
                interest_change = -5
                reply = "Pura publicidad genérica sin datos de horarios ni de la EFL. No me resolvió lo de las horas gratis de noche. Paso, gracias."
                coach = "A un perfil tecnológico dale datos concretos del horario de 8:00 PM a 6:00 AM de Free Nights."
                new_suggestions = [
                    "Una disculpa, le confirmo: de 8:00 PM a 6:00 AM la energía es 100% gratis por contrato todos los días. ¿Le interesa revisarlo?"
                ]
            else:
                patience_change = 0
                interest_change = +15
                reply = "¿Pero el horario gratis empieza a las 8:00 PM o a las 9:00 PM? Porque es a la hora que programo el cargador del auto."
                coach = "Pregunta técnica clave. Confirma el horario de 8:00 PM a 6:00 AM de Free Nights para consolidar el cierre."
                new_suggestions = [
                    "Inicia a las 8:00 PM en punto hasta las 6:00 AM. Cero costo de energía en ese horario. ¿Apartamos su plan?",
                    "Son 10 horas completas de energía gratis cada noche, ideal para su auto eléctrico. ¿Hacemos el registro?"
                ]
        else:
            # Turno >= 1 (Conversación en desarrollo)
            if has_free_nights or has_close_attempt:
                patience_change = +25
                interest_change = +40
                reply = "De 8:00 PM a 6:00 AM a costo cero cuadra perfecto con mi rutina de carga y termostato. Vamos a checar el medidor inteligente con el recibo para hacer el enrolamiento."
                coach = "Cierre tecnológico concretado. El prospecto valida el ajuste con su perfil de consumo y procede al registro."
                new_suggestions = [
                    "Excelente Don Diego. Con su ESI ID validamos la compatibilidad y dejamos programado Free Nights.",
                    "Perfecto, revisamos su factura para activar el ciclo de energía nocturna gratuita."
                ]
            elif has_natural_personality:
                patience_change = +15
                interest_change = +20
                reply = "Me interesa la parte de optimización energética. ¿La aplicación de TXU permite configurar alertas de consumo y vincular el termostato inteligente?"
                coach = "Gran sintonía técnica. Destaca la compatibilidad digital y el control en tiempo real desde la aplicación de TXU."
                new_suggestions = [
                    "Totalmente compatible con termostatos inteligentes y con monitoreo en tiempo real desde la app de TXU. ¿Le gustaría probarlo?",
                ]
            elif is_too_long:
                patience_change = -15
                interest_change = -5
                reply = "Demasiada narrativa para un plan de energía. Si no me da especificaciones de la EFL a 1,000 kWh, no me interesa seguir perdiendo el tiempo."
                coach = "Precisión técnica requerida. Enfócate en las métricas de consumo y horarios de Free Nights."
                new_suggestions = [
                    "De 8:00 PM a 6:00 AM energía al 100% gratis todos los días, desglosado en su EFL. ¿Revisamos su factura?",
                ]
            else:
                patience_change = +5
                interest_change = +15
                reply = "¿Y cómo manejan la inyección si en el futuro pongo paneles solares? ¿Tienen medición neta?"
                coach = "Pregunta técnica avanzada. Responde con el plan Free Nights & Solar Days de TXU."
                new_suggestions = [
                    "Con Solar Days le acreditamos la energía solar que genera durante el día y tiene noches gratis. ¿Revisamos su recibo?",
                ]

    # Actualizar estados de la puerta
    door_state["doorbell_rung"] = True
    door_state["patience"] = max(0, min(100, door_state["patience"] + patience_change))
    door_state["interest"] = max(0, min(100, door_state["interest"] + interest_change))
    door_state["turn"] += 1

    # Personalizar feedback del coach para el gancho de apertura inicial
    if is_opening_turn and coach and not coach.startswith("Gancho de apertura:"):
        coach = f"Gancho de apertura: {coach}"

    # Si se completó el gancho de apertura, transicionar sugerencias hacia el guion de profundización
    if is_opening_turn and not new_suggestions:
        new_suggestions = ARCHETYPE_DETAILS[archetype]["suggestions"]

    # Evaluar desenlaces con mayor flexibilidad para el vendedor
    has_closing_signal = bool(re.search(r'(cambi|hacer el cambio|revis|firm|registr|apart|enrol|contrat|paso a las|vemos a las|agend|anot|cita|factura|recibo|tr[aá]mite)', text))
    if not is_opening_turn and door_state["interest"] >= 75 and (has_closing_signal or archetype == "IDEAL_LEAD"):
        door_state["status"] = "SALE_CLOSED"
        if not any(w in reply.lower() for w in ["factura", "trámite", "registro", "cambio", "trato", "enrol"]):
            reply = f"{reply} ¡Me convenció! Vamos a sacar la factura para hacer el cambio a TXU Energy de una vez."
    elif not is_opening_turn and door_state["interest"] >= 55 and (has_closing_signal or has_decision_maker_probe or "cita" in text):
        door_state["status"] = "APPOINTMENT"
        if not any(w in reply.lower() for w in ["cita", "hora", "paso a las", "llega a las", "tarde", "noche", "agenda"]):
            reply = f"{reply} Quedamos entonces en esa hora para revisar la factura con calma."
    elif door_state["patience"] <= 10 or ("portazo" in reply.lower() and door_state["patience"] < 25):
        door_state["status"] = "REJECTED"
        if not ("portazo" in reply.lower() or "cierra" in reply.lower()):
            reply = f"{reply} Ya no me interesa, gracias. [Cierra la puerta]"

    # Agregar intercambios
    door_state["messages"].append({
        "sender": "user",
        "text": user_text,
        "coach": None,
        "patience_change": 0,
        "interest_change": 0,
    })
    door_state["messages"].append({
        "sender": "prospect",
        "text": reply,
        "coach": coach,
        "patience_change": patience_change,
        "interest_change": interest_change,
        "engine": "Motor Local (Reglas)",
    })

    if new_suggestions and door_state["status"] == "IN_PROGRESS":
        door_state["suggestions"] = new_suggestions

    return door_state


def evaluate_response(user_text, door_state):
    """
    Evalúa la respuesta del vendedor.
    Prioridad de procesamiento:
    1. Google Gemini (modelo configurado o variantes flash).
    2. API directa de DeepSeek (si hay saldo y API key).
    3. Modelos gratuitos de OpenRouter.
    4. Motor heurístico local en memoria (fallback autónomo).
    """
    door_state["doorbell_rung"] = True
    llm_result = None
    engine_name = "Motor Local (Reglas)"

    # 1. Intentar con Google Gemini
    try:
        from .gemini_service import generate_gemini_response
        llm_result = generate_gemini_response(user_text, door_state)
        if llm_result:
            engine_name = llm_result.get("engine", "Google Gemini")
            print(f"[Simulator] Respondido por: {engine_name}")
    except Exception as e:
        print(f"[Simulator] Fallback desde Gemini: {e}")

    # 2. Si Gemini no respondió, intentar con DeepSeek oficial
    if not llm_result:
        try:
            from .deepseek_service import generate_deepseek_response
            llm_result = generate_deepseek_response(user_text, door_state)
            if llm_result:
                engine_name = "DeepSeek (deepseek-chat)"
                print(f"[Simulator] Respondido por: {engine_name}")
        except Exception as e:
            print(f"[Simulator] Fallback desde DeepSeek: {e}")

    # 3. Si no, intentar con OpenRouter (modelos gratuitos)
    if not llm_result:
        try:
            from .openrouter_service import generate_llm_response
            llm_result = generate_llm_response(user_text, door_state)
            if llm_result:
                engine_name = "OpenRouter"
                print(f"[Simulator] Respondido por: {engine_name}")
        except Exception as e:
            print(f"[Simulator] Fallback desde OpenRouter: {e}")

    # Si algún servicio LLM devolvió resultado válido
    if llm_result:
        patience_change = llm_result["patience_change"]
        interest_change = llm_result["interest_change"]

        door_state["patience"] = max(0, min(100, door_state["patience"] + patience_change))
        door_state["interest"] = max(0, min(100, door_state["interest"] + interest_change))
        door_state["turn"] += 1
        door_state["status"] = llm_result["status"]

        door_state["messages"].append({
            "sender": "user",
            "text": user_text,
            "coach": None,
            "patience_change": 0,
            "interest_change": 0,
        })
        door_state["messages"].append({
            "sender": "prospect",
            "text": llm_result["reply"],
            "coach": llm_result["coach"],
            "patience_change": patience_change,
            "interest_change": interest_change,
            "engine": engine_name,
        })
        if llm_result.get("suggestions") and door_state["status"] == "IN_PROGRESS":
            door_state["suggestions"] = llm_result["suggestions"]

        return door_state

    # 4. Fallback al motor local
    print("[Simulator] Respondido por: Motor Local (Reglas)")
    return evaluate_response_local(user_text, door_state)
