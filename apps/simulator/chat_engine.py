import random
import re

RESIDENTS = [
    {"name": "Fernando López", "role": "Propietario / Casa 2 pisos en Dallas", "archetype": "BUSY"},
    {"name": "Carmen Morales", "role": "Ama de casa / Familia en Houston", "archetype": "POLITE_EVASIVE"},
    {"name": "Roberto Garza", "role": "Ingeniero / Residente en Frisco", "archetype": "SKEPTICAL"},
    {"name": "Patricia Ortiz", "role": "Dueña de negocio / Casa en Fort Worth", "archetype": "HOSTILE"},
    {"name": "Javier Treviño", "role": "Profesionista / Recibo de $380 en verano", "archetype": "IDEAL_LEAD"},
    {"name": "Ricardo Fuentes", "role": "Contador / Compara centavos por kWh", "archetype": "BARGAIN_HUNTER"},
    {"name": "Andrea Salazar", "role": "Inquilina en Plano / Vive en pareja", "archetype": "NON_DECISION_MAKER"},
    {"name": "Gonzalo Villagrán", "role": "Jubilado / 12 años con Reliant Energy", "archetype": "LOYALIST"},
    {"name": "Mauricio Alatorre", "role": "Dueño de Tesla / Carga nocturna", "archetype": "TECH_SAVVY"},
    {"name": "Beatriz Luna", "role": "Residente en Arlington / Teme al slamming", "archetype": "SKEPTICAL"},
    {"name": "Carlos Méndez", "role": "Empresario / Alto consumo de aire acondicionado", "archetype": "BUSY"},
    {"name": "Elena Ramos", "role": "Jubilada / Presupuesto fijo en Garland", "archetype": "POLITE_EVASIVE"},
    {"name": "Gabriel Domínguez", "role": "Ingeniero TI / Casa inteligente en Irving", "archetype": "TECH_SAVVY"},
    {"name": "Valeria Ríos", "role": "Estudiante universitaria / Renta cuarto", "archetype": "NON_DECISION_MAKER"},
    {"name": "Armando Cárdenas", "role": "Administrador / Busca crédito en factura", "archetype": "BARGAIN_HUNTER"},
    {"name": "Esteban Navarro", "role": "Propietario en Mesquite / Fiel a Direct Energy", "archetype": "LOYALIST"},
]

