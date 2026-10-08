"""
i18n_strings.py - Catálogo central de internacionalización bilingüe (Español / Inglés)
para el simulador comercial y de prospección de TXU Energy Smart Door.
Diseñado bajo estándares corporativos senior: CERO EMOJIS, textos profesionales ejecutivos.
"""

UI_STRINGS = {
    'es': {
        'brand_title': 'TXU Energy',
        'brand_subtitle': 'Entrenamiento Comercial Residencial y Retail (Texas)',
        'market_region': 'Texas ERCOT',
        'theme_light': 'Modo Claro',
        'theme_dark': 'Modo Oscuro',
        'theme_title': 'Alternar entre Modo Claro y Modo Oscuro',
        'lang_toggle_title': 'Cambiar idioma entre Español e Inglés',
        'lang_switch_es_title': 'Cambiar a Español',
        'lang_switch_en_title': 'Cambiar a Inglés (Switch to English)',

        # Selector de Modalidad
        'mode_label': 'Modalidad:',
        'mode_random': 'Aleatorio',
        'mode_random_full': 'Aleatorio (Puerta y Tienda)',
        'mode_door': 'Puerta',
        'mode_door_full': 'Puerta a Puerta Residencial',
        'mode_store': 'Tienda',
        'mode_store_full': 'Kiosco Retail en Tienda',

        # Encabezado del Prospecto
        'role_resident': 'Residente',
        'role_shopper': 'Comprador',
        'metric_patience': 'Paciencia',
        'metric_interest': 'Interés',
        'alert_rejection_risk': '¡Riesgo!',
        'alert_closing_opportunity': '¡Cierre!',
        'btn_reset_chat': 'Reiniciar',
        'btn_reset_chat_title': 'Reiniciar interacción actual desde el estado inicial',
        'btn_next_door': 'Siguiente Puerta',
        'btn_next_shopper': 'Abordar Siguiente Comprador',
        'btn_next_title': 'Avanzar al siguiente cliente o prospecto',

        # Barra de Intercomunicador
        'intercom_ready': 'Voz Activa: Listo',
        'intercom_speaking_female': 'Residente (Voz Femenina) hablando...',
        'intercom_speaking_male': 'Residente (Voz Masculina) hablando...',
        'intercom_preparing_audio': 'Preparando audio neuronal...',
        'intercom_listening_prompt': 'Listo para hablar (Tu turno)...',
        'intercom_mic_active_hook': 'Micrófono activo: Presenta tu gancho de apertura',
        'intercom_mic_active_approach': 'Micrófono activo: Presenta tu gancho de abordaje',
        'intercom_doorbell_ringing': 'Timbre sonando...',
        'intercom_store_approach': 'Abordaje iniciado en tienda...',
        'intercom_voice_active': 'Voz Activa',
        'intercom_voice_muted': 'Voz Silenciada',
        'intercom_handsfree_active': 'Manos Libres: Activo',
        'intercom_handsfree_manual': 'Manos Libres: Manual',
        'intercom_handsfree_title': 'Conversación continua automática',
        'intercom_mute_title': 'Silenciar o activar la voz del prospecto',

        # Tarjetas de Llegada Inicial
        'arrival_store_title': 'Llegada al Kiosco de Tienda',
        'arrival_store_desc': 'Aborda al comprador mientras camina hacia la salida o estacionamiento. Tu micrófono se encenderá automáticamente para que lances tu gancho de abordaje.',
        'arrival_store_btn': 'Abordar Comprador para Iniciar',
        'arrival_store_heading_prefix': 'Estás en la tienda viendo pasar a',
        'arrival_store_badge': 'Kiosco en Tienda',
        'arrival_porch_title': 'Llegada al Pórtico Residencial',
        'arrival_porch_desc': 'Toca el timbre para avisar al residente. Tu micrófono se encenderá automáticamente y tú hablarás primero con tu gancho de apertura o rompehielos.',
        'arrival_porch_btn': 'Tocar Timbre para Iniciar',
        'arrival_porch_heading_prefix': 'Estás frente a la residencia de',
        'arrival_porch_badge_prefix': 'Llegada al pórtico • Puerta #',
        'observation_shopper_label': 'Observación del comprador:',
        'observation_porch_label': 'Observación en la entrada:',
        'waiting_store_title': 'Abordaje en Vivo • Micrófono Activo',
        'waiting_store_desc': 'El comprador te está mirando. Habla ahora por el micrófono o envía tu gancho de abordaje.',
        'waiting_door_title': 'Timbre Activado • Micrófono en Vivo',
        'waiting_door_desc': 'El residente se acerca a la puerta. Habla ahora por el micrófono o envía tu gancho de apertura.',
        'status_closed_title': 'Venta Cerrada con Éxito',
        'status_closed_desc': 'Lograste conectar con la necesidad del residente, superaste las dudas sobre su tarifa de luz y aseguraste el registro del plan TXU Energy.',
        'status_apt_title': 'Cita Comercial Asegurada',
        'status_apt_desc': 'Estableciste un horario formal para revisar la factura de luz completa con los tomadores de decisión.',
        'status_rejected_title': 'Contacto Concluido',
        'status_rejected_desc': 'El prospecto concluyó el contacto. En venta directa el rechazo es parte natural del proceso. Aplica el aprendizaje en la próxima oportunidad.',
        'mic_btn_title': 'Activar micrófono para hablar',
        'analytics_evaluation_prefix': 'Evaluación objetiva de competencias en diálogo con',

        # Mensajes de Chat
        'speaker_listen_tooltip': 'Escuchar respuesta en voz alta',
        'coach_title': 'Análisis del Coach Comercial',
        'coach_rule_engine': 'Motor Local (Reglas)',
        'coach_gemini': 'Google Gemini',
        'sender_advisor': 'Tú (Asesor de Energía TXU)',
        'sender_prospect': 'Cliente',

        # Popover de Pistas
        'hints_btn': 'Pistas',
        'hints_title_hooks': 'Ganchos de apertura recomendados',
        'hints_title_approach': 'Ganchos de abordaje recomendados',
        'hints_title_tactics': 'Pistas tácticas recomendadas',
        'hints_desc': 'Haz clic en una sugerencia para enviarla directamente o utilízala como guía para tu respuesta:',
        'hints_toggle_title': 'Ver u ocultar sugerencias tácticas',

        # Pie de Entrada
        'btn_evaluate': 'Concluir y Evaluar',
        'btn_evaluate_title': 'Finalizar interacción actual y generar reporte analítico de desempeño',
        'input_placeholder_initial_door': 'Toca el timbre o escribe tu gancho de apertura...',
        'input_placeholder_initial_store': 'Aborda al comprador o escribe tu gancho...',
        'input_placeholder_active': 'Hable por el micrófono o escriba con su propio estilo y palabras...',
        'btn_send': 'Enviar',
        'session_completed_notice': 'Interacción finalizada. Revisa el informe analítico de desempeño superior antes de continuar.',

        # Reporte Analítico
        'analytics_summary_title': 'Informe Analítico de Desempeño Comercial',
        'analytics_score_label': 'Puntaje Global',
        'analytics_competencies_title': 'Evaluación de Competencias Clave',
        'analytics_strengths_title': 'Fortalezas Demostradas en la Sesión',
        'analytics_improvements_title': 'Áreas de Mejora Prioritarias (Sales Coach)',
        'analytics_metrics_title': 'Métricas Registradas de la Interacción',
        'analytics_metric_turns': 'Turnos de Diálogo',
        'analytics_metric_patience_delta': 'Variación de Paciencia',
        'analytics_metric_interest_delta': 'Variación de Interés',
        'analytics_metric_final_interest': 'Interés Final del Cliente',
        'analytics_btn_retry': 'Practicar de Nuevo con este Prospecto',
        'analytics_btn_continue_door': 'Continuar a la Siguiente Puerta',
        'analytics_btn_continue_shopper': 'Abordar Siguiente Comprador',

        # Indicador de Pensamiento
        'thinking_indicator': 'Escuchando propuesta y procesando objeción...',
        'connection_error': 'No se pudo obtener respuesta del modelo. Verifique la conexión o intente nuevamente.',
    },
    'en': {
        'brand_title': 'TXU Energy',
        'brand_subtitle': 'Residential & Retail Sales Training (Texas)',
        'market_region': 'Texas ERCOT',
        'theme_light': 'Light Mode',
        'theme_dark': 'Dark Mode',
        'theme_title': 'Toggle between Light and Dark Mode',
        'lang_toggle_title': 'Switch language between English and Spanish',
        'lang_switch_es_title': 'Switch to Spanish (Cambiar a Español)',
        'lang_switch_en_title': 'Switch to English',

        # Prospecting Mode Selector
        'mode_label': 'Mode:',
        'mode_random': 'Random',
        'mode_random_full': 'Random (Door & Store)',
        'mode_door': 'Door',
        'mode_door_full': 'Residential Door to Door',
        'mode_store': 'Store',
        'mode_store_full': 'Retail Store Kiosk',

        # Prospect Header
        'role_resident': 'Resident',
        'role_shopper': 'Shopper',
        'metric_patience': 'Patience',
        'metric_interest': 'Interest',
        'alert_rejection_risk': 'Risk!',
        'alert_closing_opportunity': 'Closing!',
        'btn_reset_chat': 'Restart',
        'btn_reset_chat_title': 'Restart current interaction from initial state',
        'btn_next_door': 'Next Door',
        'btn_next_shopper': 'Approach Next Shopper',
        'btn_next_title': 'Advance to next customer or prospect',

        # Intercom Bar
        'intercom_ready': 'Voice Active: Ready',
        'intercom_speaking_female': 'Resident (Female Voice) speaking...',
        'intercom_speaking_male': 'Resident (Male Voice) speaking...',
        'intercom_preparing_audio': 'Preparing neural audio...',
        'intercom_listening_prompt': 'Ready to speak (Your turn)...',
        'intercom_mic_active_hook': 'Mic active: Deliver your opening hook',
        'intercom_mic_active_approach': 'Mic active: Deliver your approach hook',
        'intercom_doorbell_ringing': 'Doorbell ringing...',
        'intercom_store_approach': 'Store approach started...',
        'intercom_voice_active': 'Voice Active',
        'intercom_voice_muted': 'Voice Muted',
        'intercom_handsfree_active': 'Hands-Free: Active',
        'intercom_handsfree_manual': 'Hands-Free: Manual',
        'intercom_handsfree_title': 'Continuous automatic conversation',
        'intercom_mute_title': 'Mute or activate prospect voice',

        # Initial Arrival Cards
        'arrival_store_title': 'Arrival at Store Kiosk',
        'arrival_store_desc': 'Approach the shopper as they walk toward the exit or parking lot. Your microphone will turn on automatically for your approach hook.',
        'arrival_store_btn': 'Approach Shopper to Start',
        'arrival_store_heading_prefix': 'You are at the store seeing',
        'arrival_store_badge': 'Store Kiosk',
        'arrival_porch_title': 'Arrival at Residential Porch',
        'arrival_porch_desc': 'Ring the doorbell to notify the resident. Your microphone will turn on automatically and you will speak first with your opening hook or icebreaker.',
        'arrival_porch_btn': 'Ring Doorbell to Start',
        'arrival_porch_heading_prefix': 'You are at the residence of',
        'arrival_porch_badge_prefix': 'Porch arrival • Door #',
        'observation_shopper_label': 'Shopper observation:',
        'observation_porch_label': 'Porch observation:',
        'waiting_store_title': 'Live Approach • Microphone Active',
        'waiting_store_desc': 'The shopper is looking at you. Speak into the microphone now or send your approach hook.',
        'waiting_door_title': 'Doorbell Activated • Microphone Live',
        'waiting_door_desc': 'The resident is approaching the door. Speak into the microphone now or send your opening hook.',
        'status_closed_title': 'Sale Successfully Closed',
        'status_closed_desc': 'You successfully connected with the customer\'s need, addressed electricity rate concerns, and secured the TXU Energy plan enrollment.',
        'status_apt_title': 'Commercial Appointment Secured',
        'status_apt_desc': 'You set a formal appointment to review the complete electric bill with the decision makers.',
        'status_rejected_title': 'Contact Concluded',
        'status_rejected_desc': 'The prospect concluded the contact. In direct sales, rejection is a natural part of the process. Apply the learnings to your next opportunity.',
        'mic_btn_title': 'Activate microphone to speak',
        'analytics_evaluation_prefix': 'Objective competency evaluation in dialogue with',

        # Chat Messages
        'speaker_listen_tooltip': 'Listen to response aloud',
        'coach_title': 'Sales Coach Critique',
        'coach_rule_engine': 'Local Engine (Rules)',
        'coach_gemini': 'Google Gemini',
        'sender_advisor': 'You (TXU Energy Advisor)',
        'sender_prospect': 'Customer',

        # Hints Popover
        'hints_btn': 'Hints',
        'hints_title_hooks': 'Recommended opening hooks',
        'hints_title_approach': 'Recommended approach hooks',
        'hints_title_tactics': 'Recommended tactical hints',
        'hints_desc': 'Click a hint to send it directly or use it as a guide for your spoken response:',
        'hints_toggle_title': 'View or hide tactical hints',

        # Footer Input
        'btn_evaluate': 'Conclude & Evaluate',
        'btn_evaluate_title': 'Finish current interaction and generate analytical performance report',
        'input_placeholder_initial_door': 'Ring the doorbell or type your opening hook...',
        'input_placeholder_initial_store': 'Approach the shopper or type your hook...',
        'input_placeholder_active': 'Speak through the microphone or type in your own style and words...',
        'btn_send': 'Send',
        'session_completed_notice': 'Interaction finished. Review the analytical performance report above before continuing.',

        # Analytical Report
        'analytics_summary_title': 'Commercial Performance Analytical Report',
        'analytics_score_label': 'Overall Score',
        'analytics_competencies_title': 'Key Competencies Evaluation',
        'analytics_strengths_title': 'Demonstrated Strengths in Session',
        'analytics_improvements_title': 'Priority Areas for Improvement (Sales Coach)',
        'analytics_metrics_title': 'Recorded Interaction Metrics',
        'analytics_metric_turns': 'Dialogue Turns',
        'analytics_metric_patience_delta': 'Patience Net Change',
        'analytics_metric_interest_delta': 'Interest Net Change',
        'analytics_metric_final_interest': 'Customer Final Interest',
        'analytics_btn_retry': 'Practice Again with this Prospect',
        'analytics_btn_continue_door': 'Continue to Next Door',
        'analytics_btn_continue_shopper': 'Approach Next Shopper',

        # Thinking Indicator
        'thinking_indicator': 'Listening to proposal and processing objection...',
        'connection_error': 'Could not obtain response from model. Please verify connection or try again.',
    }
}


