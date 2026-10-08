import re
from django.test import TestCase, Client
from django.urls import reverse
from apps.simulator.chat_engine import create_new_door, evaluate_response, ARCHETYPE_DETAILS


class SingleScreenChatSimulatorTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_new_door_structure(self):
        door = create_new_door()
        self.assertIn('door_number', door)
        self.assertIn('resident_name', door)
        self.assertIn('archetype', door)
        self.assertIn('patience', door)
        self.assertIn('interest', door)
        self.assertEqual(door['status'], 'IN_PROGRESS')
        self.assertEqual(len(door['messages']), 0, "Al llegar al pórtico no debe haber mensajes previos.")
        self.assertFalse(door['doorbell_rung'], "El timbre no debe haber sonado inicialmente.")
        self.assertEqual(door['turn'], 0)
        self.assertTrue(len(door['suggestions']) > 0, "Debe incluir sugerencias de ganchos de apertura.")

    def test_evaluate_response_opening_hook_busy_archetype(self):
        door = create_new_door()
        door['archetype'] = 'BUSY'
        door['patience'] = 50
        door['interest'] = 20
        door['turn'] = 0
        door['messages'] = []

        from apps.simulator.chat_engine import evaluate_response_local
        # El vendedor habla primero con gancho de 15 segundos sobre aire acondicionado y TXU Season Pass
        updated_door = evaluate_response_local("Solo le robo 15 segundos: con este calor TXU le da 50% de descuento en verano con Season Pass.", door)
        self.assertGreater(updated_door['interest'], 20)
        self.assertEqual(len(updated_door['messages']), 2, "Deben generarse 2 mensajes: vendedor primero y prospecto respondiendo.")
        self.assertEqual(updated_door['messages'][0]['sender'], 'user')
        self.assertEqual(updated_door['messages'][1]['sender'], 'prospect')
        self.assertTrue(updated_door['doorbell_rung'])
        self.assertIn('Gancho de apertura:', updated_door['messages'][1]['coach'])

    def test_ring_doorbell_view(self):
        # Cargar primera puerta en modo DOOR
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        session.save()
        self.client.get(reverse('simulator:chat_view'))
        self.assertFalse(self.client.session['door_state']['doorbell_rung'])

        # Tocar timbre vía POST
        resp = self.client.post(reverse('simulator:ring_doorbell'), HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.client.session['door_state']['doorbell_rung'])
        self.assertContains(resp, 'Timbre Activado')

    def test_chat_view_loads_clean_ui(self):
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        session.save()
        response = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Puerta #')
        self.assertContains(response, 'Paciencia')
        self.assertContains(response, 'Interés')
        self.assertContains(response, 'Siguiente Puerta')
        self.assertContains(response, 'Tocar Timbre para Iniciar')

        # Verificar que no contenga emojis comunes
        content = response.content.decode('utf-8')
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        self.assertFalse(bool(emoji_pattern.search(content)), "No deben existir emojis en la interfaz.")

    def test_send_message_post_and_htmx(self):
        # 1. Enviar mensaje de apertura estándar
        resp = self.client.post(reverse('simulator:send_message'), {
            'message': 'Buenas tardes, disculpe la molestia'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        session = self.client.session
        self.assertIn('door_state', session)
        self.assertEqual(len(session['door_state']['messages']), 2)
        self.assertEqual(session['door_state']['messages'][0]['sender'], 'user')
        self.assertEqual(session['door_state']['messages'][1]['sender'], 'prospect')

        # 2. Enviar segundo mensaje con cabecera HTMX
        resp_htmx = self.client.post(reverse('simulator:send_message'), {
            'message': 'Solo le robo 15 segundos para revisar su recibo de luz con TXU'
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(resp_htmx.status_code, 200)
        self.assertContains(resp_htmx, 'Análisis del Coach Comercial')

    def test_next_door_and_reset(self):
        # Cargar primera puerta
        self.client.get(reverse('simulator:chat_view'))
        first_door_num = self.client.session['door_state']['door_number']
        self.assertEqual(len(self.client.session['door_state']['messages']), 0)

        # Enviar un mensaje de gancho
        self.client.post(reverse('simulator:send_message'), {'message': 'Hola vecino, buenas tardes'})
        self.assertEqual(len(self.client.session['door_state']['messages']), 2)

        # Reiniciar chat de la puerta actual
        self.client.post(reverse('simulator:reset_chat'))
        self.assertEqual(len(self.client.session['door_state']['messages']), 0)
        self.assertFalse(self.client.session['door_state']['doorbell_rung'])

        # Siguiente puerta
        self.client.post(reverse('simulator:next_door'))
        self.assertEqual(len(self.client.session['door_state']['messages']), 0)
        self.assertFalse(self.client.session['door_state']['doorbell_rung'])

    def test_all_nine_archetypes_handled(self):
        from apps.simulator.chat_engine import evaluate_response_local
        expected_archetypes = [
            "BUSY", "SKEPTICAL", "POLITE_EVASIVE", "HOSTILE", "IDEAL_LEAD",
            "BARGAIN_HUNTER", "NON_DECISION_MAKER", "LOYALIST", "TECH_SAVVY"
        ]
        for arch in expected_archetypes:
            self.assertIn(arch, ARCHETYPE_DETAILS)
            mock_door = {
                "door_number": 100,
                "resident_name": "Test User",
                "resident_role": "Residente",
                "archetype": arch,
                "archetype_title": ARCHETYPE_DETAILS[arch]["title"],
                "archetype_description": ARCHETYPE_DETAILS[arch]["description"],
                "patience": 50,
                "interest": 30,
                "status": "IN_PROGRESS",
                "turn": 1,
                "messages": [{"sender": "prospect", "text": "Hola", "coach": None}],
                "suggestions": []
            }
            res = evaluate_response_local("Tenemos el plan TXU Season Pass a 12.8 centavos por kWh con 50% de descuento en verano", mock_door)
            self.assertIsNotNone(res)
            self.assertGreaterEqual(len(res["messages"]), 3)
            self.assertTrue(bool(res["messages"][-1]["coach"]))

    def test_resident_gender_assignment(self):
        from apps.simulator.views import ensure_door_gender
        door = create_new_door()
        self.assertIn('resident_gender', door)
        self.assertIn(door['resident_gender'], ['M', 'F'])

        # Probar ensure_door_gender con sesión existente sin resident_gender
        female_door = {'resident_name': 'Carmen Morales'}
        updated_female = ensure_door_gender(female_door)
        self.assertEqual(updated_female['resident_gender'], 'F')

        male_door = {'resident_name': 'Roberto Garza'}
        updated_male = ensure_door_gender(male_door)
        self.assertEqual(updated_male['resident_gender'], 'M')

    def test_chat_view_renders_gender_attribute(self):
        response = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('data-gender=', content)
        self.assertIn('data-resident=', content)

    def test_create_new_door_porch_observation(self):
        door = create_new_door()
        self.assertIn('porch_observation', door)
        self.assertTrue(len(door['porch_observation']) > 5)

    def test_next_door_cycles_without_immediate_repetition(self):
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        session.save()
        self.client.get(reverse('simulator:chat_view'))
        initial_door = self.client.session.get('door_state')
        previous_name = initial_door['resident_name']
        previous_arch = initial_door['archetype']

        # Cycle through 5 consecutive doors
        for _ in range(5):
            resp = self.client.post(reverse('simulator:next_door'), HTTP_HX_REQUEST='true')
            self.assertEqual(resp.status_code, 200)
            current_door = self.client.session.get('door_state')
            # Check resident name did not immediately repeat
            self.assertNotEqual(current_door['resident_name'], previous_name)
            # Check archetype did not immediately repeat
            self.assertNotEqual(current_door['archetype'], previous_arch)
            # Check door number advanced
            self.assertGreater(current_door['door_number'], initial_door['door_number'])
            previous_name = current_door['resident_name']
            previous_arch = current_door['archetype']

    def test_evaluate_response_flexible_rapport_and_greeting(self):
        from apps.simulator.chat_engine import evaluate_response_local
        door = create_new_door()
        door['patience'] = 60
        door['interest'] = 20
        door['turn'] = 1

        # Test greeting and rapport without harsh patience drop
        greeting_text = "Buenas tardes vecino, que tenga un excelente dia. Disculpe la molestia, solo queria saludarlo."
        updated = evaluate_response_local(greeting_text, door)
        self.assertGreaterEqual(updated['patience'], 60, "El saludo educado no debe penalizar la paciencia.")
        self.assertGreater(updated['interest'], 20, "El saludo cordial debe generar ligera empatia.")

        # Test open question
        question_door = create_new_door()
        question_door['patience'] = 50
        question_door['interest'] = 25
        question_door['turn'] = 1
        q_text = "Entiendo perfectamente su punto. Me gustaria saber, como ha sentido el cobro de la luz este verano?"
        updated_q = evaluate_response_local(q_text, question_door)
        self.assertGreaterEqual(updated_q['patience'], 50, "Las preguntas abiertas no deben derrumbar la paciencia.")

    def test_svg_logo_and_light_mode_default(self):
        response = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Verificar que el logo SVG está en el DOM
        self.assertIn('txu_door_logo.svg', content, "El logo SVG personalizado debe estar en la interfaz.")
        self.assertIn('Logo TXU Energy', content)

        # Verificar controles de modo claro / modo oscuro
        self.assertIn('id="theme-toggle-btn"', content)
        self.assertIn('id="theme-icon-sun"', content)
        self.assertIn('id="theme-icon-moon"', content)
        self.assertIn('Modo Claro', content)

        # Verificar que por defecto la etiqueta HTML no tiene la clase dark (Modo Claro predeterminado)
        self.assertIn('<html lang="es" class="h-full antialiased">', content)
        self.assertNotIn('<html lang="es" class="h-full antialiased dark">', content)

    def test_tts_view_empty_text_returns_204(self):
        resp = self.client.get(reverse('simulator:tts_view'), {'text': '', 'gender': 'M'})
        self.assertEqual(resp.status_code, 204, "Petición vacía a TTS debe retornar 204 No Content.")

    def test_tts_view_graceful_response(self):
        # En entorno sin conexión o sin edge-tts debe retornar 204 o 200 con audio/mpeg de forma segura
        resp = self.client.get(reverse('simulator:tts_view'), {'text': 'Hola buenas tardes', 'gender': 'F'})
        self.assertIn(resp.status_code, [200, 204])
        if resp.status_code == 200:
            self.assertEqual(resp['Content-Type'], 'audio/mpeg')

    def test_tts_service_clean_text(self):
        from apps.simulator.tts_service import clean_tts_text
        raw_text = "Buenas tardes. [Abre la puerta con desconfianza] **No me interesa**, gracias. [Cierra]"
        cleaned = clean_tts_text(raw_text)
        self.assertNotIn('[Abre la puerta', cleaned)
        self.assertNotIn('[Cierra]', cleaned)
        self.assertNotIn('**', cleaned)
        self.assertEqual(cleaned, "Buenas tardes. No me interesa, gracias.")

    def test_turn_awareness_prevents_mid_chat_opening_greetings(self):
        """Verifica que a partir del turno 1 no se generen saludos de apertura ni feedback de gancho inicial."""
        from apps.simulator.chat_engine import evaluate_response_local, ARCHETYPE_DETAILS
        archetypes = ["POLITE_EVASIVE", "BUSY", "SKEPTICAL", "HOSTILE", "LOYALIST"]
        for arch in archetypes:
            door = {
                "door_number": 105,
                "resident_name": "Test Resident",
                "resident_role": "Residente",
                "archetype": arch,
                "archetype_title": ARCHETYPE_DETAILS[arch]["title"],
                "archetype_description": ARCHETYPE_DETAILS[arch]["description"],
                "patience": 50,
                "interest": 30,
                "status": "IN_PROGRESS",
                "turn": 2,  # Ya en turno 2 (en curso)
                "messages": [
                    {"sender": "user", "text": "Hola", "coach": None},
                    {"sender": "prospect", "text": "Respuesta 1", "coach": None},
                    {"sender": "user", "text": "Pregunta 2", "coach": None},
                    {"sender": "prospect", "text": "Respuesta 2", "coach": None},
                ],
                "suggestions": []
            }
            # Enviar pregunta abierta que antes activaba has_natural_personality
            res = evaluate_response_local("El calor es insoportable, ¿le gustaría que le presente veranos gratis?", door)
            latest_reply = res["messages"][-1]["text"].lower()
            latest_coach = res["messages"][-1]["coach"].lower()

            # No debe reiniciar con saludos típicos de apertura
            self.assertFalse(latest_reply.startswith("buenas tardes"), f"El arquetipo {arch} saludó en turno intermedio: {latest_reply}")
            self.assertFalse(latest_reply.startswith("hola buenas"), f"El arquetipo {arch} saludó en turno intermedio: {latest_reply}")
            # El coach no debe diagnosticar gancho de apertura inicial
            self.assertNotIn("gancho de apertura:", latest_coach)
            self.assertNotIn("contacto inicial", latest_coach)
            self.assertNotIn("evasión inicial", latest_coach)

    def test_multi_turn_progression_elena_ramos(self):
        """Prueba de flujo completo multi-turno con Elena Ramos (POLITE_EVASIVE)."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        door = create_new_door()
        door['archetype'] = 'POLITE_EVASIVE'
        door['patience'] = 50
        door['interest'] = 20
        door['turn'] = 0
        door['messages'] = []

        # Turno 1 (Apertura)
        d1 = evaluate_response_local("Buenas tardes señora Elena, somos de TXU Energy, ¿consume mucha energía eléctrica con el clima?", door)
        self.assertIn("Gancho de apertura:", d1["messages"][-1]["coach"])
        self.assertEqual(d1["turn"], 1)

        # Turno 2 (Manejo de folleto / empatía)
        d2 = evaluate_response_local("Entiendo perfectamente Doña Elena, soy Elías asesor de ventas de TXU Energy y con este calor el aire acondicionado genera mucho consumo.", d1)
        self.assertNotIn("Gancho de apertura:", d2["messages"][-1]["coach"])
        self.assertFalse(d2["messages"][-1]["text"].startswith("Buenas tardes joven"))
        self.assertEqual(d2["turn"], 2)

        # Turno 3 (Propuesta de valor - Veranos gratis / Season Pass)
        d3 = evaluate_response_local("Claro, el calor es pesado. ¿Le gustaría conocer Season Pass con 50% de descuento en verano?", d2)
        self.assertNotIn("Buenas tardes joven", d3["messages"][-1]["text"])
        self.assertIn("contrato", d3["messages"][-1]["text"].lower())
        self.assertEqual(d3["status"], "IN_PROGRESS")
        self.assertEqual(d3["turn"], 3)

        # Turno 4 (Cierre con factura y garantía)
        d4 = evaluate_response_local("Tiene 60 días de garantía total sin penalización. ¿Tiene su factura a mano para calcular el ahorro?", d3)
        self.assertEqual(d4["status"], "SALE_CLOSED")
        self.assertIn("factura", d4["messages"][-1]["text"].lower())

    def test_bare_greeting_opening_penalized_in_hostile(self):
        """Un saludo vacío como 'hola' en el turno de apertura ante un prospecto hostil debe ser penalizado."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        door = create_new_door()
        door['resident_name'] = 'Patricia Ortiz'
        door['archetype'] = 'HOSTILE'
        door['patience'] = 50
        door['interest'] = 30
        door['turn'] = 0
        door['messages'] = []

        result = evaluate_response_local("hola", door)
        # La paciencia debe caer de 50 a 35 (-15)
        self.assertEqual(result['patience'], 35)
        # El interés debe caer de 30 a 25 (-5)
        self.assertEqual(result['interest'], 25)
        # La respuesta del prospecto debe reflejar molestia y pedir identificación
        last_reply = result['messages'][-1]['text']
        self.assertIn("calorón", last_reply.lower())
        self.assertIn("¿quién es usted", last_reply.lower())
        # El coach comercial debe reprender el saludo vacío
        coach = result['messages'][-1]['coach']
        self.assertIn("Un simple saludo no es un gancho comercial", coach)
        self.assertIn("TXU Energy", coach)

    def test_bare_greeting_opening_penalized_in_busy(self):
        """Un saludo vacío ante un prospecto ocupado debe reducir su paciencia de inmediato."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        door = create_new_door()
        door['archetype'] = 'BUSY'
        door['patience'] = 50
        door['interest'] = 20
        door['turn'] = 0
        door['messages'] = []

        result = evaluate_response_local("buenas tardes", door)
        # La paciencia debe caer de 50 a 40 (-10)
        self.assertEqual(result['patience'], 40)
        coach = result['messages'][-1]['coach']
        self.assertIn("Falta de gancho de tiempo y motivo", coach)

    def test_bare_greeting_mid_conversation_rebuked(self):
        """Saludar con 'hola' en medio de una conversación ya iniciada debe ser reprendido."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        door = create_new_door()
        door['archetype'] = 'HOSTILE'
        door['patience'] = 40
        door['interest'] = 25
        door['turn'] = 2
        door['messages'] = [
            {"sender": "user", "text": "buenas tardes", "coach": None},
            {"sender": "prospect", "text": "¿Qué quiere?", "coach": None},
        ]

        result = evaluate_response_local("hola", door)
        self.assertLessEqual(result['patience'], 30)
        last_reply = result['messages'][-1]['text']
        self.assertIn("seguir saludando", last_reply.lower())

    def test_set_prospecting_mode_endpoint(self):
        """Verifica que el endpoint /chat/mode/ actualice la sesión y devuelva el modo solicitado."""
        # 1. Cambiar a modo Tienda
        resp = self.client.post(reverse('simulator:set_prospecting_mode'), {'mode': 'STORE'}, HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.session.get('prospecting_mode'), 'STORE')
        door = self.client.session.get('door_state')
        self.assertEqual(door['encounter_type'], 'STORE')
        self.assertContains(resp, 'Abordar Comprador')

        # 2. Cambiar a modo Puerta
        resp_door = self.client.post(reverse('simulator:set_prospecting_mode'), {'mode': 'DOOR'}, HTTP_HX_REQUEST='true')
        self.assertEqual(resp_door.status_code, 200)
        self.assertEqual(self.client.session.get('prospecting_mode'), 'DOOR')
        door2 = self.client.session.get('door_state')
        self.assertEqual(door2['encounter_type'], 'DOOR')
        self.assertContains(resp_door, 'Tocar Timbre')

        # 3. Cambiar a modo Aleatorio
        resp_rand = self.client.post(reverse('simulator:set_prospecting_mode'), {'mode': 'RANDOM'}, HTTP_HX_REQUEST='true')
        self.assertEqual(resp_rand.status_code, 200)
        self.assertEqual(self.client.session.get('prospecting_mode'), 'RANDOM')

    def test_create_store_encounter_structure(self):
        """Verifica la generación de prospectos en puertas y kioscos de tiendas de autoservicio."""
        from apps.simulator.chat_engine import create_new_door, RETAIL_LOCATIONS
        store_encounter = create_new_door(mode='STORE')
        self.assertEqual(store_encounter['encounter_type'], 'STORE')
        self.assertIn(store_encounter['location_name'], RETAIL_LOCATIONS)
        self.assertEqual(store_encounter['trigger_action_label'], 'Abordar Comprador')
        self.assertEqual(store_encounter['trigger_sound'], 'store_chime')
        self.assertIsNotNone(store_encounter['door_number'])
        self.assertTrue(len(store_encounter['porch_observation']) > 5)
        self.assertIn('Kiosco', store_encounter['location_detail'])

    def test_store_encounter_evaluation_gift_card_and_hurry(self):
        """Verifica que ganchos comerciales orientados al retail (tarjetas de regalo, empatía con víveres) sean reconocidos por el coach."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        store_encounter = create_new_door(mode='STORE')
        store_encounter['archetype'] = 'BUSY'
        store_encounter['patience'] = 45
        store_encounter['interest'] = 20
        store_encounter['turn'] = 0
        store_encounter['messages'] = []

        hook_text = "Buenas tardes vecino, no le detengo el paso con sus bolsas: en el kiosco de TXU le regalamos una gift card de $50 al revisar su recibo."
        result = evaluate_response_local(hook_text, store_encounter)
        self.assertGreater(result['interest'], 20)
        coach = result['messages'][-1]['coach']
        self.assertTrue('kiosco' in coach.lower() or 'retail' in coach.lower() or 'gancho' in coach.lower())

    def test_store_bare_greeting_penalized(self):
        """Un saludo plano sin gancho mientras el cliente sale apresurado con mandado de la tienda debe penalizar la paciencia."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        store_encounter = create_new_door(mode='STORE')
        store_encounter['archetype'] = 'BUSY'
        store_encounter['patience'] = 50
        store_encounter['interest'] = 20
        store_encounter['turn'] = 0
        store_encounter['messages'] = []

        result = evaluate_response_local("hola buenas tardes", store_encounter)
        self.assertLess(result['patience'], 50)
        coach = result['messages'][-1]['coach']
        self.assertIn("retail", coach.lower())
        reply = result['messages'][-1]['text'].lower()
        self.assertTrue('mandado' in reply or 'paso' in reply or 'prisa' in reply or 'carrito' in reply or 'hielo' in reply or 'rápido' in reply)

    def test_mode_selector_rendered_in_chat_view(self):
        """Verifica que la barra de control de modalidad (Aleatorio, Puerta, Tienda) se renderice en la vista principal."""
        resp = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('mode-selector-bar', content)
        self.assertIn('Aleatorio', content)
        self.assertIn('Puerta', content)
        self.assertIn('Tienda', content)
        self.assertIn(reverse('simulator:set_prospecting_mode'), content)

    def test_compute_chat_analytics_structure(self):
        """Verifica que compute_chat_analytics genere un informe con todas las competencias y métricas."""
        from apps.simulator.chat_engine import compute_chat_analytics
        dummy_state = {
            'status': 'SALE_CLOSED',
            'archetype': 'IDEAL_LEAD',
            'patience': 80,
            'interest': 90,
            'messages': [
                {'sender': 'user', 'text': 'Buenas tardes, asesor oficial de TXU Energy con tarifa fija por contrato.'},
                {'sender': 'prospect', 'text': 'Me interesa bastante.'},
                {'sender': 'user', 'text': 'Excelente, revisemos su factura para calcular su 50% de descuento.'},
                {'sender': 'prospect', 'text': 'Hagamos el cambio de una vez.'}
            ]
        }
        analytics = compute_chat_analytics(dummy_state)
        self.assertIn('overall_score', analytics)
        self.assertGreaterEqual(analytics['overall_score'], 80)
        self.assertIn('tier_label', analytics)
        self.assertIn('status_label', analytics)
        self.assertEqual(len(analytics['competencies']), 5)
        for comp in analytics['competencies']:
            self.assertIn('name', comp)
            self.assertIn('score', comp)
            self.assertIn('description', comp)
        self.assertTrue(len(analytics['strengths']) > 0)
        self.assertTrue(len(analytics['areas_for_improvement']) > 0)
        self.assertIn('turns', analytics['metrics'])
        self.assertEqual(analytics['metrics']['turns'], 2)

    def test_finish_chat_view_htmx(self):
        """Verifica que el endpoint finish_chat genere el reporte analítico por HTMX."""
        self.client.get(reverse('simulator:chat_view'))
        resp = self.client.post(reverse('simulator:finish_chat'), HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        session_door = self.client.session.get('door_state')
        self.assertIsNotNone(session_door)
        self.assertIn('analytics', session_door)
        content = resp.content.decode('utf-8')
        self.assertIn('analytics-report-card', content)
        self.assertIn('Informe Analítico de Desempeño Comercial', content)
        self.assertIn('Puntaje Global', content)
        self.assertIn('Evaluación de Competencias Clave', content)

    def test_dynamic_alerts_and_colors_rendering(self):
        """Verifica que las alertas de Oportunidad de Cierre y Riesgo de Rechazo se muestren ante los umbrales definidos."""
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        door = create_new_door(mode='DOOR')
        door['interest'] = 75
        door['patience'] = 20
        session['door_state'] = door
        session.save()

        resp = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('¡Cierre!', content)
        self.assertIn('¡Riesgo!', content)
        self.assertIn('bg-gradient-to-r from-emerald-500 to-teal-400', content)
        self.assertIn('bg-gradient-to-r from-rose-600 to-rose-400', content)

    def test_hints_toggle_button_and_hidden_popover(self):
        """Verifica que las pistas tácticas estén ocultas en un popover y que se active mediante el botón Pistas."""
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        door = create_new_door(mode='DOOR')
        door['status'] = 'IN_PROGRESS'
        door['suggestions'] = ['Propuesta de prueba 1', 'Propuesta de prueba 2']
        session['door_state'] = door
        session.save()

        resp = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('id="btn-toggle-hints"', content)
        self.assertIn('id="hints-popover"', content)
        self.assertIn('toggleHintsMenu()', content)
        self.assertIn('Concluir y Evaluar', content)

    def test_no_duplicate_intercom_start_button(self):
        """Verifica que no exista botón redundante de tocar timbre o abordar en la barra de intercomunicador."""
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        door = create_new_door(mode='DOOR')
        session['door_state'] = door
        session.save()

        resp = self.client.get(reverse('simulator:chat_view'))
        content = resp.content.decode('utf-8')
        self.assertIn('Manos Libres: Activo', content)
        self.assertIn('Voz Activa', content)
        self.assertIn('Tocar Timbre para Iniciar', content)
        self.assertEqual(content.count('Tocar Timbre para Iniciar'), 1)

    def test_set_language_view_switches_session_and_translates_door(self):
        """Verifica que cambiar el idioma a 'en' traduzca la puerta activa sin reiniciar el turno ni el diálogo."""
        from apps.simulator.chat_engine import create_new_door
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        door = create_new_door(mode='DOOR', lang='es')
        door['messages'] = [{'sender': 'user', 'text': 'Hola', 'coach': None}]
        door['turn'] = 1
        session['door_state'] = door
        session['language'] = 'es'
        session.save()

        # Cambiar a inglés vía POST
        resp = self.client.post(reverse('simulator:set_language'), {'language': 'en'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        updated_session = self.client.session
        self.assertEqual(updated_session.get('language'), 'en')

        updated_door = updated_session.get('door_state')
        self.assertEqual(updated_door.get('language'), 'en')
        self.assertTrue(len(updated_door.get('resident_role', '')) > 0)
        self.assertEqual(len(updated_door.get('messages')), 1, "Los mensajes previos deben preservarse.")
        self.assertEqual(updated_door.get('turn'), 1, "El turno actual no debe perderse.")

    def test_set_language_htmx_renders_bilingual_ui(self):
        """Verifica que el cambio de idioma por HTMX devuelva la interfaz con data-lang y textos en inglés."""
        session = self.client.session
        session['prospecting_mode'] = 'DOOR'
        session.save()

        resp = self.client.post(
            reverse('simulator:set_language'),
            {'language': 'en'},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('data-lang="en"', content)
        self.assertIn('Patience', content)
        self.assertIn('Interest', content)
        self.assertIn('Restart', content)
        self.assertIn('id="language-selector-bar"', content)
        self.assertIn('id="mode-selector-bar"', content)

    def test_create_new_door_english(self):
        """Verifica que create_new_door en inglés genere datos y pistas en inglés."""
        from apps.simulator.chat_engine import create_new_door
        door_en = create_new_door(mode='DOOR', lang='en')
        self.assertEqual(door_en['language'], 'en')
        self.assertTrue(len(door_en['resident_role']) > 0)
        self.assertTrue(len(door_en['suggestions']) > 0)
        self.assertTrue(any('TXU' in s or 'second' in s.lower() or 'electric' in s.lower() for s in door_en['suggestions']))

        store_en = create_new_door(mode='STORE', lang='en')
        self.assertEqual(store_en['language'], 'en')
        self.assertTrue(len(store_en['resident_role']) > 0)

    def test_translate_door_state_bidirectional(self):
        """Verifica que translate_door_state traduzca correctamente de ida y vuelta."""
        from apps.simulator.chat_engine import create_new_door, translate_door_state
        door_es = create_new_door(mode='DOOR', lang='es')
        door_en = translate_door_state(door_es, lang='en')
        self.assertEqual(door_en['language'], 'en')
        self.assertTrue(len(door_en['resident_role']) > 0)

        door_es_back = translate_door_state(door_en, lang='es')
        self.assertEqual(door_es_back['language'], 'es')
        self.assertTrue(len(door_es_back['resident_role']) > 0)

    def test_compute_chat_analytics_english(self):
        """Verifica que compute_chat_analytics genere competencias y fortalezas en inglés cuando lang='en'."""
        from apps.simulator.chat_engine import create_new_door, compute_chat_analytics
        door = create_new_door(mode='DOOR', lang='en')
        door['messages'] = [
            {'sender': 'user', 'text': 'Hi, I am from TXU Energy, do you have 15 seconds?', 'coach': 'Good'},
            {'sender': 'prospect', 'text': 'Sure, what do you have?', 'coach': None, 'interest_change': 15, 'patience_change': 5}
        ]
        door['turn'] = 1
        analytics = compute_chat_analytics(door, lang='en')
        self.assertIsNotNone(analytics)
        comp_names = [c['name'] for c in analytics['competencies']]
        self.assertIn('Hook & Opening', comp_names)
        self.assertIn('Connection & Empathy', comp_names)
        self.assertIn('Commercial Diagnosis', comp_names)
        self.assertIn('Objection Handling', comp_names)
        self.assertIn('Closing Assertiveness', comp_names)
        self.assertTrue(len(analytics['strengths']) > 0)
        self.assertTrue(len(analytics['areas_for_improvement']) > 0)

    def test_evaluate_response_local_english(self):
        """Verifica que evaluate_response_local en inglés procese palabras clave y devuelva feedback en inglés."""
        from apps.simulator.chat_engine import create_new_door, evaluate_response_local
        door = create_new_door(mode='DOOR', lang='en')
        door['archetype'] = 'BUSY'
        door['patience'] = 50
        door['interest'] = 20
        door['turn'] = 0
        door['messages'] = []

        res = evaluate_response_local(
            "I only need 15 seconds: with this Texas heat TXU offers Season Pass with 50% summer discount.",
            door,
            lang='en'
        )
        self.assertGreater(res['interest'], 20)
        self.assertEqual(len(res['messages']), 2)
        latest_coach = res['messages'][-1]['coach']
        self.assertTrue('hook:' in latest_coach.lower() or 'time' in latest_coach.lower())

    def test_tts_service_english_voices(self):
        """Verifica que el servicio TTS defina voces neuronales en inglés de alta calidad."""
        from apps.simulator.tts_service import VOICE_MALE_EN, VOICE_FEMALE_EN
        self.assertEqual(VOICE_MALE_EN, "en-US-GuyNeural")
        self.assertEqual(VOICE_FEMALE_EN, "en-US-JennyNeural")

    def test_zero_emojis_in_english_ui(self):
        """Verifica que la interfaz completa en inglés tenga CERO EMOJIS."""
        session = self.client.session
        session['language'] = 'en'
        session.save()
        resp = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        self.assertFalse(bool(emoji_pattern.search(content)), "No deben existir emojis en la interfaz en inglés.")








