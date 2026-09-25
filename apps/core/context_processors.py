from apps.core.models import ProspectorProfile
from apps.simulator.models import SimulationDay


def global_simulator_context(request):
    """
    Inyecta el perfil activo del vendedor y cualquier jornada en progreso en todos los templates.
    """
    profile = ProspectorProfile.get_or_create_default()
    active_day = SimulationDay.objects.filter(profile=profile, is_completed=False).order_by('-id').first()
    return {
        'current_profile': profile,
        'active_day': active_day,
    }