ARCHETYPE_DETAILS_I18N = {
    'es': {
        "BUSY": {
            "title": "El Ocupado (Prisa con el A/C)",
            "description": "Tiene prisa evidente y va de salida. Valora la brevedad, empatía y respetar su tiempo.",
            "porch_observation": "Llaves del auto en mano, portafolio y mirada atenta al reloj.",
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
            "initial_message": "Menos mal que pasa alguien de energía. El mes pasado el recibo se me fue a $420 dólares con el calor. ¿Ustedes tienen tarifas fijas que no suban?",
            "opening_hooks": [
                "Buenas tardes vecino, exactamente para eso estamos pasando hoy: muchos vecinos tuvieron el mismo susto de más de $400 por tarifas variables.",
                "Hola vecino, buenas tardes. Qué bueno que lo menciona; el plan Season Pass de TXU le da 50% de descuento automático en verano e invierno.",
                "Buenas tardes. TXU Energy le congela su precio con tarifa fija protegida y le entregamos un comparativo sin compromiso ahora mismo."
            ],
            "suggestions": [
                "Comprendo perfectamente su frustración, pagar $420 por el calor es un golpe durísimo. Con TXU Energy le aseguramos una tarifa fija protegida por 24 meses y 50% de descuento en verano con Season Pass. Si me permite ver cuántos kWh consumió, le calculo su ahorro en 1 minuto.",
                "Sí, claro, somos los más baratos de Texas, fírmeme aquí de una vez y le cambio el medidor.",
                "Eso le pasa por no fijarse en la fecha de vencimiento de su contrato anterior."
            ]
        },
        "BARGAIN_HUNTER": {
            "title": "El Cazador de Ofertas (Compara Tarifas)",
            "description": "Analítico, revisa centavos por kWh y la etiqueta EFL. Valora transparencia y créditos de factura.",
            "porch_observation": "Gafas de lectura en mano y calculadora en la mesa del recibidor.",
            "initial_message": "Mire, yo pago 13.8 centavos por kWh con mi proveedor actual. Si no me ofrece menos de 13 centavos todo incluido, no tiene caso hablar.",
            "opening_hooks": [
                "Buenas tardes caballero, me alegra hablar con alguien que conoce sus números. En TXU desglosamos el cargo base y la tarifa TDU de Oncor con total claridad.",
                "Hola, buenas tardes. Más allá del centavo por kWh, el plan Clear Deal de TXU le otorga un crédito de $30 dólares cada mes en que consuma más de 1,000 kWh.",
                "Buenas tardes vecino. Con gusto revisamos su EFL para ver si esos 13.8 centavos incluyen la entrega de Oncor o tienen cargos ocultos."
            ],
            "suggestions": [
                "Excelente que conozca su tarifa exacta; pocos clientes revisan la EFL con tanto detalle. Con el plan Clear Deal de TXU tiene crédito automático de $30 dólares cada mes al superar 1,000 kWh, lo que baja su costo promedio efectivo. ¿Cuántos kWh consume típicamente en verano?",
                "Nosotros le dejamos el centavo en 10 centavos garantizado sin importar los cargos de Oncor.",
                "Las matemáticas de los otros proveedores son engañosas y le están robando dinero."
            ]
        },
        "LOYALIST": {
            "title": "El Cliente Fiel (Años con la Competencia)",
            "description": "Lleva 10+ años con Reliant o Direct Energy por inercia. Valora que Oncor mantiene los mismos postes y cables.",
            "porch_observation": "Calcomanía de su proveedor actual visible en el medidor; actitud tranquila pero arraigada.",
            "initial_message": "No joven, gracias. Llevo 12 años con Reliant Energy y nunca me han fallado, no tengo motivos para cambiarme a TXU.",
            "opening_hooks": [
                "Buenas tardes señor, es muy respetable su lealtad de 12 años con Reliant; de hecho, la luz sigue llegando por los mismos cables de Oncor.",
                "Hola, buenas tardes. Precisamente a los clientes con más de 10 años en su compañía los visitamos porque casi siempre tienen tarifas desactualizadas.",
                "Buenas tardes vecino. No le pido que cancele nada hoy; solo le muestro en 1 minuto cómo se compara su tarifa actual con el 50% de descuento de TXU."
            ],
            "suggestions": [
                "Respeto profundamente su lealtad de 12 años, señor; demuestra lo importante que es la estabilidad para su hogar. La buena noticia es que Oncor sigue manteniendo los mismos cables y postes sin importar el proveedor. La diferencia es que los clientes antiguos suelen pagar tarifas altas por renovación automática. ¿Cuándo fue la última vez que revisó su precio por kWh?",
                "Reliant es una pésima compañía y le está cobrando de más solo por confiado.",
                "Si no cambia a TXU hoy mismo se va a arrepentir cuando llegue la factura de agosto."
            ]
        },
        "TECH_SAVVY": {
            "title": "El Tecnológico (Dueño de Auto Eléctrico)",
            "description": "Tiene auto eléctrico, termostato Nest o paneles. Le atraen Free Nights y herramientas digitales.",
            "porch_observation": "Cargador de auto eléctrico en la cochera y timbre inteligente con cámara Google Nest.",
            "initial_message": "Tengo auto eléctrico y cargo de noche, además controlo los termostatos inteligentes. ¿Tienen planes que realmente aprovechen eso?",
            "opening_hooks": [
                "Buenas tardes caballero, vi el cargador en la cochera; precisamente venimos informando del plan Free Nights de TXU Energy con electricidad 100% gratis de 8 PM a 6 AM.",
                "Hola, buenas tardes. Para usuarios con alta tecnología y vehículo eléctrico, TXU tiene compatibilidad total y energía gratuita toda la noche.",
                "Buenas tardes vecino. Si carga su auto después de las 8 de la noche, con TXU Energy el costo de cargar su batería es literalmente $0 dólares.",
            ],
            "suggestions": [
                "Exactamente para su perfil fue diseñado el plan Free Nights de TXU Energy: toda la electricidad que consuma de 8 PM a 6 AM es 100% gratuita, incluyendo la carga de su auto y el aire acondicionado nocturno. Además, nuestra app móvil le permite programar y monitorear su consumo hora por hora. ¿A qué hora suele conectar su vehículo?",
                "El auto eléctrico gasta muchísima luz y va a fundir el transformador de la cuadra.",
                "Nuestros planes son normales, pero le podemos regalar una tarjeta de regalo si firma hoy."
            ]
        },
        "NON_DECISION_MAKER": {
            "title": "El Inquilino (No Toma Decisiones)",
            "description": "Renta la casa o la cuenta está a nombre de otra persona. Busca no comprometerse.",
            "porch_observation": "Joven o familiar que atiende la puerta mirando hacia adentro.",
            "initial_message": "Yo solo rento aquí con unos amigos y el contrato de luz está a nombre del dueño de la casa. No puedo hacer ningún cambio.",
            "opening_hooks": [
                "Buenas tardes vecina, comprendo perfectamente. ¿Ustedes pagan la luz directamente o viene incluida en la renta?",
                "Hola, buenas tardes. Para los inquilinos que pagan su recibo tenemos planes sin depósito y sin verificación de crédito rígida.",
                "Buenas tardes. Si pagan la factura entre ustedes, les conviene avisarle al dueño del 50% de descuento de verano de TXU."
            ],
            "suggestions": [
                "Entiendo perfectamente, gracias por aclarármelo. Si ustedes pagan el recibo de luz cada mes, al dueño le conviene que el costo baje para que no haya retrasos. ¿Sabe cuándo vence el contrato actual o a qué teléfono puedo saludar al titular de la cuenta?",
                "Fírmeme usted el contrato, el dueño ni cuenta se va a dar del cambio de compañía.",
                "Entonces no me haga perder el tiempo, llámeme al dueño de inmediato."
            ]
        }
    },
    'en': {
        "BUSY": {
            "title": "The Busy Homeowner (In a Hurry with the A/C)",
            "description": "Clearly in a rush and on the way out. Values brevity, empathy, and respect for their time.",
            "porch_observation": "Car keys in hand, briefcase, and frequently checking their watch.",
            "initial_message": "Please make it quick, I'm heading out the door for work. In this Texas heat nobody wants to stand on the porch. What can I do for you?",
            "opening_hooks": [
                "Good afternoon neighbor, sorry for the quick interruption: I only need 15 seconds before you leave to share TXU's 50% summer discount.",
                "Hello, good afternoon. I know you're in a hurry, just one quick question: what time this evening can I catch you for 2 minutes to review your bill?",
                "Good afternoon neighbor. I noticed the A/C units running full blast; with this Texas heat we wanted to notify you about TXU's savings program."
            ],
            "suggestions": [
                "Just 15 seconds on your way out: in this heat, A/C bills skyrocket. TXU gives you 50% off during summer with Season Pass. How much was your last bill?",
                "I know you're in a hurry. What time this evening would be best to share a 2-minute bill comparison?",
                "I am here to explain the full history of Texas electric deregulation and all kilowatt options."
            ]
        },
        "SKEPTICAL": {
            "title": "The Skeptical Homeowner (Fears Slamming)",
            "description": "Fears scams and unauthorized provider switching (slamming). Opens up if caution is validated and official badge is shown.",
            "porch_observation": "Cracks the door open with the security chain on; cautiously observing through the peephole.",
            "initial_message": "Who are you? I don't show my electric bill to anyone at my door, there are too many scammers switching contracts without permission.",
            "opening_hooks": [
                "Good afternoon neighbor, my name is an official TXU Energy advisor, here is my badge. I know caution is high with scams in Texas; I am not asking for personal info.",
                "Hello neighbor, sorry to bother you. First of all, here is my official company ID; we are just checking if your neighbors have locked in their rates against summer spikes.",
                "Good afternoon. As a careful homeowner, you do well verifying who knocks on your door; we are directly from TXU Energy with protected fixed rates."
            ],
            "suggestions": [
                "You are 100% right and smart to protect yourself; never share your ESI ID number with strangers. I am an official TXU Energy advisor, here is my badge. I'm not asking for your bill today, just one question: is your current rate fixed or variable?",
                "I am an official representative, look at my badge, you have nothing to distrust.",
                "We helped your next-door neighbors lock in a fixed-cent rate to shield themselves from summer market spikes."
            ]
        },
        "POLITE_EVASIVE": {
            "title": "The Polite Evasive Homeowner",
            "description": "Friendly and smiling, attempts to exit by requesting a flyer. Responds well to diagnostic questions about summer power usage.",
            "porch_observation": "Friendly smile but body oriented towards the inside of the home.",
            "initial_message": "Good afternoon! What you have from TXU sounds interesting, but I'm quite busy right now. Why don't you leave a flyer and if I'm interested I'll call?",
            "opening_hooks": [
                "Good afternoon neighbor, sorry to interrupt for a moment. We are checking in with homes on this street regarding the impact of A/C on summer bills.",
                "Hello neighbor, great to greet you. Quick question before leaving any paper information: does your electric bill typically exceed $200 in the hot months?",
                "Good afternoon, just a quick 30-second inquiry regarding TXU Energy's summer discount program for homes on this block."
            ],
            "suggestions": [
                "I would be glad to leave one. Just so I leave the right information: does your electricity bill usually exceed $250 in July and August?",
                "Sure thing, here is the flyer. It has the TXU Energy phone number whenever you feel like calling.",
                "Company policy does not allow me to leave flyers; I need you to listen to me right now."
            ]
        },
        "HOSTILE": {
            "title": "The Hostile Prospect",
            "description": "Irritable and defensive due to extreme heat or solicitors. Disarmed with genuine respect, sincere apologies, and empathy.",
            "porch_observation": "Tense facial expression and sweat on forehead from heat; holding the door firmly.",
            "initial_message": "Knocking on the door again! With 100-degree heat outside, the last thing I want is people bothering me about electricity. I'm not interested in anything!",
            "opening_hooks": [
                "Good afternoon sir, sincere apologies for knocking on your door in this 100-degree heat. I just wanted to leave a respectful greeting from TXU Energy.",
                "Hello, good afternoon. I know it's frustrating having someone knock at this hour; I promise to be extremely brief if you grant me just 20 seconds.",
                "Good afternoon neighbor, sorry to interrupt your rest. I will step away immediately if you are busy, we were just checking service reliability on this block."
            ],
            "suggestions": [
                "You are completely right sir, sincere apologies for interrupting you. In this brutal heat nobody wants their door knocked on. I'll step away right now, have a wonderful afternoon.",
                "Calm down sir, do not get upset over nothing, I am just here to offer a TXU rate that will benefit you.",
                "The sidewalk is public property and I am simply doing my job for TXU Energy."
            ]
        },
        "IDEAL_LEAD": {
            "title": "The Qualified Lead (Electric Bill Spike)",
            "description": "Their previous fixed contract expired and variable rates spiked their bill; seeking immediate relief and price protection.",
            "porch_observation": "Opened mail envelope in hand with visible electricity bill statement.",
            "initial_message": "Thank goodness someone from energy stopped by. Last month my electric bill jumped to $420 with this heat wave. Do you have fixed rates that won't surge?",
            "opening_hooks": [
                "Good afternoon neighbor, that is exactly why we are in the neighborhood today: several neighbors had that exact same shock over $400 due to variable rates.",
                "Hello neighbor, good afternoon. I'm glad you brought that up; TXU's Season Pass plan gives you an automatic 50% discount across summer and winter.",
                "Good afternoon. TXU Energy freezes your price with protected fixed rates and we can provide a no-obligation comparison right now."
            ],
            "suggestions": [
                "I completely understand your frustration, paying $420 because of the Texas heat is a heavy hit. With TXU Energy we lock in a protected fixed rate for 24 months plus 50% off summer electricity with Season Pass. If you allow me to check your kWh usage, I can calculate your exact savings in 1 minute.",
                "Yes of course, we are the cheapest in Texas, just sign right here and I'll switch your meter.",
                "That happened to you because you didn't pay attention to your contract expiration date."
            ]
        },
        "BARGAIN_HUNTER": {
            "title": "The Bargain Hunter (Comparing Rates)",
            "description": "Analytical, scrutinizes cents per kWh and the EFL sheet. Values transparency and bill credits.",
            "porch_observation": "Reading glasses in hand and calculator visible on the entryway table.",
            "initial_message": "Look, I pay 13.8 cents per kWh with my current provider. If you can't offer under 13 cents all-inclusive, there's no point in talking.",
            "opening_hooks": [
                "Good afternoon sir, I appreciate talking with someone who knows their exact numbers. At TXU we clearly itemize the base charge and Oncor TDU delivery fees.",
                "Hello, good afternoon. Beyond the cent per kWh, TXU's Clear Deal plan provides a $30 bill credit every single month you use over 1,000 kWh.",
                "Good afternoon neighbor. We would be happy to review your EFL to see if that 13.8 cents includes Oncor delivery or has hidden tiered charges."
            ],
            "suggestions": [
                "It's great that you know your exact rate; very few customers review the EFL sheet in detail. With TXU's Clear Deal plan you get an automatic $30 credit every month you exceed 1,000 kWh, lowering your effective average cost. How many kWh do you typically use in the summer?",
                "We can guarantee 10 cents flat regardless of Oncor delivery charges.",
                "Other providers' math is deceptive and they are taking your money."
            ]
        },
        "LOYALIST": {
            "title": "The Brand Loyalist (Years with Competitor)",
            "description": "10+ years with Reliant or Direct Energy by inertia. Values knowing that Oncor maintains the exact same lines and poles.",
            "porch_observation": "Current provider logo sticker visible on the electric meter; calm but deeply entrenched attitude.",
            "initial_message": "No thanks, young man. I've been with Reliant Energy for 12 years and they've never let me down. I have no reason to switch to TXU.",
            "opening_hooks": [
                "Good afternoon sir, your 12-year loyalty with Reliant is very respectable; electricity still delivers across the exact same Oncor power lines.",
                "Hello, good afternoon. We specifically visit homeowners with 10+ years with their company because long-term accounts often sit on outdated renewal rates.",
                "Good afternoon neighbor. I'm not asking you to cancel anything today; I can simply show you in 1 minute how your current rate compares to TXU's 50% discount."
            ],
            "suggestions": [
                "I deeply respect your 12 years of loyalty, sir; it proves how much household stability matters to you. The great news is that Oncor continues maintaining the exact same wires and poles regardless of provider. The difference is that long-term legacy accounts often pay higher rates on automatic renewals. When was the last time you checked your price per kWh?",
                "Reliant is a terrible company and they are overcharging you because you trust them blindly.",
                "If you don't switch to TXU today you're going to regret it when your August bill arrives."
            ]
        },
        "TECH_SAVVY": {
            "title": "The Tech Savvy Homeowner (EV Owner)",
            "description": "Drives an EV, uses Nest thermostat or solar. Attracted to Free Nights and real-time app insights.",
            "porch_observation": "EV level-2 charger in the garage and Google Nest smart doorbell camera.",
            "initial_message": "I drive an EV and charge overnight, plus I control smart thermostats. Do you have plans that actually take advantage of that?",
            "opening_hooks": [
                "Good afternoon sir, I noticed the EV charger in the garage; we are sharing information on TXU Energy's Free Nights plan with 100% free power from 8 PM to 6 AM.",
                "Hello, good afternoon. For high-tech smart homes and EV drivers, TXU offers seamless compatibility and zero energy charges all night long.",
                "Good afternoon neighbor. If you charge your EV after 8 PM, with TXU Energy the cost to charge your vehicle battery is literally $0."
            ],
            "suggestions": [
                "TXU Energy's Free Nights plan was designed specifically for your setup: all electricity used between 8 PM and 6 AM is 100% free, including your EV charging and nighttime A/C. Plus, our mobile app tracks and schedules your hourly usage. What time do you usually plug in your car?",
                "Electric vehicles pull way too much power and will blow out the neighborhood transformer.",
                "Our plans are standard, but we can give you a gift card if you sign up today."
            ]
        },
        "NON_DECISION_MAKER": {
            "title": "The Non-Decision Maker (Tenant / Roommate)",
            "description": "Renting the home or the electricity bill is under someone else's name. Avoids commitments.",
            "porch_observation": "Young adult or relative answering the door looking back inside.",
            "initial_message": "I just rent here with roommates and the electric bill is under the landlord's name. I can't authorize any changes.",
            "opening_hooks": [
                "Good afternoon neighbor, I completely understand. Do you all pay the electric bill directly or is it bundled into your rent?",
                "Hello, good afternoon. For tenants who split their power bill, we have zero-deposit plans without rigid credit checks.",
                "Good afternoon. If you pay the power bill among yourselves, your landlord would love to know about TXU's 50% summer discount."
            ],
            "suggestions": [
                "I understand completely, thank you for clarifying. If you all pay the electricity bill each month, the landlord benefits from lower utility costs. Do you happen to know when the current contract renews, or is there a number where I can reach the account holder?",
                "Just sign the contract for me, the landlord will never even notice the provider switch.",
                "Then please don't waste my time, call the landlord right now."
            ]
        }
    }
}


