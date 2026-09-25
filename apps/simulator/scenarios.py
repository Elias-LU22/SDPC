"""
Biblioteca de escenarios, diálogos, objeciones y pedagogía de ventas puerta a puerta.
Contiene la estructura de nodos conversacionales para cada arquetipo de prospecto.
"""

SCENARIOS = {
    'BUSY': {
        'title': 'El Residente con Prisa / Ocupado',
        'archetype_name': 'El Ocupado',
        'initial_patience': 45,
        'initial_interest': 25,
        'mood_icon': '⏱️',
        'dialogue_nodes': {
            'start': {
                'statement': 'Sí dígame rápido joven, voy saliendo para el trabajo y ya tengo el tiempo encima. ¿Qué se le ofrece?',
                'options': [
                    {
                        'id': 'opt_1_bad',
                        'text': 'Buenos días, perdone que le robe unos minutitos de su valioso tiempo. Mi nombre es representante de una empresa transnacional con 20 años en el mercado...',
                        'patience_change': -35,
                        'interest_change': -10,
                        'next_node': 'busy_annoyed',
                        'tactic': 'Discurso Corporativo Tradicional (Grave Error)',
                        'coach_feedback': '¡Error fatal! El prospecto te dijo explícitamente que va de salida. Dar un discurso formal de introducción corporativa en la puerta consume su paciencia de inmediato.'
                    },
                    {
                        'id': 'opt_1_good',
                        'text': 'Entendido, sé que va de salida: le robo solo 15 segundos de reloj mientras cierra la reja. Estamos cambiando los cableados de la cuadra a fibra pura. ¿Hoy en su casa se le traba el internet cuando varios se conectan?',
                        'patience_change': +15,
                        'interest_change': +25,
                        'next_node': 'busy_hooked',
                        'tactic': 'Gancho Rápido con Reconocimiento de Tiempo (Excelente)',
                        'coach_feedback': '¡Brillante! Validaste su prisa, pusiste un límite de tiempo creíble (15 segundos) y lanzaste una pregunta de dolor directa en vez de hablar de ti.'
                    },
                    {
                        'id': 'opt_1_neutral',
                        'text': 'Solo venía a dejarle este volante con las nuevas promociones de internet y telefonía para que lo cheque cuando tenga tiempo.',
                        'patience_change': 0,
                        'interest_change': -15,
                        'next_node': 'busy_flyer_dismiss',
                        'tactic': 'Repartidor de Volantes (Inútil)',
                        'coach_feedback': 'El 95% de los volantes entregados sin generar curiosidad terminan en la basura antes de entrar a la casa. Un prospector profesional califica antes de soltar material.'
                    }
                ]
            },
            'busy_annoyed': {
                'statement': 'No joven, no tengo tiempo para sermones comerciales. Con permiso que voy tarde. [Intenta cerrar la puerta]',
                'options': [
                    {
                        'id': 'opt_rescue',
                        'text': '¡Espere, señor! Solo dígame a qué hora regresa hoy para que un técnico le mida la señal gratis en 3 minutos.',
                        'patience_change': -20,
                        'interest_change': +10,
                        'next_node': 'busy_closing_chance',
                        'tactic': 'Interrupción Desesperada',
                        'coach_feedback': 'Intentar retener al cliente físicamente cuando está irritado es riesgoso, pero al menos diste una acción concreta de 3 minutos.'
                    },
                    {
                        'id': 'opt_retreat',
                        'text': 'Tiene toda la razón, que le vaya excelente en su trabajo y maneje con cuidado.',
                        'patience_change': +10,
                        'interest_change': 0,
                        'next_node': 'door_rejected_polite',
                        'tactic': 'Retirada Cortés',
                        'coach_feedback': 'Bien al no desgastarte ni confrontar. En cambaceo la energía emocional es tu activo más valioso; cuando la puerta se pierde, saluda con elegancia y avanza.'
                    }
                ]
            },
            'busy_hooked': {
                'statement': 'Uy, pues la verdad sí, en las noches cuando mis hijos juegan y yo estoy en videollamada se congela bastante. Pero de verdad ya tengo el carro prendido.',
                'options': [
                    {
                        'id': 'opt_hook_close',
                        'text': 'Justo eso resolvimos a sus vecinos de la casa 106. No le quito más tiempo hoy: ¿a qué hora llega en la tarde para que pase 5 minutos a mostrarle cómo queda su instalación sin costo?',
                        'patience_change': +10,
                        'interest_change': +25,
                        'next_node': 'busy_book_appointment',
                        'tactic': 'Cierre de Cita Rápida con Prueba Social',
                        'coach_feedback': '¡Magistral! Mencionaste al vecino para generar confianza y pediste una cita concreta en su horario libre respetando su prisa.'
                    },
                    {
                        'id': 'opt_hook_explain',
                        'text': 'Lo que pasa es que las compañías tradicionales usan cobre coaxial y nosotros usamos fibra óptica monomodo GPON simétrica que permite 500 megas de subida...',
                        'patience_change': -25,
                        'interest_change': -10,
                        'next_node': 'busy_annoyed',
                        'tactic': 'Vómito Técnico Inoportuno',
                        'coach_feedback': 'Caíste en la trampa del tecnicismo. El prospecto te dio la señal de dolor, no era momento de explicar física cuántica sino de agendar el siguiente paso.'
                    }
                ]
            },
            'busy_flyer_dismiss': {
                'statement': 'Sale pues, déjelo ahí en el buzón y luego le echo un ojo. Hasta luego.',
                'options': [
                    {
                        'id': 'opt_flyer_end',
                        'text': 'Muchas gracias, ahí viene mi teléfono, que tenga buen día.',
                        'patience_change': 0,
                        'interest_change': -10,
                        'next_node': 'door_rejected_soft',
                        'tactic': 'Abandono Pasivo',
                        'coach_feedback': 'Prospecto perdido. Nunca te llamará. Aprendizaje: no regales material sin haber obtenido un dato de contacto o microacuerdo.'
                    }
                ]
            },
            'busy_closing_chance': {
                'statement': 'Mire, llego a las 7:00 PM. Si pasa a esa hora puntual le recibo los datos, pero ahorita ya me voy.',
                'options': [
                    {
                        'id': 'opt_confirm_7',
                        'text': 'A las 7:00 PM en punto estaré aquí con su estudio de cobertura listo. ¿Cuál es su nombre para anotarlo en mi agenda?',
                        'patience_change': +20,
                        'interest_change': +20,
                        'next_node': 'success_appointment',
                        'tactic': 'Confirmación Firme de Cita',
                        'coach_feedback': '¡Objetivo logrado! Convertiste una puerta casi cerrada en una cita formal con hora fija.'
                    }
                ]
            },
            'busy_book_appointment': {
                'statement': 'Llego como a las 6:30 PM. Si viene a las 7:00 PM me encuentra cenando con calma. Déjeme su nombre.',
                'options': [
                    {
                        'id': 'opt_confirm_direct',
                        'text': 'Hecho, soy su asesor. A las 7:00 PM paso solo 5 minutos para que vea la comparativa. ¿Me regala su nombre para la ficha de vecino?',
                        'patience_change': +20,
                        'interest_change': +30,
                        'next_node': 'success_appointment',
                        'tactic': 'Cierre Asertivo Profesional',
                        'coach_feedback': 'Excelente gestión de venta puerta a puerta: rápido, al grano, profesional y con cita asegurada.'
                    }
                ]
            }
        }
    },

    'SKEPTICAL': {
        'title': 'El Residente Escéptico / Desconfiado',
        'archetype_name': 'El Desconfiado',
        'initial_patience': 60,
        'initial_interest': 15,
        'mood_icon': '🧐',
        'dialogue_nodes': {
            'start': {
                'statement': '[Mira por la mirilla o entreabre la reja con desconfianza] ¿Quién es usted? No compramos nada en la puerta ni damos datos personales.',
                'options': [
                    {
                        'id': 'opt_defensive',
                        'text': 'No desconfíe de mí, señor(a), soy una persona honesta y mire, tengo gafete de la empresa, no soy ningún delincuente.',
                        'patience_change': -20,
                        'interest_change': -15,
                        'next_node': 'skep_more_defensive',
                        'tactic': 'Defensiva Personal (Pésima)',
                        'coach_feedback': 'Mencionar palabras como "delincuente" o "no desconfíe" activa mayores alarmas psicológicas en el prospecto. Nunca te justifiques defensivamente.'
                    },
                    {
                        'id': 'opt_disarm',
                        'text': 'Lo comprendo al 100%, hoy en día hay que ser muy cuidadoso con quién toca a la puerta. No le vengo a pedir ni dinero ni que me firme nada hoy. Mi nombre es asesor de la zona. ¿Le puedo hacer una sola pregunta sobre el servicio del fraccionamiento?',
                        'patience_change': +25,
                        'interest_change': +20,
                        'next_node': 'skep_disarmed',
                        'tactic': 'Desarme Emocional + Validación de Desconfianza',
                        'coach_feedback': '¡Técnica de oro! Validar su miedo ("yo también desconfiaría") neutraliza la tensión, y asegurar que no pedirás dinero ni firmas elimina la barrera de compra.'
                    },
                    {
                        'id': 'opt_aggressive_pitch',
                        'text': 'Señor, solo vengo a ofrecerle una promoción exclusiva con 50% de descuento que se vence hoy mismo si firma el contrato.',
                        'patience_change': -30,
                        'interest_change': -20,
                        'next_node': 'skep_slam',
                        'tactic': 'Urgencia Artificial Agresiva',
                        'coach_feedback': 'La falsa urgencia ("se vence hoy") ante un prospecto escéptico confirma su sospecha de que es una trampa comercial.'
                    }
                ]
            },
            'skep_more_defensive': {
                'statement': 'Pues gafetes cualquiera se manda a hacer en la imprenta. Dígame qué quiere o le llamo a la vigilancia.',
                'options': [
                    {
                        'id': 'opt_apology_reset',
                        'text': 'Tiene toda la razón, disculpe si lo incomodé. Solo estamos avisando a la calle sobre la nueva antena instalada. Si gusta revisar la página oficial de la compañía ahí puede verificar la cuadrilla.',
                        'patience_change': +15,
                        'interest_change': +10,
                        'next_node': 'skep_curious',
                        'tactic': 'Transparencia Institucional',
                        'coach_feedback': 'Buena recuperación. Apelar a medios oficiales y aceptar su precaución baja la adrenalina.'
                    },
                    {
                        'id': 'opt_argue',
                        'text': '¡Qué exagerado! Si no quiere escucharme me voy.',
                        'patience_change': -50,
                        'interest_change': -50,
                        'next_node': 'door_rejected_hostile',
                        'tactic': 'Confrontación Directa',
                        'coach_feedback': 'Pelear con un prospecto destruye tu moral y genera mala reputación en la cuadra. Regla número 1: jamás te enganches.'
                    }
                ]
            },
            'skep_disarmed': {
                'statement': 'Bueno... ¿de qué se trata la pregunta? Pero sin compromisos.',
                'options': [
                    {
                        'id': 'opt_probe_pain',
                        'text': 'Varios vecinos nos comentaron que pagan más de $800 al mes y cuando llueve se quedan sin conexión. ¿En su caso el proveedor actual le ha cumplido lo que le prometió o le han subido la tarifa?',
                        'patience_change': +10,
                        'interest_change': +30,
                        'next_node': 'skep_opens_up',
                        'tactic': 'Pregunta de Indagación de Dolor Común',
                        'coach_feedback': '¡Excelente pregunta de sondeo! Tocar problemas reales de facturación y fallas de servicio conecta de inmediato con la frustración del cliente.'
                    },
                    {
                        'id': 'opt_boast_product',
                        'text': 'La pregunta es si le gustaría tener el mejor módem del mundo con tecnología Wi-Fi 6 y soporte prioritario.',
                        'patience_change': -15,
                        'interest_change': +5,
                        'next_node': 'skep_skeptical_again',
                        'tactic': 'Pregunta de Autobombo',
                        'coach_feedback': 'Las preguntas genéricas de "¿le gustaría tener lo mejor?" suenan a telemarketing barato. Siempre indaga sobre su situación actual primero.'
                    }
                ]
            },
            'skep_opens_up': {
                'statement': 'Pues mire, la verdad sí me subieron 70 pesos el mes pasado sin avisar y el servicio al cliente es puro robot por WhatsApp. Nadie da la cara.',
                'options': [
                    {
                        'id': 'opt_contrast_solve',
                        'text': 'Es exactamente por lo que los vecinos se cambiaron. Con nosotros la tarifa es fija por contrato y tiene mi número directo para cualquier tema. ¿Qué le parece si revisamos su último recibo 3 minutos y le demuestro cuánto se ahorra?',
                        'patience_change': +15,
                        'interest_change': +35,
                        'next_node': 'skep_receipt_check',
                        'tactic': 'Puente Solución + Revisión de Factura',
                        'coach_feedback': 'Pedir el recibo actual es la técnica reina del cambaceo: te da el nombre, el gasto exacto y la fecha de corte para cerrar.'
                    },
                    {
                        'id': 'opt_attack_competition',
                        'text': '¡Esos de esa compañía son unos rateros! Qué bueno que me abrió para decirles sus verdades.',
                        'patience_change': -10,
                        'interest_change': +10,
                        'next_node': 'skep_receipt_check',
                        'tactic': 'Ataque Desmedido a la Competencia',
                        'coach_feedback': 'Cuidado con sonar rencoroso o hablar mal del competidor; un buen asesor deja que los números y el cliente hablen por sí mismos.'
                    }
                ]
            },
            'skep_receipt_check': {
                'statement': 'Aquí tengo la aplicación con la última factura... Pago $750 por 100 megas.',
                'options': [
                    {
                        'id': 'opt_close_value',
                        'text': 'Por $550 con nosotros tendría 500 megas de fibra pura, ahorrándose $200 cada mes ($2,400 al año). Si le aparto el paquete hoy, la instalación no le cuesta un solo centavo. ¿Lo instalamos mañana por la mañana o prefiere la tarde?',
                        'patience_change': +15,
                        'interest_change': +35,
                        'next_node': 'success_sale',
                        'tactic': 'Cierre de Doble Alternativa con Ahorro Anualizado',
                        'coach_feedback': '¡Cierre de libro de texto! Anualizaste el ahorro ($2,400 al año suena mucho más potente que $200 al mes) y usaste doble alternativa para cerrar.'
                    }
                ]
            },
            'skep_slam': {
                'statement': '¡No me interesa, gracias! [Cierra la puerta con fuerza]',
                'options': [
                    {
                        'id': 'opt_next_door',
                        'text': 'Anotar como no interesado y pasar a la siguiente casa.',
                        'patience_change': 0,
                        'interest_change': 0,
                        'next_node': 'door_rejected_hostile',
                        'tactic': 'Aceptar el No y Continuar',
                        'coach_feedback': 'El "No" es parte natural de la estadística de campo. Cada rechazo te acerca más al próximo "Sí". Respira y a la que sigue.'
                    }
                ]
            },
            'skep_curious': {
                'statement': 'A ver, dígame rápido qué traen entonces...',
                'options': [
                    {
                        'id': 'opt_resume_probe',
                        'text': 'Estamos garantizando a los vecinos de la cuadra una reducción de hasta 30% en su factura de conectividad sin perder megas. ¿Usted con quién tiene contratado?',
                        'patience_change': +10,
                        'interest_change': +20,
                        'next_node': 'skep_opens_up',
                        'tactic': 'Propuesta de Valor Concisa',
                        'coach_feedback': 'Muy buen rescate de la conversación.'
                    }
                ]
            },
            'skep_skeptical_again': {
                'statement': 'Todos dicen lo mismo. No me interesa cambiarme, gracias.',
                'options': [
                    {
                        'id': 'opt_leave_polite',
                        'text': 'Entendido señor, gracias por su tiempo, que pase buena tarde.',
                        'patience_change': 0,
                        'interest_change': 0,
                        'next_node': 'door_rejected_soft',
                        'tactic': 'Cierre Amable',
                        'coach_feedback': 'No se pudo quebrar la objeción por haber empezado con tecnicismos en vez de escuchar.'
                    }
                ]
            }
        }
    },

    'POLITE_EVASIVE': {
        'title': 'El Residente Amable pero Evasivo ("Déjeme el folleto")',
        'archetype_name': 'El Amable Evasivo',
        'initial_patience': 75,
        'initial_interest': 20,
        'mood_icon': '😊',
        'dialogue_nodes': {
            'start': {
                'statement': '¡Hola, buenas tardes joven! Ay mire, se ve muy interesante lo que trae, pero ahorita ando comiendo. ¿Por qué no me deja un volante o su tarjeta y si me interesa yo le marco?',
                'options': [
                    {
                        'id': 'opt_give_flyer',
                        'text': '¡Claro que sí señora, tenga el folleto! Ahí viene mi WhatsApp, ojalá me mande un mensajito. ¡Buen provecho!',
                        'patience_change': +10,
                        'interest_change': -20,
                        'next_node': 'polite_lost',
                        'tactic': 'Entrega Sumisa de Material (Cero Efectividad)',
                        'coach_feedback': '¡Caíste en la objeción más dulce y letal del cambaceo! Te sonrió, te dijo que sí, te pidió el volante y nunca te llamará. Regla: siempre ofrece una pregunta de calificación antes de soltar el folleto.'
                    },
                    {
                        'id': 'opt_redirect_question',
                        'text': 'Con muchísimo gusto le dejo el folleto para que coma a gusto. Solo para no dejarle propaganda que no le sirva: ¿en su casa su mayor dolor de cabeza actual es que el internet es lento o que siente que le están cobrando de más?',
                        'patience_change': 0,
                        'interest_change': +25,
                        'next_node': 'polite_engaged',
                        'tactic': 'Acepta y Redirige con Pregunta de Dolor (Técnica Sandler)',
                        'coach_feedback': '¡Extraordinario manejo de objeción! Concedes la petición ("con gusto se lo dejo") pero aíslas la necesidad real antes de irte.'
                    },
                    {
                        'id': 'opt_refuse_flyer',
                        'text': 'No señora, no le puedo dejar folleto porque la empresa me pide que explique todo en persona aquí y ahora.',
                        'patience_change': -40,
                        'interest_change': -20,
                        'next_node': 'door_rejected_polite',
                        'tactic': 'Rigidez Agresiva',
                        'coach_feedback': 'Sonaste intransigente e invasivo ante una persona que te estaba tratando con amabilidad. Destruyó la empatía.'
                    }
                ]
            },
            'polite_lost': {
                'statement': '¡Muchas gracias corazón! Que Dios te bendiga y vendas mucho. [Cierra la puerta con el folleto en mano]',
                'options': [
                    {
                        'id': 'opt_polite_finish',
                        'text': 'Agradecer y avanzar a la siguiente casa.',
                        'patience_change': 0,
                        'interest_change': 0,
                        'next_node': 'door_rejected_soft',
                        'tactic': 'Prospecto Perdido',
                        'coach_feedback': 'Conversación muy agradable, pero 0 ventas. Recuerda: en prospección no buscamos caer bien, buscamos ayudar a resolver problemas y cerrar acuerdos.'
                    }
                ]
            },
            'polite_engaged': {
                'statement': 'Pues... la verdad me cobran $680 pesos y casi ni lo usamos en el día porque salimos a trabajar. Siento que tiro el dinero.',
                'options': [
                    {
                        'id': 'opt_polite_proposal',
                        'text': 'Le entiendo perfecto Doña Carmen. Si le dejo una propuesta donde solo pague $390 por exactamente lo que necesita y se ahorre casi $300 al mes, ¿le gustaría que regrese a las 6pm que ya terminó de comer para dejárselo instalado?',
                        'patience_change': +10,
                        'interest_change': +35,
                        'next_node': 'polite_closing_appointment',
                        'tactic': 'Plan a la Medida + Cita Posterior',
                        'coach_feedback': '¡De manual! Descubriste que pagaba de más por algo que no usaba y le ofreciste una cita respetando su hora de comida.'
                    }
                ]
            },
            'polite_closing_appointment': {
                'statement': '¡Ay, pues eso sí me conviene! A las 6:30 ya está mi esposo aquí y tomamos la decisión. Pásese a esa hora.',
                'options': [
                    {
                        'id': 'opt_lock_both_decision_makers',
                        'text': 'Excelente, a las 6:30 PM en punto estaré aquí para platicar con los dos y ver los detalles. ¿Me regala su número de teléfono por si me demoro 5 minutos en la cuadra?',
                        'patience_change': +15,
                        'interest_change': +30,
                        'next_node': 'success_appointment',
                        'tactic': 'Aseguramiento de Tomadores de Decisión',
                        'coach_feedback': '¡Mundial! Tener a ambos tomadores de decisión (esposo y esposa) reunidos en la cita garantiza que la objeción de "tengo que consultarlo con mi pareja" quede eliminada.'
                    }
                ]
            }
        }
    },

    'HOSTILE': {
        'title': 'El Residente Hostil / Enojado',
        'archetype_name': 'El Hostil',
        'initial_patience': 25,
        'initial_interest': 5,
        'mood_icon': '😠',
        'dialogue_nodes': {
            'start': {
                'statement': '¡¿Qué no ven el letrero de NO MOLESTAR?! ¡Estoy harto de que toquen la campana todo el día vendedores! ¡Lárguense de mi banqueta!',
                'options': [
                    {
                        'id': 'opt_hostile_apologize_grace',
                        'text': 'Tiene toda la razón, una disculpa sincera por interrumpirlo señor, no vi el letrero. Me retiro de inmediato, que pase buena tarde.',
                        'patience_change': +20,
                        'interest_change': +10,
                        'next_node': 'hostile_deescalate',
                        'tactic': 'Desescalada Radical con Respeto Absoluto',
                        'coach_feedback': '¡Inteligencia emocional pura! No te enganchaste, desarmaste su ira aceptando su razón y protegiste tu energía para la siguiente puerta.'
                    },
                    {
                        'id': 'opt_hostile_insist',
                        'text': 'Cálmese señor, solo es una promoción que le va a convenir, no se enoje por nada.',
                        'patience_change': -30,
                        'interest_change': -20,
                        'next_node': 'hostile_explosion',
                        'tactic': 'Minimizar Emoción del Cliente (Grave Error)',
                        'coach_feedback': 'Decirle a alguien enojado "cálmese" o "no se enoje" es echarle gasolina al fuego. Nunca invalides la emoción del cliente.'
                    },
                    {
                        'id': 'opt_hostile_retaliate',
                        'text': '¡La banqueta es pública y yo estoy trabajando honestamente, aprenda a ser educado!',
                        'patience_change': -50,
                        'interest_change': -50,
                        'next_node': 'door_rejected_hostile',
                        'tactic': 'Pelea Callejera Inútil',
                        'coach_feedback': 'Pelear en la calle te cuesta 30 puntos de moral y energía. El vendedor profesional es imperturbable como un monje.'
                    }
                ]
            },
            'hostile_deescalate': {
                'statement': '[Se sorprende por tu educación y baja la guardia] ... Bueno, es que han pasado 4 hoy. ¿De qué empresa es usted?',
                'options': [
                    {
                        'id': 'opt_hostile_brief_pivot',
                        'text': 'Somos de la cuadrilla técnica de fibra óptica del vecindario. Como le digo, no quiero quitarle ni un segundo, solo estamos verificando que nadie en esta cuadra tenga problemas de corte en su servicio.',
                        'patience_change': +20,
                        'interest_change': +25,
                        'next_node': 'hostile_unexpected_win',
                        'tactic': 'Pivote Suave de Servicio Técnico',
                        'coach_feedback': '¡Increíble! Lograste convertir una situación hostil en curiosidad genuina gracias a tu templanza.'
                    },
                    {
                        'id': 'opt_hostile_leave_safe',
                        'text': 'De la nueva red de fibra. Pero de verdad lo dejo descansar, un placer saludarle.',
                        'patience_change': +10,
                        'interest_change': 0,
                        'next_node': 'door_rejected_polite',
                        'tactic': 'Retirada Estratégica Elegante',
                        'coach_feedback': 'Muy digno. A veces retirarse con clase deja una semilla positiva en el vecindario.'
                    }
                ]
            },
            'hostile_unexpected_win': {
                'statement': 'Pues fíjese que los de mi compañía me dejaron sin línea desde el martes y no han venido. ¿Ustedes instalan rápido?',
                'options': [
                    {
                        'id': 'opt_hostile_close',
                        'text': 'Hoy mismo por la tarde tengo cuadrilla en la esquina. Si me da 2 minutos le levanto la orden y en menos de 24 horas tiene su servicio funcionando al 100%. ¿Le aparto el técnico?',
                        'patience_change': +20,
                        'interest_change': +40,
                        'next_node': 'success_sale',
                        'tactic': 'Solución de Emergencia Inmediata',
                        'coach_feedback': '¡Triunfo legendario de cambaceo! Transformaste un grito hostil en una venta cerrada resolviendo su dolor urgente.'
                    }
                ]
            },
            'hostile_explosion': {
                'statement': '¡¿Qué me calme?! ¡Ahorita le suelto a los perros si no se larga de aquí! [Portazo estruendoso]',
                'options': [
                    {
                        'id': 'opt_hostile_end',
                        'text': 'Retirarse rápido y recuperar el aliento.',
                        'patience_change': -20,
                        'interest_change': 0,
                        'next_node': 'door_rejected_hostile',
                        'tactic': 'Portazo Violento',
                        'coach_feedback': 'Lección dolorosa: cuando un prospecto está alterado, nunca discutas ni insistas. Tu paz mental y seguridad van primero.'
                    }
                ]
            }
        }
    },

    'IDEAL_LEAD': {
        'title': 'El Prospecto Calificado / Cliente Ideal',
        'archetype_name': 'El Prospecto Calificado',
        'initial_patience': 70,
        'initial_interest': 45,
        'mood_icon': '⭐',
        'dialogue_nodes': {
            'start': {
                'statement': '¡Buenas tardes! Fíjese que qué bueno que pasa. Mi vecino de enfrente me dijo que vinieron a instalarle algo de internet nuevo. ¿Ustedes son los mismos?',
                'options': [
                    {
                        'id': 'opt_ideal_confirm_probe',
                        'text': '¡Exactamente señor! Estuvimos con Don Javier en la mañana. Me comentó que por aquí varios vecinos buscaban mejor velocidad. ¿En su caso qué tal le funciona su conexión actual?',
                        'patience_change': +15,
                        'interest_change': +30,
                        'next_node': 'ideal_shared_pain',
                        'tactic': 'Confirmación de Referido + Sondeo Abierto',
                        'coach_feedback': '¡Apalancamiento perfecto! Usar el nombre del vecino genera confianza instantánea y abre la conversación de forma orgánica.'
                    },
                    {
                        'id': 'opt_ideal_long_pitch',
                        'text': 'Sí señor, somos nosotros. Mire, le voy a leer el folleto completo: tenemos paquete de 100, 200, 300, 500 y 1000 megas simétricos con IP fija opcional...',
                        'patience_change': -20,
                        'interest_change': -10,
                        'next_node': 'ideal_bored',
                        'tactic': 'Lectura de Folleto (Mata-Ventas)',
                        'coach_feedback': '¡No leas un menú cuando el cliente ya tiene hambre! Cuando un prospecto viene recomendado, haz preguntas para cerrar rápido, no lo aburras con opciones infinitas.'
                    }
                ]
            },
            'ideal_shared_pain': {
                'statement': 'Mire, mi esposa da clases en línea y mis hijos juegan en la consola. La empresa actual nos cobra $900 al mes y a cada rato se cae. Si me dan mejor servicio y pago menos, me cambio hoy mismo.',
                'options': [
                    {
                        'id': 'opt_ideal_direct_close',
                        'text': 'Don Javier contrató el de 500 megas por $550 al mes y le quedó perfecto. Se ahorra $350 mensuales con fibra simétrica directa. Si me regala una copia de su identificación o recibo, en 5 minutos le aparto la cuadrilla de instalación para mañana a primera hora. ¿Cerramos el contrato de una vez?',
                        'patience_change': +20,
                        'interest_change': +40,
                        'next_node': 'success_sale',
                        'tactic': 'Cierre Directo por Compromiso Inmediato',
                        'coach_feedback': '¡Magistral! El prospecto te dio luz verde total y fuiste directo al cierre sin titubear ni sobre-explicar.'
                    },
                    {
                        'id': 'opt_ideal_hesitate',
                        'text': 'Bueno, pues si quiere le dejo una hojita para que lo platique con su esposa y en una semana regreso a ver qué pensaron.',
                        'patience_change': -15,
                        'interest_change': -25,
                        'next_node': 'ideal_hesitated_lost',
                        'tactic': 'Miedo al Cierre (Vendedor Cobarde)',
                        'coach_feedback': '¡Cometiste el pecado mortal del vendedor! El prospecto te dijo "me cambio hoy mismo" y tú le dijiste que regrese en una semana. Si no pides el pedido, la venta se enfría y muere.'
                    }
                ]
            },
            'ideal_bored': {
                'statement': 'Son muchas opciones... ¿cuál es el que le pusieron a Javier y cuánto cuesta?',
                'options': [
                    {
                        'id': 'opt_ideal_recover_close',
                        'text': '500 megas de fibra por $550 al mes con módem de alta cobertura. Es el paquete favorito del fraccionamiento. ¿Le aparto el técnico para mañana?',
                        'patience_change': +15,
                        'interest_change': +30,
                        'next_node': 'success_sale',
                        'tactic': 'Simplificación y Cierre',
                        'coach_feedback': 'Buena recuperación rápida al simplificar la oferta.'
                    }
                ]
            },
            'ideal_hesitated_lost': {
                'statement': 'Ah... bueno, si usted dice. Déjeme la hoja y luego vemos. Hasta luego.',
                'options': [
                    {
                        'id': 'opt_ideal_end_lost',
                        'text': 'Despedirse lamentando la oportunidad.',
                        'patience_change': 0,
                        'interest_change': 0,
                        'next_node': 'door_rejected_soft',
                        'tactic': 'Oportunidad de Oro Desperdiciada',
                        'coach_feedback': 'Que esto te sirva de lección: cuando el cliente dice "sí quiero", dejas de vender y empiezas a firmar.'
                    }
                ]
            }
        }
    },

    'NOT_HOME': {
        'title': 'Nadie en Casa / Sin Respuesta',
        'archetype_name': 'Nadie Atiende',
        'initial_patience': 0,
        'initial_interest': 0,
        'mood_icon': '🚪',
        'dialogue_nodes': {
            'start': {
                'statement': '[Tocas el timbre dos veces y esperas 30 segundos. Se escuchan pasos a lo lejos pero nadie abre, o la casa está vacía con las luces apagadas.]',
                'options': [
                    {
                        'id': 'opt_leave_hanger',
                        'text': 'Dejar un colgador de puerta (Door Hanger) con teléfono y pasar a la siguiente casa.',
                        'patience_change': 0,
                        'interest_change': 0,
                        'next_node': 'not_home_finished',
                        'tactic': 'Gestión Eficiente del Tiempo en Calle',
                        'coach_feedback': 'Excelente disciplina. En puerta fría, si en 30-45 segundos no abren, dejas recordatorio y avanzas. Quedarse esperando minutos en una puerta vacía agota tu día.'
                    }
                ]
            }
        }
    }
}


def get_scenario(archetype_code):
    return SCENARIOS.get(archetype_code, SCENARIOS['SKEPTICAL'])
