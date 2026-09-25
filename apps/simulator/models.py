from django.db import models
from django.utils import timezone
from apps.core.models import ProspectorProfile


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('RESIDENTIAL', 'Residencial (Hogares)'),
        ('COMMERCIAL', 'Comercial (Negocios / Pymes)'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='RESIDENTIAL')
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    commission_per_sale = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    commission_per_appointment = models.DecimalField(max_digits=8, decimal_places=2, default=100.00)
    difficulty_multiplier = models.FloatField(default=1.0)
    icon_emoji = models.CharField(max_length=10, default='📡')

    def __str__(self):
        return f"{self.icon_emoji} {self.name} ({self.get_category_display()})"


class Neighborhood(models.Model):
    TARGET_CHOICES = [
        ('RESIDENTIAL', 'Zona Residencial'),
        ('COMMERCIAL', 'Corredor Comercial'),
    ]

    name = models.CharField(max_length=150)
    target_type = models.CharField(max_length=20, choices=TARGET_CHOICES, default='RESIDENTIAL')
    description = models.TextField()
    door_count = models.PositiveIntegerField(default=10)
    open_rate = models.PositiveIntegerField(default=75, help_text="Porcentaje de probabilidad de que alguien abra la puerta (0-100)")
    economic_level = models.CharField(max_length=50, default='Medio')
    difficulty = models.CharField(max_length=20, default='Normal')
    badge_color = models.CharField(max_length=30, default='emerald')

    def __str__(self):
        return f"{self.name} ({self.economic_level})"


class SimulationDay(models.Model):
    profile = models.ForeignKey(ProspectorProfile, on_delete=models.CASCADE, related_name='simulation_days')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Recursos del vendedor durante el día
    energy = models.IntegerField(default=100)  # 0 a 100
    morale = models.IntegerField(default=100)  # 0 a 100
    current_time_str = models.CharField(max_length=20, default='09:00 AM')
    
    # Contadores de la jornada
    doors_knocked = models.PositiveIntegerField(default=0)
    doors_opened = models.PositiveIntegerField(default=0)
    pitches_started = models.PositiveIntegerField(default=0)
    appointments_booked = models.PositiveIntegerField(default=0)
    sales_closed = models.PositiveIntegerField(default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    is_completed = models.BooleanField(default=False)
    coach_summary = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Jornada #{self.id} - {self.neighborhood.name} ({self.created_at.strftime('%d/%m/%Y')})"

    def advance_time(self, minutes=15):
        # Conversión de hora simple para simulación 9:00 AM -> 6:00 PM
        hours_map = [
            '09:00 AM', '09:20 AM', '09:45 AM', '10:15 AM', '10:45 AM',
            '11:15 AM', '11:45 AM', '12:30 PM', '01:15 PM', '02:00 PM',
            '02:45 PM', '03:30 PM', '04:15 PM', '05:00 PM', '05:45 PM', '06:15 PM'
        ]
        # Avanzar según puertas visitadas
        idx = min(self.doors_knocked, len(hours_map) - 1)
        self.current_time_str = hours_map[idx]


class Door(models.Model):
    STATUS_CHOICES = [
        ('UNVISITED', 'Sin visitar'),
        ('NOT_HOME', 'Nadie atiende'),
        ('IN_PROGRESS', 'En conversación'),
        ('REJECTED', 'Rechazado'),
        ('APPOINTMENT', 'Cita agendada'),
        ('SALE_CLOSED', 'Venta cerrada'),
    ]

    ARCHETYPE_CHOICES = [
        ('BUSY', 'El Ocupado / Con Prisa'),
        ('SKEPTICAL', 'El Desconfiado / Escéptico'),
        ('POLITE_EVASIVE', 'El Amable Evasivo ("Déjeme un folleto")'),
        ('HOSTILE', 'El Hostil / Malhumorado'),
        ('IDEAL_LEAD', 'El Prospecto Ideal / Calificado'),
        ('NOT_HOME', 'Nadie en Casa'),
    ]

    simulation_day = models.ForeignKey(SimulationDay, on_delete=models.CASCADE, related_name='doors')
    door_number = models.PositiveIntegerField()
    street_side = models.CharField(max_length=5, default='LEFT') # LEFT or RIGHT
    house_facade = models.CharField(max_length=100, default='🏠 Casa contemporánea')
    resident_name = models.CharField(max_length=100, default='Residente')
    occupant_role = models.CharField(max_length=100, default='Dueño(a) de casa')
    archetype = models.CharField(max_length=30, choices=ARCHETYPE_CHOICES, default='SKEPTICAL')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNVISITED')
    
    # Dinámica de interacción
    interest = models.IntegerField(default=30)  # 0 a 100
    patience = models.IntegerField(default=50)  # 0 a 100
    current_node = models.CharField(max_length=50, default='start')
    dialogue_history = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Puerta #{self.door_number} - {self.resident_name} ({self.get_status_display()})"


class DoorInteractionLog(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE, related_name='logs')
    turn_index = models.PositiveIntegerField(default=1)
    prospect_statement = models.TextField()
    player_choice_text = models.TextField()
    coach_critique = models.TextField()
    tactic_type = models.CharField(max_length=50, default='General')
    interest_change = models.IntegerField(default=0)
    patience_change = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