RETAIL_SHOPPERS_I18N = {
    'es': {
        "Guillermo Lozano": {
            "role": "Comprador con prisa / Carrito con hielo en H-E-B",
            "location": "H-E-B Frisco - Puerta de Salida",
            "store_observation": "Lleva un carrito lleno de víveres, dos bolsas de hielo derritiéndose y las llaves de la camioneta en la mano.",
            "opening_hooks": [
                "¡Buenas tardes caballero! Solo 10 segundos antes de subir el mandado al auto: ¿su recibo de luz subió con este calor?",
                "Buenas tardes vecino, no le detengo el paso: TXU le da 50% de descuento en luz en verano para compensar el gasto del súper.",
                "¡Hola! Rápido mientras camina al coche: ¿cuánto pagó de electricidad el mes pasado con el aire al máximo?"
            ]
        },
        "Marcela Beltrán": {
            "role": "Madre de familia / Saliendo de compras en Walmart",
            "location": "Walmart Supercenter Dallas - Salida de Cajas",
            "store_observation": "Revisando el ticket de compra largo en la mano y atenta a las promociones de la entrada.",
            "opening_hooks": [
                "¡Buenas tardes! Estamos comparando centavos por kilovatio directo de la etiqueta EFL para que ahorre en la luz.",
                "Hola vecina, si su recibo supera 1,000 kWh en verano, TXU le da $30 de crédito automático en factura cada mes.",
                "Buenas tardes, ¿a cuántos centavos le están cobrando el kWh actualmente en su compañía de luz?"
            ]
        },
        "Arturo Cavazos": {
            "role": "Contratista independiente / Home Depot",
            "location": "Home Depot Arlington - Entrada Principal",
            "store_observation": "Caminando a paso firme hacia la entrada de herramientas con gorra de trabajo; esquiva la mirada hacia el kiosco.",
            "opening_hooks": [
                "Buenas tardes caballero, somos módulo oficial certificado de TXU Energy dentro de la tienda, no pedimos firmas ni cuentas hoy.",
                "Hola, buenas tardes. Con total transparencia en pantalla le comparamos si su tarifa de luz actual está protegida contra apagones.",
                "Buenas tardes, disculpe. Solo una consulta rápida para clientes de Home Depot: ¿su tarifa de luz comercial o residencial es fija o variable?"
            ]
        },
        "Laura Cárdenas": {
            "role": "Compradora en Fiesta Mart / Busca tarjeta de regalo",
            "location": "Fiesta Mart Fort Worth - Entrada Principal",
            "store_observation": "Se detiene un segundo con curiosidad frente al letrero de 'Gana una Gift Card de $50 con TXU Energy'.",
            "opening_hooks": [
                "¡Buenas tardes vecina! Si revisamos su tarifa de luz de verano en 2 minutos se lleva una tarjeta de regalo de $50 de la tienda.",
                "Hola, buenas tardes. ¿Cuánto le cobraron de pura luz el mes pasado con el aire acondicionado al tope?",
                "Buenas tardes vecina, en el kiosco oficial de TXU estamos activando 50% de descuento en luz para los clientes de Fiesta Mart."
            ]
        },
        "Samuel Elizondo": {
            "role": "Profesionista / Lleva app de su proveedor en el celular",
            "location": "Kroger Plano - Pasillo de Salida",
            "store_observation": "Esperando a su acompañante junto a la salida mientras revisa notificaciones en su smartphone.",
            "opening_hooks": [
                "Buenas tardes caballero. Noté que usa su smartphone, ¿en la app de su luz tiene monitoreo de consumo en tiempo real?",
                "Hola, buenas tardes. Para usuarios con tecnología en casa o auto eléctrico, TXU tiene el plan Free Nights con luz gratis de 8 PM a 6 AM.",
                "Buenas tardes. ¿Ya conoce la garantía de tarifa protegida de TXU Energy para blindar su consumo inteligente este verano?"
            ]
        },
        "Gloria Hinojosa": {
            "role": "Jubilada en H-E-B / Fiel a Reliant Energy",
            "location": "H-E-B Houston - Puerta Principal",
            "store_observation": "Caminando despacio con su bolsa de compras reutilizable; sonríe amablemente pero sigue de largo.",
            "opening_hooks": [
                "Buenas tardes señora, qué gusto verla en H-E-B. Representamos a TXU Energy informando que Oncor mantiene los mismos postes pero con tarifas más económicas.",
                "Hola, buenas tardes. Muchos clientes que llevaban años con Reliant se sorprendieron al ver cuánto podían ahorrar cambiando a TXU.",
                "Buenas tardes. Respetamos mucho su lealtad con su proveedor actual; solo le mostramos en 1 minuto si su precio está actualizado."
            ]
        },
        "Rodrigo Paredes": {
            "role": "Joven universitario / Acompaña a sus padres",
            "location": "Walmart Supercenter Garland - Salida de Cajas",
            "store_observation": "Empujando el carrito con refrescos mientras sus familiares pagan en la caja de autoservicio.",
            "opening_hooks": [
                "¡Buenas tardes! Vengo de TXU Energy con información importante sobre el subsidio de verano en la electricidad para el hogar.",
                "Hola, buenas tardes. ¿Quién en su casa se encarga de revisar los recibos de la luz para entregarle un comparativo breve de ahorro?",
                "Buenas tardes. Estamos entregando cupones de descuento para el recibo de luz familiar, ¿quién suele administrar la cuenta en casa?"
            ]
        },
        "Verónica Trejo": {
            "role": "Compradora evasiva / Lleva prisa para subir al auto",
            "location": "Costco Wholesale Irving - Entrada Principal",
            "store_observation": "Lleva gafas de sol puestas y paquetes en el carrito; saluda cordialmente con una sonrisa pero no frena el paso.",
            "opening_hooks": [
                "Buenas tardes vecina, disculpe que la interrumpa un momento. Solo una consulta breve antes de que guarde sus compras en el auto.",
                "Hola vecina, qué gusto saludarla. Rápido, en 15 segundos: ¿su factura de luz suele superar los $200 dólares en los meses de calor?",
                "Buenas tardes, tenemos un folleto con cupón de ahorro de TXU Energy para socios de la tienda, ¿gusta que se lo entregue con una comparativa?"
            ]
        },
        "Ernesto Macías": {
            "role": "Comprador irritable / Molesto por promotores de pasillo",
            "location": "Walmart Supercenter Dallas - Entrada de Abarrotes",
            "store_observation": "Cruza la salida resoplando por el calor que entra por las puertas automáticas; frunce el ceño al notar el módulo comercial.",
            "opening_hooks": [
                "Buenas tardes señor, una disculpa sincera por la interrupción. Solo un saludo respetuoso del módulo de TXU Energy en la tienda.",
                "Hola, buenas tardes. No lo detengo para nada señor, solo desearle buen provecho y excelente camino a casa.",
                "Buenas tardes caballero, con permiso. Con este calorón afuera solo pasamos a recordarles que TXU mantiene las tarifas protegidas."
            ]
        }
    },
    'en': {
        "Guillermo Lozano": {
            "role": "Hurried Shopper / Cart with melting ice at H-E-B",
            "location": "H-E-B Frisco - Exit Doors",
            "store_observation": "Pushing a cart loaded with groceries, two melting bags of ice, and truck keys in hand.",
            "opening_hooks": [
                "Good afternoon sir! Just 10 seconds before loading your groceries: did your electric bill surge with this heat?",
                "Good afternoon neighbor, I won't slow your pace: TXU offers 50% off summer power to offset high grocery costs.",
                "Hello! Quick question on your way to the truck: how much did you pay for electricity last month running A/C non-stop?"
            ]
        },
        "Marcela Beltrán": {
            "role": "Family Mother / Finishing shopping at Walmart",
            "location": "Walmart Supercenter Dallas - Checkout Exit",
            "store_observation": "Reviewing a long receipt in hand while checking out promotions near the store exit.",
            "opening_hooks": [
                "Good afternoon! We are comparing cents per kWh straight from the EFL sheet to help you save on electricity.",
                "Hello neighbor, if your household uses over 1,000 kWh in summer, TXU gives you an automatic $30 bill credit each month.",
                "Good afternoon, how many cents per kWh is your electric provider currently charging you?"
            ]
        },
        "Arturo Cavazos": {
            "role": "Independent Contractor / Home Depot",
            "location": "Home Depot Arlington - Main Entrance",
            "store_observation": "Walking briskly toward tool corral in work cap; averts gaze away from the utility kiosk.",
            "opening_hooks": [
                "Good afternoon sir, we are the certified TXU Energy desk inside the store; no signatures or account changes today.",
                "Hello, good afternoon. With total transparency on screen we can check if your current electricity rate is protected against surges.",
                "Good afternoon, excuse me. Quick question for Home Depot customers: is your residential or commercial power rate fixed or variable?"
            ]
        },
        "Laura Cárdenas": {
            "role": "Shopper at Fiesta Mart / Looking for Gift Card",
            "location": "Fiesta Mart Fort Worth - Main Entrance",
            "store_observation": "Pauses with curiosity in front of the 'Earn a $50 Store Gift Card with TXU Energy' banner.",
            "opening_hooks": [
                "Good afternoon neighbor! If we review your summer electric rate in 2 minutes, you receive a $50 store gift card.",
                "Hello, good afternoon. How much was your electricity bill last month with the A/C running all day?",
                "Good afternoon neighbor, at TXU's official kiosk we are activating 50% summer electric discounts for Fiesta Mart shoppers."
            ]
        },
        "Samuel Elizondo": {
            "role": "Professional / Checking provider app on smartphone",
            "location": "Kroger Plano - Exit Corridor",
            "store_observation": "Waiting for his shopping partner by the exit while browsing notifications on his smartphone.",
            "opening_hooks": [
                "Good afternoon sir. I noticed you use your smartphone; does your current power app provide real-time hourly usage tracking?",
                "Hello, good afternoon. For smart home tech users and EV drivers, TXU offers the Free Nights plan with 100% free power from 8 PM to 6 AM.",
                "Good afternoon. Have you explored TXU Energy's price protection guarantee to shield your smart home consumption this summer?"
            ]
        },
        "Gloria Hinojosa": {
            "role": "Senior Shopper at H-E-B / Loyal to Reliant Energy",
            "location": "H-E-B Houston - Main Entrance",
            "store_observation": "Walking unhurriedly with reusable tote bags; smiles politely but keeps walking forward.",
            "opening_hooks": [
                "Good afternoon ma'am, wonderful seeing you at H-E-B. We represent TXU Energy sharing that Oncor maintains the exact same lines but at lower rates.",
                "Hello, good afternoon. Many customers who stayed with Reliant for years were surprised to see how much they could save with TXU.",
                "Good afternoon. We deeply respect your loyalty to your current provider; in just 1 minute we can show if your price is up to date."
            ]
        },
        "Rodrigo Paredes": {
            "role": "College Student / Assisting parents with groceries",
            "location": "Walmart Supercenter Garland - Checkout Exit",
            "store_observation": "Pushing shopping cart with beverages while his family finishes paying at self-checkout.",
            "opening_hooks": [
                "Good afternoon! I am with TXU Energy sharing important details on Texas summer electricity savings for households.",
                "Hello, good afternoon. Who in your household handles reviewing the power bills so I can hand you a quick savings summary?",
                "Good afternoon. We are distributing discount vouchers for household power bills; who usually manages the utility account at home?"
            ]
        },
        "Verónica Trejo": {
            "role": "Evasive Shopper / In a hurry to reach car",
            "location": "Costco Wholesale Irving - Main Entrance",
            "store_observation": "Wearing sunglasses with packed shopping cart; politely nods with a smile but does not slow her pace.",
            "opening_hooks": [
                "Good afternoon neighbor, sorry to interrupt for a moment. Just a brief 15-second inquiry before you load your car.",
                "Hello neighbor, great seeing you. Quick question: does your household power bill usually exceed $200 during hot months?",
                "Good afternoon, we have a savings voucher flyer from TXU Energy for store members, would you like a quick comparison?"
            ]
        },
        "Ernesto Macías": {
            "role": "Irritable Shopper / Annoyed by hallway solicitors",
            "location": "Walmart Supercenter Dallas - Grocery Entrance",
            "store_observation": "Walks through exit huffing from the heat wave blasting through sliding doors; scowls at the sales kiosk.",
            "opening_hooks": [
                "Good afternoon sir, sincere apologies for the interruption. Just a respectful greeting from the TXU Energy kiosk.",
                "Hello, good afternoon. I will not hold you up at all sir, just wishing you safe travels and a wonderful afternoon.",
                "Good afternoon sir, excuse me. With this heat wave outside we are reminding shoppers that TXU protects fixed rates."
            ]
        }
    }
}