ARCHETYPE_DETAILS = {
    "BUSY": {
        "title": "El Ocupado (Prisa con el A/C)",
        "description": "Tiene prisa evidente y va de salida. Castiga discursos corporativos largos; premia ganchos de 15 segundos sobre el 50% de descuento en verano con TXU Season Pass.",
        "initial_patience": 50,
        "initial_interest": 20,
        "initial_message": "Dígame rápido por favor, voy de salida al trabajo. Con este calor de Texas nadie quiere estar en la puerta. ¿Qué se le ofrece?",
        "suggestions": [
            "Solo 15 segundos mientras sale: con este calor el aire acondicionado dispara las facturas. TXU le da 50% de descuento en verano con Season Pass. ¿Cuánto pagó el mes pasado?",
            "Sé que va con prisa. ¿A qué hora le encuentro en la tarde para mostrarle el comparativo de su recibo en 2 minutos?",
            "Vengo a explicarle la historia de la desregulación eléctrica de Texas y todas las opciones de kilovatios."
        ]
    },
    "SKEPTICAL": {
        "title": "El Desconfiado (Teme al Slamming)",
        "description": "Teme estafas y el cambio no autorizado de proveedor (slamming). Se desarma con gafete oficial de TXU Energy, validando su precaución y no exigiendo su recibo de inmediato.",
        "initial_patience": 60,
        "initial_interest": 15,
        "initial_message": "¿Quién es usted? No le muestro mi recibo de luz a nadie en la puerta, andan muchos estafadores cambiando contratos sin permiso.",
        "suggestions": [
            "Tiene toda la razón y hace bien en protegerse; nunca muestre su número ESI ID a extraños. Soy asesor oficial de TXU Energy, mire mi gafete. No le pido su recibo hoy, solo una pregunta: ¿su tarifa actual es fija o variable?",
            "Soy representante oficial de la empresa, mire mi credencial, no tiene nada de qué desconfiar.",
            "A sus vecinos de la casa de al lado les ayudamos a bloquear su tarifa en centavos fijos para protegerse de los picos de verano."
        ]
    },
    "POLITE_EVASIVE": {
        "title": "El Amable Evasivo",
        "description": "Amable y sonriente, pero busca despedirte pidiendo un folleto. Regla: no soltar propaganda sin antes calificar con una pregunta sobre su consumo en verano.",
        "initial_patience": 70,
        "initial_interest": 20,
        "initial_message": "Buenas tardes joven. Se ve interesante lo que trae de TXU, pero ando ocupada. ¿Por qué no me deja su folleto y si me interesa yo les hablo?",
        "suggestions": [
            "Con mucho gusto se lo dejo. Solo para saber cuál dejarle: ¿su factura de luz suele superar los $250 dólares en julio y agosto?",
            "Claro que sí, tenga el volante. Ahí viene el teléfono de TXU Energy para cuando guste marcar.",
            "No puedo dejar folletos por política de la empresa, necesito que me escuche ahora mismo."
        ]
    },
    "HOSTILE": {
        "title": "El Hostil",
        "description": "Irritable y a la defensiva por el calor o vendedores ambulantes. Exige desescalada inmediata con empatía sincera o retirada profesional. Castiga el 'cálmese'.",
        "initial_patience": 30,
        "initial_interest": 5,
        "initial_message": "¡Otra vez tocando la puerta! Con 100 grados de calor afuera lo último que quiero es que vengan a molestar con la luz. ¡No me interesa nada!",
        "suggestions": [
            "Tiene toda la razón señor, una disculpa sincera por interrumpirlo. Con este calor nadie quiere que le toquen la puerta. Me retiro de inmediato, que pase buena tarde.",
            "Cálmese señor, no se enoje por nada, solo le vengo a ofrecer una tarifa de TXU que le va a convenir.",
            "La banqueta es pública y solo estoy haciendo mi trabajo con TXU Energy."
        ]
    },
    "IDEAL_LEAD": {
        "title": "El Prospecto Calificado (Recibo Disparado)",
        "description": "Su contrato de electricidad anterior venció y su proveedor actual le cobró una tarifa exorbitante; busca alivio urgente. Premia asertividad y cierre directo.",
        "initial_patience": 70,
        "initial_interest": 50,
        "initial_message": "Buenas tardes. Qué bueno que pasa de TXU. El mes pasado mi compañía me cobró casi $400 dólares por el puro aire acondicionado. Esto es un abuso y quiero cambiarme ya.",
        "suggestions": [
            "Le entiendo perfecto, muchos vecinos sufrieron ese golpe porque su contrato venció y entraron a tarifa variable. Con TXU Season Pass le damos 50% de descuento en verano y tarifa protegida. ¿Tiene su factura a mano para calcular su ahorro?",
            "Tenemos paquetes con muchas tarifas, opciones solares, planes nocturnos y términos variables...",
            "Si le garantizamos bloquear su precio por 24 meses y reducir su factura de verano a la mitad, ¿hacemos el registro hoy mismo sin cortes?"
        ]
    },
    "BARGAIN_HUNTER": {
        "title": "El Cazador de Descuentos (Centavos por kWh)",
        "description": "Obsesionado con comparar precios por kWh y evitar cargos ocultos. Castiga la falta de claridad; premia números netos de la etiqueta EFL y créditos de factura.",
        "initial_patience": 55,
        "initial_interest": 40,
        "initial_message": "A ver joven de TXU, ¿a cuántos centavos el kWh viene el plan? Pero dígame el promedio real a 1,000 kWh en la etiqueta EFL, no me disfrace los cargos de Oncor.",
        "suggestions": [
            "En el plan Clear Deal el promedio a 1,000 kWh queda en 12.8 centavos con el crédito automático de $30 dólares de TXU incluido, todo desglosado en la EFL. ¿Cuánto le cobran hoy?",
            "Depende de cuánto consuma cada mes, las tarifas de electricidad van variando en Texas según el clima.",
            "Con nosotros se ahorra una fortuna garantizada, somos la compañía de luz más barata de Texas."
        ]
    },
    "NON_DECISION_MAKER": {
        "title": "El No Decide (Familiar)",
        "description": "Vive en la propiedad pero no es el titular del contrato de electricidad ante ERCOT. Castiga intentar venderle a quien no firma; premia agendar el horario del titular.",
        "initial_patience": 65,
        "initial_interest": 30,
        "initial_message": "Buenas tardes. Sí nos llega caro el recibo de la luz, pero de eso se encarga mi pareja. Yo aquí no tomo decisiones de contratos.",
        "suggestions": [
            "Comprendo totalmente. ¿A qué hora llega su pareja para pasar 3 minutos y entregarle la comparativa de ahorro de verano directamente?",
            "No se preocupe, fírmeme usted y ya luego le avisa cuando llegue el cambio de TXU en su recibo.",
            "¿Me permitiría dejarle una nota breve con el comparativo de TXU Season Pass para que lo platiquen en la noche?"
        ]
    },
    "LOYALIST": {
        "title": "El Casado con la Competencia (Reliant / Direct Energy)",
        "description": "Lleva años con su compañía por inercia y teme quedarse sin luz durante el cambio. Castiga atacar a su compañía; premia explicar que Oncor entrega los cables y la transición es invisible.",
        "initial_patience": 60,
        "initial_interest": 15,
        "initial_message": "Llevo más de 10 años con Reliant y no me gusta andar cambiando de compañía. Aunque paguemos bastante, ya los conozco y no quiero problemas.",
        "suggestions": [
            "Es muy respetable su lealtad, Reliant es una empresa conocida. Pero en Texas, Oncor sigue siendo quien entrega la energía física; no hay corte ni por un segundo. Solo por curiosidad: ¿hace cuánto que no le revisan la tarifa para bajarle el costo?",
            "Reliant es carísima y se aprovechan de los clientes viejos que no se fijan en el recibo.",
            "TXU le ofrece 60 días de garantía total: si no ve el ahorro en su primer recibo, puede cambiar de plan sin penalización."
        ]
    },
    "TECH_SAVVY": {
        "title": "El Propietario con Auto Eléctrico (EV) / Casa Inteligente",
        "description": "Tiene vehículo eléctrico (Tesla/EV), paneles solares o termostato inteligente. Busca maximizar ahorro nocturno con Free Nights & Solar Days.",
        "initial_patience": 50,
        "initial_interest": 45,
        "initial_message": "¿TXU maneja el plan de Noches Gratis (Free Nights)? Acabamos de comprar un auto eléctrico y tenemos termostato inteligente, me interesa cargar el carro a costo cero.",
        "suggestions": [
            "Exactamente, con Free Nights & Solar Days toda la electricidad de 8:00 PM a 6:00 AM es 100% gratuita. Puede cargar su auto eléctrico y enfriar su casa toda la noche sin pagar un centavo de energía. ¿A qué hora suele enchufar su vehículo?",
            "Sí tenemos ese plan, pero le conviene más el paquete estándar para toda la casa que usan todos los clientes.",
            "De día la energía es 100% solar y de noche es gratis por contrato. ¿Revisamos su consumo mensual para confirmar si es el plan óptimo para su perfil?"
        ]
    }
}


