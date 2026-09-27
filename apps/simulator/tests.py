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
        self.assertEqual(len(door['messages']), 1)
        self.assertEqual(door['messages'][0]['sender'], 'prospect')

    def test_evaluate_response_busy_archetype(self):
        door = create_new_door()
        door['archetype'] = 'BUSY'
        door['patience'] = 50
        door['interest'] = 20
        door['turn'] = 1

        # Probar respuesta con gancho de 15 segundos sobre aire acondicionado y TXU Season Pass
        updated_door = evaluate_response("Solo le robo 15 segundos: con este calor TXU le da 50% de descuento en verano con Season Pass.", door)
        self.assertGreater(updated_door['interest'], 20)
        self.assertEqual(len(updated_door['messages']), 3)
        self.assertEqual(updated_door['messages'][1]['sender'], 'user')
        self.assertEqual(updated_door['messages'][2]['sender'], 'prospect')
        self.assertIsNotNone(updated_door['messages'][2]['coach'])

    def test_chat_view_loads_clean_ui(self):
        response = self.client.get(reverse('simulator:chat_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Puerta #')
        self.assertContains(response, 'Paciencia')
        self.assertContains(response, 'Interés')
        self.assertContains(response, 'Siguiente Puerta')

        # Verificar que no contenga emojis comunes
        content = response.content.decode('utf-8')
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        self.assertFalse(bool(emoji_pattern.search(content)), "No deben existir emojis en la interfaz.")

    def test_send_message_post_and_htmx(self):
        # 1. Enviar mensaje estándar
        resp = self.client.post(reverse('simulator:send_message'), {
            'message': 'Buenas tardes, disculpe la molestia'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        session = self.client.session
        self.assertIn('door_state', session)
        self.assertGreaterEqual(len(session['door_state']['messages']), 3)

        # 2. Enviar mensaje con cabecera HTMX
        resp_htmx = self.client.post(reverse('simulator:send_message'), {
            'message': 'Solo le robo 15 segundos para revisar su recibo de luz con TXU'
        }, HTTP_HX_REQUEST='true')
        self.assertEqual(resp_htmx.status_code, 200)
        self.assertContains(resp_htmx, 'Análisis del Coach Comercial')

    def test_next_door_and_reset(self):
        # Cargar primera puerta
        self.client.get(reverse('simulator:chat_view'))
        first_door_num = self.client.session['door_state']['door_number']

        # Enviar un mensaje
        self.client.post(reverse('simulator:send_message'), {'message': 'Hola'})
        self.assertEqual(len(self.client.session['door_state']['messages']), 3)

        # Reiniciar chat de la puerta actual
        self.client.post(reverse('simulator:reset_chat'))
        self.assertEqual(len(self.client.session['door_state']['messages']), 1)

        # Siguiente puerta
        self.client.post(reverse('simulator:next_door'))
        self.assertEqual(len(self.client.session['door_state']['messages']), 1)

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
