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

        # El vendedor habla primero con gancho de 15 segundos sobre aire acondicionado y TXU Season Pass
        updated_door = evaluate_response("Solo le robo 15 segundos: con este calor TXU le da 50% de descuento en verano con Season Pass.", door)
        self.assertGreater(updated_door['interest'], 20)
        self.assertEqual(len(updated_door['messages']), 2, "Deben generarse 2 mensajes: vendedor primero y prospecto respondiendo.")
        self.assertEqual(updated_door['messages'][0]['sender'], 'user')
        self.assertEqual(updated_door['messages'][1]['sender'], 'prospect')
        self.assertTrue(updated_door['doorbell_rung'])
        self.assertIn('Gancho de apertura:', updated_door['messages'][1]['coach'])

    def test_ring_doorbell_view(self):
        # Cargar primera puerta
        self.client.get(reverse('simulator:chat_view'))
        self.assertFalse(self.client.session['door_state']['doorbell_rung'])

        # Tocar timbre vía POST
        resp = self.client.post(reverse('simulator:ring_doorbell'), HTTP_HX_REQUEST='true')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.client.session['door_state']['doorbell_rung'])
        self.assertContains(resp, 'Timbre Activado')

    def test_chat_view_loads_clean_ui(self):
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
        self.assertIn('Logo TXU Energy Puerta a Puerta', content)

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