def create_new_door():
    """Genera un nuevo prospecto de puerta para la sesión."""
    resident = random.choice(RESIDENTS)
    archetype_key = resident["archetype"]
    archetype_data = ARCHETYPE_DETAILS[archetype_key]
    door_num = random.randint(101, 299)

    return {
        "door_number": door_num,
        "resident_name": resident["name"],
        "resident_role": resident["role"],
        "archetype": archetype_key,
        "archetype_title": archetype_data["title"],
        "archetype_description": archetype_data["description"],
        "patience": archetype_data["initial_patience"],
        "interest": archetype_data["initial_interest"],
        "status": "IN_PROGRESS",  # IN_PROGRESS, SALE_CLOSED, APPOINTMENT, REJECTED
        "turn": 1,
        "messages": [
            {
                "sender": "prospect",
                "text": archetype_data["initial_message"],
                "coach": None,
                "patience_change": 0,
                "interest_change": 0,
            }
        ],
        "suggestions": archetype_data["suggestions"],
    }


def evaluate_response_local(user_text, door_state):
    """
    Evalúa la respuesta del asesor comercial de TXU Energy usando el motor
    local de respaldo con reglas de prospección y arquetipos residenciales.
    """
    text = user_text.lower().strip()
    archetype = door_state["archetype"]
    turn = door_state["turn"]

    # Detección de patrones en contexto de energía eléctrica TXU
    has_time_hook = bool(re.search(r'(15 segundo|r[aá]pido|no le quito tiempo|solo un minuto|un momento|de pasada|10 segundo)', text))
    has_pain_probe = bool(re.search(r'(cu[aá]nto paga|recibo|factura|cobro|luz|electricidad|verano|calor|aire acondicionado|a/c|clima|subi[oó]|car[oa]|tarifa variable)', text))
    has_neighbor_social_proof = bool(re.search(r'(vecin|cuadra|manzana|al lado|don |do[nñ]a |aqu[ií] enfrente|calle)', text))
    has_close_attempt = bool(re.search(r'(recibo|factura|compar|revis|hacer el cambio|enrol|registr|cambiarnos|apart|firm|contrat|cambio digital)', text))
    has_flyer_surrender = bool(re.search(r'(tenga el folleto|tenga el volante|ah[ií] le dejo|ah[ií] viene mi n[uú]mero|le dejo la tarjeta|1-800)', text))
    has_flyer_redirect = bool(re.search(r'(con gusto|con mucho gusto|se lo dejo pero|antes de dej[aá]rselo|para saber si vale la pena|para saber cu[aá]l)', text))
    has_defensive_claim = bool(re.search(r'(no desconf[ií]e|soy honesto|no soy delincuente|mire mi credencial|mire mi gafete|c[aá]lmese|no se enoje)', text))
    has_apology_respect = bool(re.search(r'(disculp|raz[oó]n|respet|permiso|buena tarde|no quise molestar|me retiro|con este calor)', text))
    has_season_pass = bool(re.search(r'(season pass|50%|cincuenta por ciento|descuento en verano|julio y agosto|invierno|mitad)', text))
    has_free_nights = bool(re.search(r'(noches gratis|free nights|8.*6|costo cero|gratis de noche|cargar|tesla|auto el[eé]ctrico|veh[ií]culo el[eé]ctrico|ev)', text))
    has_cents_kwh = bool(re.search(r'(centavo|\d+\s*centavo|\d+\.\d+\s*centavo|kwh|efl|etiqueta|cr[eé]dito de \$30|clear deal|tarifa fija)', text))
    has_oncor_guarantee = bool(re.search(r'(oncor|centerpoint|cables|postes|no hay corte|no se le va la luz|cero cortes|mismo cableado|distribuidora)', text))
    has_decision_maker_probe = bool(re.search(r'(a qu[eé] hora llega|a qu[eé] hora est[aá]|titular|espos|pap[aá]|mam[aá]|qui[eé]n se encarga|regres|vuelvo|tarde|noche)', text))
    has_attack_competitor = bool(re.search(r'(no sirve|p[eé]sim|obsolet|mentiros|chatarra|porquer[ií]a|robo|abus|se aprovechan)', text))
    has_slamming_assurance = bool(re.search(r'(gafete|oficial|100 a[nñ]os|proteger|esi id|no le pido firmas|no le pido su recibo)', text))
    is_too_long = len(text) > 180

    patience_change = 0
    interest_change = 0
    reply = ""
    coach = ""
    new_suggestions = []

    # ==========================
    # EVALUACIÓN POR ARQUETIPO (TXU ENERGY)
    # ==========================
    if archetype == "BUSY":
        if has_time_hook and (has_pain_probe or has_season_pass or has_neighbor_social_proof):
            patience_change = +15
            interest_change = +30
            reply = "Pues mire, la verdad sí, el mes pasado me llegaron casi $350 dólares de pura luz por tener el aire prendido día y noche. Pero ya tengo el carro encendido."
            coach = "Excelente apertura de prospección. Reconociste su prisa, pusiste un marco de 15 segundos y tocaste el dolor principal en Texas: el recibo inflado por el aire acondicionado."
            new_suggestions = [
                "No le quito más tiempo hoy: ¿a qué hora llega en la tarde para mostrarle el comparativo con Season Pass en 2 minutos?",
                "¿Le dejo un comparativo con su vecino de al lado para que lo revise con calma?",
                "Le puedo explicar las especificaciones técnicas completas ahorita mismo."
            ]
        elif is_too_long or has_defensive_claim:
            patience_change = -30
            interest_change = -10
            reply = "No tengo tiempo para discursos largos joven, ya voy tarde al trabajo. Con permiso. [Comienza a cerrar la puerta]"
            coach = "Error en apertura rápida. El prospecto con prisa rechaza introducciones largas. Debiste usar un gancho de 15 segundos sobre el recibo de luz."
            new_suggestions = [
                "Una disculpa, solo dígame si le encuentro a las 6:30 PM para revisar su tarifa sin compromiso.",
                "Tiene toda la razón, que tenga excelente día de trabajo.",
                "¡Espere! Solo son 5 minutos de su tiempo."
            ]
        elif has_close_attempt or has_decision_maker_probe:
            patience_change = +10
            interest_change = +25
            reply = "Llego a las 6:30 PM. Si pasa a esa hora puntual con gusto le muestro la factura de luz para ver si es cierto el descuento, pero ahorita ya me voy."
            coach = "Aseguramiento de cita. Lograste un compromiso de hora precisa respetando su agenda."
            new_suggestions = [
                "A las 6:30 PM puntual estaré aquí. ¿Cuál es su nombre para anotarlo en mi agenda?",
                "Perfecto, nos vemos a las 6:30 PM. Buen día.",
            ]
        else:
            patience_change = -15
            interest_change = +5
            reply = "Ajá... pero dígame al grano de qué compañía es y qué quiere, porque de verdad voy de salida."
            coach = "Respuesta neutral. Acelera el ritmo e introduce el ahorro de verano de TXU Season Pass de inmediato."
            new_suggestions = [
                "TXU le da 50% de descuento en verano en los cargos de luz. ¿A qué hora le encuentro para hacer el cálculo?",
                "¿Cuánto pagó en su última factura para decirle si califica al descuento?"
            ]

    elif archetype == "SKEPTICAL":
        if has_apology_respect or has_slamming_assurance or (has_neighbor_social_proof and not has_close_attempt):
            patience_change = +20
            interest_change = +30
            reply = "Bueno... los vecinos sí me dijeron que andaban de TXU Energy. Es que con tantos estafadores uno desconfía. ¿Qué plan tienen para proteger la tarifa?"
            coach = "Gran manejo de la desconfianza. Validar su derecho a proteger su cuenta sin presionar por el recibo desarma la sospecha de slamming."
            new_suggestions = [
                "Tenemos la promesa Price Protect: tarifa fija por contrato sin aumentos en olas de calor. ¿Sabe si hoy su tarifa es fija o variable?",
                "Si me permite su última factura 1 minuto, le calculo exactamente cuánto se ahorraría con tarifa protegida.",
                "TXU Energy es la empresa número 1 de Texas con más de 100 años sirviendo a la comunidad."
            ]
        elif has_defensive_claim:
            patience_change = -25
            interest_change = -20
            reply = "Gafetes cualquiera los imprime. No le voy a mostrar ningún recibo, por favor retírese de mi propiedad."
            coach = "Error defensivo. Decir 'no desconfíe' o 'mire mi credencial' activa mayores alertas. Nunca exijas el recibo sin antes generar confianza."
            new_suggestions = [
                "Comprendo su precaución y tiene toda la razón. No le pido datos hoy. Le dejo el número oficial de TXU Energy para que verifique cuando guste.",
                "Disculpe la molestia, que tenga buen día.",
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
                "Totalmente garantizado por escrito en la EFL y sin corte de luz. ¿Registramos la cuenta para el próximo ciclo?",
            ]
        else:
            patience_change = -5
            interest_change = +10
            reply = "Sigo sin ver la ventaja. Todas las compañías de luz prometen ahorrar y luego el primer recibo llega carísimo."
            coach = "Objeción de escepticismo activo. Menciona la garantía de satisfacción de 60 días de TXU Energy sin penalización."
            new_suggestions = [
                "TXU le da 60 días de prueba sin penalización: si no le convence el ahorro, puede cambiar de plan libremente. ¿Le parece justo?",
                "¿Cuánto pagó en su última factura para demostrarle la diferencia exacta en dólares?"
            ]

    elif archetype == "POLITE_EVASIVE":
        if has_flyer_redirect and has_pain_probe:
            patience_change = +10
            interest_change = +35
            reply = "Pues mire... la verdad el mes pasado pagué casi $320 dólares y casi ni estamos en el día. No entiendo por qué subió tanto."
            coach = "Excelente técnica 'Acepta y Redirige'. Concediste la petición del folleto pero aislaste el problema real de su factura antes de retirarte."
            new_suggestions = [
                "Podemos aplicarle el plan Season Pass para que en julio y agosto pague la mitad de energía. ¿A qué hora está su familia para revisarlo juntos?",
                "Si le consigo el crédito automático de $30 dólares en factura, ¿le aparto su registro hoy mismo?",
            ]
        elif has_flyer_surrender:
            patience_change = 0
            interest_change = -30
            reply = "Muchas gracias joven, que le vaya muy bien y venda mucho. [Cierra la puerta amablemente con el volante en la mano]"
            coach = "Error clásico de cambaceo. Entregar el folleto sin calificar la factura equivale al 99% de tasa de pérdida de prospectos."
            new_suggestions = [
                "¡Espere Doña Carmen! Solo una pregunta rápida antes de que entre...",
                "Agradecer amablemente y pasar a la siguiente puerta."
            ]
        elif has_close_attempt or has_decision_maker_probe:
            patience_change = +10
            interest_change = +25
            reply = "A las 6:30 ya llega mi esposo de trabajar y podemos sacar la factura para revisarla juntos si gusta pasar a esa hora."
            coach = "Aseguramiento de tomador de decisiones. Gran paso para revisar la factura con quien tiene la decisión de compra."
            new_suggestions = [
                "Excelente, a las 6:30 PM en punto regreso para platicarlo con los dos. Gracias Doña Carmen."
            ]
        else:
            patience_change = -5
            interest_change = +10
            reply = "Sí suena muy bonito lo de TXU, pero como le digo, déjeme la información impresa y nosotros lo checamos con calma."
            coach = "El prospecto insiste en evadir. Haz una pregunta directa sobre cuánto le llegó su última factura de verano."
            new_suggestions = [
                "Con gusto se lo dejo. Solo dígame: ¿cuándo fue la última vez que su compañía de luz le congeló el precio para no subirle en calor?",
                "Claro que sí, le dejo el folleto de TXU Energy."
            ]

    elif archetype == "HOSTILE":
        if has_apology_respect:
            patience_change = +30
            interest_change = +15
            reply = "[Baja el tono, sorprendido por su educación] ... Bueno, es que han pasado como cuatro hoy a molestar. ¿Dice que viene de TXU Energy?"
            coach = "Inteligencia emocional y desescalada. No te enganchaste y desarmaste la tensión reconociendo la molestia del calor con respeto."
            new_suggestions = [
                "Así es señor, representamos a TXU Energy. Solo estamos verificando que los residentes del área no paguen de más por el aire acondicionado.",
                "De TXU Energy. Pero de verdad lo dejo con su familia, una disculpa y buen día.",
            ]
        elif has_defensive_claim:
            patience_change = -40
            interest_change = -30
            reply = "¡¿Qué me calme?! ¡Aprenda a respetar propiedad privada o llamo a la policía! [Portazo fuerte]"
            coach = "Fallo severo. Decir 'cálmese' a una persona irritada intensifica el conflicto. Perdiste la puerta."
            new_suggestions = [
                "Retirarse con calma y respirar profundo.",
            ]
        elif has_pain_probe or has_season_pass:
            patience_change = +15
            interest_change = +25
            reply = "Los de mi compañía me cobraron $420 dólares el mes pasado y no me quisieron hacer ningún ajuste. ¿Ustedes de verdad tienen descuento o es el mismo cuento?"
            coach = "Giro inesperado. El prospecto reveló su molestia real: una factura abusiva de su compañía actual."
            new_suggestions = [
                "Le entiendo completamente. En TXU Season Pass le descontamos el 50% de la energía en los meses de calor. ¿Revisamos su factura para corregirlo?",
            ]
        else:
            patience_change = -20
            interest_change = -10
            reply = "No quiero cambiarme de nada, no insista. [Mano en la puerta]"
            coach = "Resistencia alta. Si no aplicas empatía sincera o te disculpas, cerrará la puerta."
            new_suggestions = [
                "Disculpe la molestia señor, que tenga buena tarde.",
                "Solo le informaba de la tarifa de verano, no le quito más tiempo."
            ]

    elif archetype == "IDEAL_LEAD":
        if has_close_attempt or has_season_pass or (has_neighbor_social_proof and has_pain_probe):
            patience_change = +15
            interest_change = +40
            reply = "Mi vecino me dijo que con TXU Season Pass le bajó la mitad del cargo de luz en julio. Si me da ese plan con precio congelado, me cambio hoy mismo."
            coach = "Cliente listo para cerrar. No des más rodeos; solicita su factura para registrar la cuenta en el sistema de TXU."
            new_suggestions = [
                "Trato hecho. Tomo los datos de su recibo y queda registrado en TXU hoy mismo sin interrupción de luz. ¿A qué nombre elaboro el contrato?",
                "¿Prefiere que le envíe la confirmación a su correo o por mensaje de texto?",
            ]
        elif has_cents_kwh or has_pain_probe:
            patience_change = +15
            interest_change = +35
            reply = "Tener 50% de descuento en verano y tarifa protegida por 24 meses me parece excelente. Si el trámite no me corta la luz, hacemos el cambio."
            coach = "Excelente concreción. El prospecto calificado buscaba una solución rápida a su factura disparada."
            new_suggestions = [
                "Totalmente garantizado por Oncor: no se corta ni un segundo. ¿A qué nombre elaboramos la orden de servicio?",
                "¿Tiene su recibo a mano para validar su número ESI ID en el sistema?",
            ]
        elif is_too_long:
            patience_change = -15
            interest_change = -10
            reply = "Son demasiadas opciones joven. Solo dígame cuánto me voy a ahorrar en verano y cómo hacemos el cambio."
            coach = "Sobrecarga de información. Cuando el cliente ya tiene interés, simplifica y pide la factura para enrolarlo."
            new_suggestions = [
                "Con Season Pass se ahorra la mitad en cargos de energía en verano. ¿Hacemos el registro en 2 minutos?",
            ]
        else:
            patience_change = +10
            interest_change = +25
            reply = "Ahorita estoy pagando casi 18 centavos con la otra compañía y me sube en verano. ¿A cuánto me quedaría con TXU?"
            coach = "Señal de dolor evidente. Plantea el ahorro directo comparativo con el plan Season Pass o Clear Deal."
            new_suggestions = [
                "Con nosotros la tarifa queda protegida desde 12.8 centavos con crédito incluido. ¿Revisamos su factura de una vez?",
            ]

    elif archetype == "BARGAIN_HUNTER":
        if has_cents_kwh or has_season_pass:
            patience_change = +15
            interest_change = +35
            reply = "A 12.8 centavos promedio con el crédito de $30 de TXU y 50% de descuento en verano, los números sí me cuadran. ¿Qué documentos necesita para el trámite?"
            coach = "Gran cierre numérico. El cazador de ofertas o negociador de kWh necesitaba ver el desglose neto sin costos ocultos."
            new_suggestions = [
                "Solo su última factura para ingresar su ESI ID y mañana queda programado el cambio en Oncor. ¿A qué nombre elaboro el registro?",
                "¿Prefiere el plan a 12 meses o a 24 meses con tarifa protegida?",
            ]
        elif is_too_long:
            patience_change = -20
            interest_change = -10
            reply = "Puro rollo y no me dijo el precio exacto por kWh en la EFL a 1,000 kWh. Si no me da números claros no me haga perder el tiempo."
            coach = "Falta de claridad en costo. A este arquetipo hay que presentarle los centavos por kWh y el crédito de factura sin rodeos."
            new_suggestions = [
                "Son 12.8 centavos netos por kWh en la EFL a 1,000 kWh con crédito de $30 dólares. ¿Le aparto el registro?",
                "Una disculpa, voy al grano: Clear Deal a 12.8 centavos fijos. ¿Le conviene?"
            ]
        else:
            patience_change = -5
            interest_change = +15
            reply = "¿Y ese plan tiene cargo base mensual o penalización si gasto menos de 1,000 kWh? Quiero ver la etiqueta EFL."
            coach = "Objeción de transparencia. Muestra la etiqueta EFL y aclara los cargos de entrega de Oncor para dar confianza total."
            new_suggestions = [
                "La EFL desglosa cargo de energía y cargo TDU de Oncor con total transparencia. ¿Revisamos su consumo mensual?",
                "¿Cuánto consume en kWh al mes para calcularle el costo neto exacto en dólares?"
            ]

    elif archetype == "NON_DECISION_MAKER":
        if has_decision_maker_probe:
            patience_change = +25
            interest_change = +25
            door_state["status"] = "APPOINTMENT"
            reply = "Mi pareja llega a las 7:00 PM del trabajo. Si pasa a esa hora puntual con gusto sacamos la factura de luz y lo revisan."
            coach = "Excelente calificación de rol. En cambaceo de luz es vital no desgastar la oferta con quien no es titular de la cuenta ante ERCOT."
            new_suggestions = [
                "A las 7:00 PM en punto estaré aquí para revisar la factura con ustedes en 3 minutos. Muchas gracias.",
                "Perfecto, anotado en mi agenda a las 7:00 PM. Que pase buena tarde."
            ]
        elif is_too_long or has_close_attempt:
            patience_change = -25
            interest_change = -15
            reply = "Joven, ya le dije que la cuenta de luz está a nombre de mi pareja y yo aquí no firmo nada. No insista conmigo por favor."
            coach = "Error táctico grave: intentar cerrar a quien no tiene potestad legal sobre el contrato genera rechazo. Pregunta el horario del titular."
            new_suggestions = [
                "Tiene toda la razón, una disculpa. Solo dígame a qué hora llega el titular para pasar brevemente.",
                "Disculpe la molestia, que tenga muy buena tarde."
            ]
        else:
            patience_change = -10
            interest_change = +5
            reply = "Pues se oye bien lo de TXU, pero como le digo, quien paga y decide eso es mi familiar cuando llegue."
            coach = "Identificación de barrera de autoridad. No expliques más promociones; solicita el horario del titular."
            new_suggestions = [
                "Entiendo perfectamente. ¿A qué hora le encuentro hoy por la tarde para dejarle la propuesta en sus manos?",
                "¿Le puedo dejar una nota con el cálculo de ahorro de verano para que lo platiquen en familia?"
            ]

    elif archetype == "LOYALIST":
        if has_oncor_guarantee or has_season_pass:
            patience_change = +20
            interest_change = +35
            reply = "¿O sea que Oncor sigue entregando la luz por los mismos cables y no hay ningún corte? Si no me arriesgo a quedarme sin aire acondicionado, vale la pena checarlo."
            coach = "Excelente desactivación de fricción. El cliente leal a Reliant o Direct Energy teme cortes operativos; aclarar el rol de Oncor disipa el miedo por completo."
            new_suggestions = [
                "Exactamente, cero minutos sin servicio garantizado. ¿Revisamos su factura para calcular la diferencia con Season Pass?",
                "Totalmente garantizado. ¿A qué hora le acomoda que le deje el comparativo impreso?"
            ]
        elif has_attack_competitor:
            patience_change = -30
            interest_change = -25
            reply = "A mí Reliant me ha cumplido bien todos estos años y no me gusta que vengan a hablar mal de ellos a mi puerta. Buenas tardes."
            coach = "Grave error: atacar a su compañía actual cuestiona su propio criterio de compra. Valida su lealtad y enfócate en la ventaja del 50% de Season Pass."
            new_suggestions = [
                "Tiene toda la razón y una disculpa por el comentario. Respeto su lealtad con su empresa. Que pase buena tarde.",
                "Comprendo su punto señor, una disculpa sincera."
            ]
        else:
            patience_change = -5
            interest_change = +10
            reply = "Es que ya estoy acostumbrado a ellos. Cambiarme de compañía de luz siempre se me hace un lío de trámites."
            coach = "Objeción de inercia. Explica que el cambio a TXU es 100% digital a través del medidor inteligente sin trámites engorrosos."
            new_suggestions = [
                "El cambio a TXU es 100% digital por su medidor inteligente, sin papeleos ni cortes de energía. ¿Hacemos la prueba?",
                "¿Hace cuánto que Reliant no le ajusta la tarifa para compensar el consumo de verano?"
            ]

    elif archetype == "TECH_SAVVY":
        if has_free_nights or has_cents_kwh:
            patience_change = +25
            interest_change = +40
            reply = "Electricidad 100% gratuita de 8:00 PM a 6:00 AM para cargar el Tesla y enfriar la casa a costo cero me parece ideal. ¿Cómo registramos el plan?"
            coach = "Conexión de propuesta de valor perfecta. Alineaste el plan Free Nights & Solar Days con su caso de uso de alta demanda nocturna (EV y climatización)."
            new_suggestions = [
                "Solo ingresamos su número ESI ID y correo para activar Free Nights en su próximo ciclo. ¿A qué nombre elaboro el registro?",
                "¿Tiene su recibo a la mano para confirmar que su medidor inteligente esté listo para Free Nights?"
            ]
        elif has_flyer_surrender or is_too_long:
            patience_change = -25
            interest_change = -15
            reply = "Pura publicidad genérica sin datos de horarios ni de la EFL. No me resolvió lo de las horas gratis de noche. Paso, gracias."
            coach = "Falta de preparación técnica. Un cliente con EV o casa inteligente exige datos precisos del horario de Free Nights."
            new_suggestions = [
                "Una disculpa, le confirmo: de 8:00 PM a 6:00 AM la energía es 100% gratis por contrato todos los días. ¿Le interesa revisarlo?",
                "Tiene razón, disculpe. Que pase buen día."
            ]
        else:
            patience_change = -5
            interest_change = +15
            reply = "¿Pero el horario gratis empieza a las 8:00 PM o a las 9:00 PM? Porque es a la hora que programo el cargador del auto."
            coach = "Pregunta técnica clave. Confirma el horario de 8:00 PM a 6:00 AM de Free Nights para consolidar el cierre."
            new_suggestions = [
                "Inicia a las 8:00 PM en punto hasta las 6:00 AM. Cero costo de energía en ese horario. ¿Apartamos su plan?",
                "Son 10 horas completas de energía gratis cada noche, ideal para su auto eléctrico. ¿Hacemos el registro?"
            ]

    # Actualizar estados de la puerta
    door_state["patience"] = max(0, min(100, door_state["patience"] + patience_change))
    door_state["interest"] = max(0, min(100, door_state["interest"] + interest_change))
    door_state["turn"] += 1

    # Evaluar desenlaces
    if door_state["interest"] >= 80 and (has_close_attempt or archetype == "IDEAL_LEAD"):
        door_state["status"] = "SALE_CLOSED"
        reply = reply + " ¡Excelente, hagámoslo! Aquí tiene mi factura para hacer la transición a TXU Energy."
    elif door_state["interest"] >= 60 and has_close_attempt:
        door_state["status"] = "APPOINTMENT"
        reply = reply + " Quedamos entonces en esa hora para revisar la factura a detalle."
    elif door_state["patience"] <= 15 or "portazo" in reply.lower() or "cerrar la puerta" in reply.lower() and door_state["patience"] < 25:
        door_state["status"] = "REJECTED"
        if not ("portazo" in reply.lower() or "cierra" in reply.lower()):
            reply = reply + " Ya no me interesa, gracias. [Cierra la puerta]"

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
