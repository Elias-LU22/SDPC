from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ProspectorProfile
from apps.simulator.models import Product, Neighborhood, SimulationDay


def dashboard(request):
    """
    Vista principal: resumen de carrera del asesor comercial, métricas acumuladas,
    selección de campaña/producto y barrio para iniciar nueva jornada de venta directa.
    """
    profile = ProspectorProfile.get_or_create_default()
    products = Product.objects.all()
    neighborhoods = Neighborhood.objects.all()
    recent_days = SimulationDay.objects.filter(profile=profile, is_completed=True).order_by('-completed_at')[:5]
    
    context = {
        'profile': profile,
        'products': products,
        'neighborhoods': neighborhoods,
        'recent_days': recent_days,
        'xp_to_next_level': profile.level * 150,
        'xp_progress_pct': min(100, int((profile.xp / (profile.level * 150)) * 100)),
    }
    return render(request, 'core/dashboard.html', context)


def upgrade_skill(request, skill_name):
    """
    Permite al jugador invertir comisiones acumuladas ($) para entrenar una habilidad de venta.
    """
    if request.method == 'POST':
        profile = ProspectorProfile.get_or_create_default()
        cost = Decimal('300.00')  # Costo en comisiones por punto de habilidad
        
        valid_skills = ['empathy', 'persuasion', 'resilience', 'closing_skill']
        if skill_name in valid_skills:
            current_val = getattr(profile, skill_name)
            if current_val >= 10:
                messages.warning(request, f"¡La habilidad {skill_name} ya está en su nivel máximo (10)!")
            elif profile.cash_earned < cost:
                messages.error(request, f"Comisiones insuficientes. Necesitas ${cost:,.2f} para este entrenamiento intensivo.")
            else:
                profile.cash_earned -= cost
                setattr(profile, skill_name, current_val + 1)
                profile.save()
                skill_labels = {
                    'empathy': 'Empatía y Escucha Activa',
                    'persuasion': 'Persuasión y Refutación',
                    'resilience': 'Resiliencia Emocional',
                    'closing_skill': 'Técnica de Cierre'
                }
                messages.success(request, f"¡Entrenamiento completado! +1 a {skill_labels.get(skill_name, skill_name)}.")
        
    return redirect('core:dashboard')


def reset_career(request):
    """
    Reinicia el progreso de carrera para comenzar una nueva partida limpia.
    """
    if request.method == 'POST':
        profile = ProspectorProfile.get_or_create_default()
        profile.level = 1
        profile.xp = 0
        profile.cash_earned = 0.00
        profile.empathy = 3
        profile.persuasion = 3
        profile.resilience = 4
        profile.closing_skill = 2
        profile.total_days_worked = 0
        profile.total_doors_knocked = 0
        profile.total_doors_opened = 0
        profile.total_objections_handled = 0
        profile.total_appointments = 0
        profile.total_sales = 0
        profile.total_rejections = 0
        profile.save()
        
        # Eliminar jornadas anteriores
        SimulationDay.objects.filter(profile=profile).delete()
        messages.info(request, "Tu historial de carrera y estadísticas han sido reiniciados a cero.")
        
    return redirect('core:dashboard')