RESIDENT_ROLES_I18N = {
    'es': {
        "Fernando López": "Propietario / Casa 2 pisos en Dallas",
        "Carmen Morales": "Ama de casa / Familia en Houston",
        "Roberto Garza": "Ingeniero / Residente en Frisco",
        "Patricia Ortiz": "Dueña de negocio / Casa en Fort Worth",
        "Javier Treviño": "Profesionista / Recibo de $380 en verano",
        "Ricardo Fuentes": "Contador / Compara centavos por kWh",
        "Andrea Salazar": "Inquilina en Plano / Vive en pareja",
        "Gonzalo Villagrán": "Jubilado / 12 años con Reliant Energy",
        "Mauricio Alatorre": "Dueño de Tesla / Carga nocturna",
        "Beatriz Luna": "Residente en Arlington / Teme al slamming",
        "Carlos Méndez": "Empresario / Alto consumo de aire acondicionado",
        "Elena Ramos": "Jubilada / Presupuesto fijo en Garland",
        "Gabriel Domínguez": "Ingeniero TI / Casa inteligente en Irving",
        "Valeria Ríos": "Estudiante universitaria / Renta cuarto",
        "Armando Cárdenas": "Administrador / Busca crédito en factura",
        "Esteban Navarro": "Propietario en Mesquite / Fiel a Direct Energy",
    },
    'en': {
        "Fernando López": "Homeowner / 2-story home in Dallas",
        "Carmen Morales": "Homemaker / Family in Houston",
        "Roberto Garza": "Engineer / Resident in Frisco",
        "Patricia Ortiz": "Business Owner / House in Fort Worth",
        "Javier Treviño": "Professional / $380 summer electric bill",
        "Ricardo Fuentes": "Accountant / Compares cents per kWh",
        "Andrea Salazar": "Tenant in Plano / Living with partner",
        "Gonzalo Villagrán": "Retiree / 12 years with Reliant Energy",
        "Mauricio Alatorre": "Tesla Owner / Nighttime EV charging",
        "Beatriz Luna": "Resident in Arlington / Fears slamming",
        "Carlos Méndez": "Business Owner / Heavy A/C consumption",
        "Elena Ramos": "Retiree / Fixed budget in Garland",
        "Gabriel Domínguez": "IT Engineer / Smart home in Irving",
        "Valeria Ríos": "College Student / Renting a room",
        "Armando Cárdenas": "Administrator / Seeking bill credits",
        "Esteban Navarro": "Homeowner in Mesquite / Loyal to Direct Energy",
    }
}


