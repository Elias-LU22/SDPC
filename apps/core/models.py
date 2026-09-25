from django.db import models
from django.contrib.auth.models import User


class ProspectorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='prospector_profile')
    name = models.CharField(max_length=100, default='Vendedor Novato')
    avatar_emoji = models.CharField(max_length=10, default='🚶‍♂️')
    
    # Progreso de carrera
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    cash_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Habilidades del vendedor (1 a 10)
    empathy = models.PositiveIntegerField(default=3, help_text="Mejora la detección de necesidades y reduce la desconfianza")
    persuasion = models.PositiveIntegerField(default=3, help_text="Aumenta el impacto positivo al rebatir objeciones")
    resilience = models.PositiveIntegerField(default=4, help_text="Reduce el desgaste de moral y energía tras rechazos")
    closing_skill = models.PositiveIntegerField(default=2, help_text="Aumenta la tasa de éxito al pedir la cita o la venta")
    
    # Estadísticas históricas de campo
    total_days_worked = models.PositiveIntegerField(default=0)
    total_doors_knocked = models.PositiveIntegerField(default=0)
    total_doors_opened = models.PositiveIntegerField(default=0)
    total_objections_handled = models.PositiveIntegerField(default=0)
    total_appointments = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    total_rejections = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Nivel {self.level})"

    def add_xp(self, amount):
        self.xp += amount
        # Fórmula de nivel: cada nivel requiere (nivel * 150) XP
        required_xp = self.level * 150
        leveled_up = False
        while self.xp >= required_xp:
            self.xp -= required_xp
            self.level += 1
            leveled_up = True
            # Mejorar habilidades automáticamente al subir de nivel
            if self.level % 2 == 0 and self.empathy < 10:
                self.empathy += 1
            if self.level % 2 != 0 and self.persuasion < 10:
                self.persuasion += 1
            if self.level % 3 == 0 and self.closing_skill < 10:
                self.closing_skill += 1
            if self.resilience < 10:
                self.resilience += 1
            required_xp = self.level * 150
        self.save()
        return leveled_up

    @property
    def conversion_rate(self):
        if self.total_doors_knocked == 0:
            return 0.0
        return round((self.total_sales + self.total_appointments) / self.total_doors_knocked * 100, 1)

    @classmethod
    def get_or_create_default(cls):
        profile = cls.objects.first()
        if not profile:
            profile = cls.objects.create(
                name="Elias (Prospector)",
                avatar_emoji="💼",
                level=1,
                xp=0,
                cash_earned=0.00,
                empathy=3,
                persuasion=3,
                resilience=4,
                closing_skill=2,
            )
        return profile
