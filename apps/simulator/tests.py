from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import ProspectorProfile
from apps.simulator.models import Product, Neighborhood, SimulationDay, Door, DoorInteractionLog
from apps.simulator.engine import create_simulation_day, knock_door, process_dialogue_step, finish_simulation_day


class ProspectorSimulatorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = ProspectorProfile.get_or_create_default()
        self.product = Product.objects.create(
            name="Fibra Test",
            category="RESIDENTIAL",
            tagline="Test Internet",
            description="Fibra de prueba",
            commission_per_sale=500.0,
            commission_per_appointment=100.0,
            icon_emoji="🚀"
        )
        self.neighborhood = Neighborhood.objects.create(
            name="Barrio Test",
            target_type="RESIDENTIAL",
            description="Zona de prueba",
            door_count=6,
            open_rate=80,
            economic_level="Medio",
            difficulty="Fácil"
        )

    def test_profile_xp_and_level_up(self):
        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.xp, 0)
        
        # Agregar 160 XP (nivel 1 requiere 150)
        leveled_up = self.profile.add_xp(160)
        self.assertTrue(leveled_up)
        self.assertEqual(self.profile.level, 2)
        self.assertEqual(self.profile.xp, 10)

    def test_create_simulation_day_generates_doors(self):
        day = create_simulation_day(self.profile, self.neighborhood, self.product)
        self.assertIsNotNone(day.id)
        self.assertEqual(day.doors.count(), 6)
        self.assertEqual(day.energy, 100)
        self.assertEqual(day.morale, 100)
        
        # Comprobar que hay casas en ambos lados
        left_doors = day.doors.filter(street_side='LEFT').count()
        right_doors = day.doors.filter(street_side='RIGHT').count()
        self.assertGreater(left_doors, 0)
        self.assertGreater(right_doors, 0)

    def test_knock_door_flow(self):
        day = create_simulation_day(self.profile, self.neighborhood, self.product)
        door = day.doors.first()
        self.assertEqual(door.status, 'UNVISITED')
        
        knocked_door = knock_door(door)
        self.assertIn(knocked_door.status, ['IN_PROGRESS', 'NOT_HOME'])
        day.refresh_from_db()
        self.assertEqual(day.doors_knocked, 1)
        self.assertLess(day.energy, 100)

    def test_process_dialogue_step(self):
        day = create_simulation_day(self.profile, self.neighborhood, self.product)
        door = day.doors.first()
        # Forzar un arquetipo conocido
        door.archetype = 'BUSY'
        door.current_node = 'start'
        door.status = 'IN_PROGRESS'
        door.save()

        # Probar opción efectiva
        res = process_dialogue_step(door, 'opt_1_good')
        door.refresh_from_db()
        self.assertEqual(res['next_node_id'], 'busy_hooked')
        self.assertEqual(door.current_node, 'busy_hooked')
        self.assertGreater(door.interest, 25)
        self.assertEqual(len(door.dialogue_history), 1)
        self.assertEqual(DoorInteractionLog.objects.filter(door=door).count(), 1)

    def test_successful_sale_outcome(self):
        day = create_simulation_day(self.profile, self.neighborhood, self.product)
        door = day.doors.first()
        door.archetype = 'IDEAL_LEAD'
        door.current_node = 'ideal_shared_pain'
        door.status = 'IN_PROGRESS'
        door.save()

        # Seleccionar cierre directo
        res = process_dialogue_step(door, 'opt_ideal_direct_close')
        door.refresh_from_db()
        day.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(door.status, 'SALE_CLOSED')
        self.assertEqual(day.sales_closed, 1)
        self.assertEqual(day.earnings, 500.0)
        self.assertEqual(self.profile.total_sales, 1)

    def test_finish_simulation_day(self):
        day = create_simulation_day(self.profile, self.neighborhood, self.product)
        day.doors_knocked = 5
        day.doors_opened = 4
        day.sales_closed = 1
        day.save()

        completed_day = finish_simulation_day(day)
        self.assertTrue(completed_day.is_completed)
        self.assertIsNotNone(completed_day.completed_at)
        self.assertIn("Evaluación de la Jornada", completed_day.coach_summary)

    def test_http_views(self):
        # 1. Dashboard
        resp = self.client.get(reverse('core:dashboard'))
        self.assertEqual(resp.status_code, 200)

        # 2. Iniciar Jornada
        resp = self.client.post(reverse('simulator:start_day'), {
            'neighborhood_id': self.neighborhood.id,
            'product_id': self.product.id
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        
        day = SimulationDay.objects.filter(profile=self.profile).last()
        self.assertIsNotNone(day)

        # 3. Vista de Calle
        resp = self.client.get(reverse('simulator:street_view', args=[day.id]))
        self.assertEqual(resp.status_code, 200)

        # 4. Tocar Puerta
        door = day.doors.first()
        resp = self.client.get(reverse('simulator:knock_door', args=[door.id]), follow=True)
        self.assertEqual(resp.status_code, 200)

        # 5. Encuentro de Puerta
        resp = self.client.get(reverse('simulator:door_encounter', args=[door.id]))
        self.assertEqual(resp.status_code, 200)

        # 6. Petición HTMX en paso de diálogo
        resp_htmx = self.client.post(
            reverse('simulator:dialogue_step', args=[door.id]),
            {'option_id': 'opt_1_good'},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(resp_htmx.status_code, 200)
        self.assertContains(resp_htmx, 'Paciencia del Residente')
        self.assertContains(resp_htmx, 'Interés Comercial')

        # 7. Finalizar Jornada
        resp = self.client.post(reverse('simulator:finish_day', args=[day.id]), follow=True)
        self.assertEqual(resp.status_code, 200)

        # 8. Resumen de Jornada
        resp = self.client.get(reverse('simulator:day_summary', args=[day.id]))
        self.assertEqual(resp.status_code, 200)

    def test_skill_upgrade_with_cash(self):
        self.profile.cash_earned = 400.00
        self.profile.save()
        initial_empathy = self.profile.empathy

        resp = self.client.post(reverse('core:upgrade_skill', args=['empathy']), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.empathy, initial_empathy + 1)
        self.assertEqual(self.profile.cash_earned, 100.00)

    def test_skill_upgrade_insufficient_cash(self):
        self.profile.cash_earned = 50.00
        self.profile.save()
        initial_empathy = self.profile.empathy

        resp = self.client.post(reverse('core:upgrade_skill', args=['empathy']), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.empathy, initial_empathy)
        self.assertEqual(self.profile.cash_earned, 50.00)

    def test_reset_career(self):
        self.profile.level = 5
        self.profile.cash_earned = 1500.00
        self.profile.save()

        resp = self.client.post(reverse('core:reset_career'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.level, 1)
        self.assertEqual(self.profile.cash_earned, 0.00)