ANALYTICS_I18N = {
    'es': {
        'competencies': [
            {"name": "Gancho y Apertura", "description": "Claridad en tiempo, empresa e impacto en los primeros 15s"},
            {"name": "Conexión y Empatía", "description": "Rapport, escucha activa y validación de objeciones"},
            {"name": "Diagnóstico Comercial", "description": "Preguntas sobre tarifa, consumo y factura eléctrica"},
            {"name": "Manejo de Objeciones", "description": "Superación de barreras (folletos, prisa, proveedor actual)"},
            {"name": "Asertividad de Cierre", "description": "Llamado a la acción, revisión de factura y garantía TXU"}
        ],
        'tiers': {
            'SALE_CLOSED': ("Cierre Maestro de Venta", "Venta Cerrada con Éxito"),
            'APPOINTMENT': ("Cita Comercial Calificada", "Cita Comercial Agendada"),
            'REJECTED': ("Oportunidad de Aprendizaje", "Contacto Concluido sin Cierre"),
            'COMPLETED': ("Sesión Finalizada para Evaluación", "Evaluación de Desempeño Comercial")
        },
        'strengths_pool': [
            "Gancho de entrada efectivo con identificación corporativa de TXU Energy y marco de tiempo.",
            "Excelente conexión humana, cortesía y contención emocional de la objeción.",
            "Preguntas de diagnóstico acertadas sobre el impacto del calor en la factura eléctrica.",
            "Sólido manejo de objeciones destacando los beneficios clave de la tarifa protegida.",
            "Asertividad en la propuesta de valor y aseguramiento del siguiente paso comercial.",
            "Mantuvo la compostura profesional y el respeto durante todo el diálogo.",
            "Iniciativa para interactuar y explorar las necesidades del cliente."
        ],
        'improvements_pool': [
            "Fortalece la apertura: di tu nombre, TXU Energy y ofrece un marco de 15 segundos en tu primera frase para capturar la atención.",
            "Indaga antes de ofertar: pregunta cuántos centavos por kWh pagan o cuánto subió el recibo con el aire acondicionado.",
            "Aumenta la empatía: valida primero la queja del cliente ('lo entiendo perfectamente', 'tiene toda la razón') antes de argumentar.",
            "Manejo de evasivas: si piden folleto o tienen prisa, no cedas el control; pide 30 segundos para revisar la factura o agenda una hora precisa.",
            "Llamado al cierre: menciona la garantía de satisfacción de 60 días sin penalización para eliminar cualquier sensación de riesgo.",
            "Continúa practicando cierres en menos turnos para optimizar tu tiempo de atención.",
            "Personaliza aún más las ventajas según el perfil tecnológico o ahorrador de cada cliente."
        ]
    },
    'en': {
        'competencies': [
            {"name": "Hook & Opening", "description": "Clarity in time, company name, and impact within the first 15s"},
            {"name": "Connection & Empathy", "description": "Rapport, active listening, and objection validation"},
            {"name": "Commercial Diagnosis", "description": "Questions regarding current rate, kWh usage, and electric bill"},
            {"name": "Objection Handling", "description": "Overcoming resistance (flyers, hurry, incumbent provider)"},
            {"name": "Closing Assertiveness", "description": "Call to action, bill comparison, and TXU 60-day guarantee"}
        ],
        'tiers': {
            'SALE_CLOSED': ("Master Sales Close", "Sale Closed Successfully"),
            'APPOINTMENT': ("Qualified Commercial Appointment", "Commercial Appointment Scheduled"),
            'REJECTED': ("Learning Opportunity", "Contact Concluded without Close"),
            'COMPLETED': ("Session Completed for Evaluation", "Commercial Performance Evaluation")
        },
        'strengths_pool': [
            "Effective opening hook with TXU Energy corporate identification and clear time frame.",
            "Outstanding human rapport, courtesy, and emotional objection de-escalation.",
            "Accurate diagnostic questions regarding summer heat impact on the electricity bill.",
            "Solid objection handling highlighting key benefits of price-protected fixed rates.",
            "High assertiveness in value proposition and securing the commercial next step.",
            "Maintained executive professionalism and composure throughout the dialogue.",
            "Strong proactive initiative to interact and diagnose the customer's utility needs."
        ],
        'improvements_pool': [
            "Strengthen the opening: state your name, TXU Energy, and offer a 15-second frame in your very first sentence to capture attention.",
            "Diagnose before presenting: ask what cents per kWh they pay or how much their bill jumped with summer A/C.",
            "Increase empathy: validate customer frustration first ('I completely understand', 'you are 100% right') before countering.",
            "Handling brush-offs: if they ask for a flyer or are in a hurry, keep control; ask for 30 seconds to review the bill or book a precise callback.",
            "Closing call to action: highlight the 60-day satisfaction guarantee with zero switching fees to remove all risk.",
            "Keep practicing closing in fewer turns to maximize your hourly prospecting efficiency.",
            "Further tailor savings benefits based on tech-savvy, EV, or budget-conscious customer profiles."
        ]
    }
}


