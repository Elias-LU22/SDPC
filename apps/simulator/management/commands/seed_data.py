from django.core.management.base import BaseCommand
from apps.simulator.models import Product, Neighborhood
from apps.core.models import ProspectorProfile


class Command(BaseCommand):
    help = 'Inicializa productos, barrios y perfil inicial para el simulador de prospección'

    def handle(self, *args, **options):
        # Crear perfil inicial
        profile = ProspectorProfile.get_or_create_default()
        self.stdout.write(self.style.SUCCESS(f"Perfil verificado: {profile.name}"))

        # Productos
        products_data = [
            {
                'name': 'Fibra Óptica Ultra 500 Mbps',
                'category': 'RESIDENTIAL',
                'tagline': 'Internet simétrico sin cortes con instalación gratuita hoy',
                'description': 'Servicio de internet de fibra óptica directo al hogar con módem Wi-Fi 6 de última generación. Ideal para familias con teletrabajo, streaming y gamers.',
                'commission_per_sale': 450.00,
                'commission_per_appointment': 80.00,
                'difficulty_multiplier': 1.0,
                'icon_emoji': '🚀',
            },
            {
                'name': 'Alarma y Seguridad Inteligente 24/7',
                'category': 'RESIDENTIAL',
                'tagline': 'Protección perimetral con cámaras HD y respuesta armada inmediata',
                'description': 'Kit de seguridad disuasorio con sensores de apertura, detección de movimiento infrarrojo y enlace a central de monitoreo con botón de pánico en app móvil.',
                'commission_per_sale': 750.00,
                'commission_per_appointment': 150.00,
                'difficulty_multiplier': 1.2,
                'icon_emoji': '🛡️',
            },
            {
                'name': 'Terminal Punto de Venta (TPV) SmartPay',
                'category': 'COMMERCIAL',
                'tagline': 'Cobra con tarjeta y pagos QR con la comisión más baja (1.5%) y depósito en 24h',
                'description': 'Dispositivo inalámbrico 4G con pantalla táctil e impresora térmica de tickets para pequeños y medianos comercios. Sin renta mensual obligatoria.',
                'commission_per_sale': 600.00,
                'commission_per_appointment': 120.00,
                'difficulty_multiplier': 1.1,
                'icon_emoji': '💳',
            },
            {
                'name': 'Paneles Solares Residenciales ZeroWatt',
                'category': 'RESIDENTIAL',
                'tagline': 'Reduce hasta un 90% tu recibo de luz sin inversión inicial fuerte',
                'description': 'Sistema fotovoltaico interconectado a la red con financiamiento a la medida y garantía de generación por 25 años.',
                'commission_per_sale': 1800.00,
                'commission_per_appointment': 300.00,
                'difficulty_multiplier': 1.4,
                'icon_emoji': '☀️',
            },
        ]

        for p_data in products_data:
            obj, created = Product.objects.update_or_create(
                name=p_data['name'],
                defaults=p_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Producto creado: {obj.name}"))

        # Barrios / Zonas
        neighborhoods_data = [
            {
                'name': 'Fraccionamiento Las Palmas',
                'target_type': 'RESIDENTIAL',
                'economic_level': 'Medio - Alto',
                'description': 'Fraccionamiento residencial tranquilo con casas de 2 plantas y jardines. Familias con hijos pequeños y profesionistas. Hay bastante gente durante las tardes.',
                'door_count': 10,
                'open_rate': 80,
                'difficulty': 'Fácil',
                'badge_color': 'emerald',
            },
            {
                'name': 'Colonia San Jerónimo',
                'target_type': 'RESIDENTIAL',
                'economic_level': 'Medio',
                'description': 'Barrio tradicional con rejas altas y vecinos precavidos ante desconocidos. Requiere generar confianza de inmediato y demostrar seriedad.',
                'door_count': 12,
                'open_rate': 70,
                'difficulty': 'Intermedio',
                'badge_color': 'amber',
            },
            {
                'name': 'Corredor Comercial Juárez',
                'target_type': 'COMMERCIAL',
                'economic_level': 'Comercial Pymes',
                'description': 'Avenida concurrida con abarrotes, talleres, estéticas, papelerías y fondas. Los encargados están muy ocupados atendiendo a sus clientes.',
                'door_count': 10,
                'open_rate': 90,
                'difficulty': 'Avanzado',
                'badge_color': 'rose',
            },
        ]

        for n_data in neighborhoods_data:
            obj, created = Neighborhood.objects.update_or_create(
                name=n_data['name'],
                defaults=n_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Barrio creado: {obj.name}"))

        self.stdout.write(self.style.SUCCESS("Datos iniciales del simulador sembrados correctamente."))