def get_ui_strings(lang='es'):
    """Retorna el diccionario de cadenas UI para el idioma solicitado ('es' o 'en')."""
    return UI_STRINGS.get(lang, UI_STRINGS['es'])


def get_archetype_info(archetype_key, lang='es'):
    """Retorna los datos del arquetipo en el idioma especificado."""
    catalog = ARCHETYPE_DETAILS_I18N.get(lang, ARCHETYPE_DETAILS_I18N['es'])
    return catalog.get(archetype_key, ARCHETYPE_DETAILS_I18N['es'].get(archetype_key, {}))


def get_shopper_info(shopper_name, lang='es'):
    """Retorna los datos de observación y ganchos del comprador en el idioma especificado."""
    catalog = RETAIL_SHOPPERS_I18N.get(lang, RETAIL_SHOPPERS_I18N['es'])
    return catalog.get(shopper_name, RETAIL_SHOPPERS_I18N['es'].get(shopper_name, {}))


def get_resident_role(resident_name, lang='es'):
    """Retorna el rol profesional/residencial en el idioma correspondiente."""
    catalog = RESIDENT_ROLES_I18N.get(lang, RESIDENT_ROLES_I18N['es'])
    return catalog.get(resident_name, RESIDENT_ROLES_I18N['es'].get(resident_name, "Residente"))


LOCAL_RESPONSES_EN = {
    "HOSTILE": {
        "bare_greeting_store": "Yes? What do you want? Don't block my grocery cart just to say 'hello', my groceries are melting.",
        "bare_greeting_door": "Yes? Who are you? Don't stand on my porch just to say 'hi' with this heat wave outside.",
        "reply_default": "Look, I've had a rough day with this Texas heat wave, but at least you speak respectfully. Tell me quickly what TXU is offering.",
        "coach_default": "Opening hook: Good professional composure. Your calm approach de-escalated hostility into an opportunity.",
        "suggestions_default": [
            "TXU's Season Pass offers a 50% discount in summer and winter. How much was your electricity bill last month?",
            "With this extreme heat, the A/C skyrockets bills. We lock in fixed protected rates with zero hidden charges.",
            "I only need 60 seconds to review your kWh usage and verify if your current tariff has variable surge pricing."
        ]
    },
    "BUSY": {
        "bare_greeting_store": "Good afternoon... please make it quick, my ice is melting in the cart. What are you promoting?",
        "bare_greeting_door": "Good afternoon... please make it quick, I'm heading out the door for work. What is this about?",
        "reply_default": "I appreciate you respecting my time. I only have one minute before heading out, what's the bottom line on savings?",
        "coach_default": "Time hook: Highly effective. Respecting a busy customer's time builds immediate credibility.",
        "suggestions_default": [
            "Just 15 seconds: TXU's Season Pass gives you 50% off summer power. What was your total bill last month?",
            "What time this evening can I catch you for 2 minutes to show you a side-by-side bill comparison?",
            "If your household uses over 1,000 kWh, our Clear Deal plan provides an automatic $30 credit every month."
        ]
    },
    "SKEPTICAL": {
        "bare_greeting_store": "Yes? What company is this? I don't stop for solicitors at store exits.",
        "bare_greeting_door": "Yes? Who are you? I don't show my electric bill to anyone at my door.",
        "reply_default": "Thank you for showing your official badge. With so many scams going around, one has to be careful. How do your fixed rates work?",
        "coach_default": "Trust building: Excellent. Validating skepticism and displaying official credentials breaks down resistance.",
        "suggestions_default": [
            "You are 100% right to be cautious. We lock in fixed cents per kWh for 24 months, shielding you from summer grid spikes.",
            "Never share your account or ESI ID with unverified solicitors. Does your current contract have a fixed or variable rate?",
            "Oncor maintains the exact same lines and poles with zero service interruption during the switch."
        ]
    },
    "POLITE_EVASIVE": {
        "bare_greeting_store": "Good afternoon... excuse me, I'm heading to my car. If you have a flyer leave it with me and I'll look at it later.",
        "bare_greeting_door": "Good afternoon! If you have a flyer, leave it with me and I'll call if interested.",
        "reply_default": "Well, my summer electric bill usually exceeds $250 with the A/C running constantly. Tell me more about that 50% discount.",
        "coach_default": "Diagnostic probe: Outstanding. Asking about summer bill thresholds prevents the flyer brush-off.",
        "suggestions_default": [
            "With Season Pass you get 50% off electricity during July and August. May I calculate your exact monthly savings?",
            "Would you prefer an automatic $30 monthly bill credit or free electricity all night with Free Nights?",
            "We can review your last billing statement in 90 seconds to see if your current rate is competitive."
        ]
    },
    "IDEAL_LEAD": {
        "bare_greeting_store": "Good afternoon. Is this about electricity? My bill surged over $400 last month, what do you offer?",
        "bare_greeting_door": "Good afternoon. My power bill jumped to $420 last month. Do you have fixed rates that won't surge?",
        "reply_default": "Paying over $400 is killing my budget. If you can lock in a protected rate with 50% summer savings, I'm ready to make the switch.",
        "coach_default": "Qualified lead: Superb connection. Addressing the bill surge with immediate price protection creates high closing momentum.",
        "suggestions_default": [
            "We can lock in your 24-month fixed rate today with our 60-day satisfaction guarantee and zero cancellation fees.",
            "With Season Pass 50% discount, that $400 summer bill drops substantially. Let's verify your address to enroll.",
            "Let's finalize your enrollment in 3 minutes so your next bill is fully protected."
        ]
    },
    "BARGAIN_HUNTER": {
        "bare_greeting_store": "Good afternoon. What plan do you have and how many cents per kWh do you charge?",
        "bare_greeting_door": "Look, I pay 13.8 cents per kWh. If you can't offer under 13 cents all-inclusive, there's no point in talking.",
        "reply_default": "I like that you itemize Oncor delivery charges and offer that $30 monthly bill credit. Let's compare the EFL numbers.",
        "coach_default": "Analytical alignment: Great work. Providing transparent EFL numbers and bill credits wins analytical buyers.",
        "suggestions_default": [
            "Clear Deal gives you $30 bill credit every month above 1,000 kWh, lowering your effective average cost.",
            "Our EFL clearly separates the energy charge from Oncor TDU fees with zero hidden gimmicks.",
            "Let's calculate your average cost across 1,000 and 2,000 kWh usage tiers."
        ]
    },
    "LOYALIST": {
        "bare_greeting_store": "No thanks, I've been with Reliant for years and I'm not looking to switch.",
        "bare_greeting_door": "I've been with Reliant Energy for 12 years and never had an issue, I have no reason to switch.",
        "reply_default": "I didn't realize Oncor delivers the exact same power regardless of company. It has been years since I checked my rate per kWh.",
        "coach_default": "Overcoming inertia: Brilliant. Clarifying that delivery infrastructure is identical removes switching fear.",
        "suggestions_default": [
            "Oncor maintains the exact same wires and meters. The only difference is avoiding outdated renewal markups.",
            "Legacy accounts often pay 3 to 5 cents more per kWh on auto-renewal. Let's check your current rate.",
            "TXU offers a 60-day satisfaction guarantee with zero penalties if you aren't completely thrilled."
        ]
    },
    "TECH_SAVVY": {
        "bare_greeting_store": "I drive an EV and charge overnight. Do you have plans tailored to smart homes?",
        "bare_greeting_door": "I charge my EV overnight and control smart thermostats. Do you have plans that actually leverage that?",
        "reply_default": "Free electricity from 8 PM to 6 AM is huge for charging my EV and cooling the house overnight. How do I track it in the app?",
        "coach_default": "Tech alignment: Excellent. Pitching Free Nights to EV and smart home owners fits their exact consumption pattern.",
        "suggestions_default": [
            "TXU's Free Nights gives you 100% free electricity between 8 PM and 6 AM, including your EV charging.",
            "Our mobile app provides real-time hourly usage breakdown and smart thermostat optimization.",
            "You can schedule your EV charger to start at 8:01 PM and pay literally zero dollars for vehicle fuel."
        ]
    },
    "NON_DECISION_MAKER": {
        "bare_greeting_store": "Good afternoon, what do you need? I'm just here with my family.",
        "bare_greeting_door": "I just rent here with roommates, the utility account is under the landlord's name.",
        "reply_default": "We split the power bill among roommates, so saving 50% in summer would definitely help us. Let me give you the account holder's contact.",
        "coach_default": "Tenant qualification: Great job. Identifying who pays the utility bill uncovers a referral or secondary decision maker.",
        "suggestions_default": [
            "If you split the bill each month, sharing TXU's 50% summer discount with your landlord benefits everyone.",
            "We have zero-deposit plans for roommates and tenants. What is the best phone number to reach the account holder?",
            "What time of day is the primary account holder typically home to share a 2-minute savings summary?"
        ]
    }
}


def localize_local_output(reply, coach, suggestions, lang, archetype, is_bare_greeting=False, is_store=False):
    """
    Traduce las respuestas y críticas del motor local a inglés cuando el idioma activo es 'en'.
    """
    if (lang or 'es').lower() != 'en':
        return reply, coach, suggestions

    arch_data = LOCAL_RESPONSES_EN.get(archetype, LOCAL_RESPONSES_EN['BUSY'])
    if is_bare_greeting:
        key = 'bare_greeting_store' if is_store else 'bare_greeting_door'
        reply_en = arch_data.get(key, arch_data['reply_default'])
        coach_en = "A simple greeting is not a commercial hook. State your name, TXU Energy, and a 15-second time frame immediately."
        sugg_en = arch_data.get('suggestions_default', suggestions)[:3]
        return reply_en, coach_en, sugg_en

    return arch_data['reply_default'], arch_data['coach_default'], arch_data['suggestions_default']
