from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import SimulationDay, Door, Product, Neighborhood, DoorInteractionLog
from .engine import create_simulation_day, knock_door, process_dialogue_step, finish_simulation_day
from .scenarios import get_scenario
from apps.core.models import ProspectorProfile


def start_day(request):
    """
    Inicia una nueva jornada de prospección con el barrio y producto seleccionados.
    """
    if request.method == 'POST':
        neighborhood_id = request.POST.get('neighborhood_id')
        product_id = request.POST.get('product_id')

        neighborhood = get_object_or_404(Neighborhood, id=neighborhood_id)
        product = get_object_or_404(Product, id=product_id)
        profile = ProspectorProfile.get_or_create_default()

        # Si ya hay una jornada activa, redirigir a ella o cerrarla
        existing_day = SimulationDay.objects.filter(profile=profile, is_completed=False).first()
        if existing_day:
            messages.info(request, "Ya tenías una jornada en curso. Te hemos dirigido a ella.")
            return redirect('simulator:street_view', day_id=existing_day.id)

        day = create_simulation_day(profile, neighborhood, product)
        messages.success(request, f"¡Has llegado a {neighborhood.name}! Es hora de empezar a tocar puertas.")
        return redirect('simulator:street_view', day_id=day.id)

    return redirect('core:dashboard')


def street_view(request, day_id):
    """
    Vista del vecindario / calle: muestra las casas a la izquierda y derecha,
    recursos de energía/moral y el estado de cada puerta.
    """
    day = get_object_or_404(SimulationDay, id=day_id)
    doors = day.doors.all().order_by('door_number')
    
    # Separar casas por acera para vista urbana realista
    left_doors = [d for d in doors if d.street_side == 'LEFT']
    right_doors = [d for d in doors if d.street_side == 'RIGHT']

    # Porcentaje de puertas visitadas
    total_doors = doors.count()
    visited_doors = doors.exclude(status='UNVISITED').count()
    progress_pct = int((visited_doors / total_doors) * 100) if total_doors > 0 else 0

    all_completed = visited_doors == total_doors
    is_exhausted = day.energy <= 0 or day.morale <= 0

    context = {
        'day': day,
        'doors': doors,
        'left_doors': left_doors,
        'right_doors': right_doors,
        'progress_pct': progress_pct,
        'visited_doors': visited_doors,
        'total_doors': total_doors,
        'all_completed': all_completed,
        'is_exhausted': is_exhausted,
    }
    return render(request, 'simulator/street_view.html', context)


def knock_door_view(request, door_id):
    """
    Acción de llamar a la puerta o tocar el timbre.
    """
    door = get_object_or_404(Door, id=door_id)
    day = door.simulation_day

    if day.is_completed:
        messages.warning(request, "Esta jornada ya ha concluido.")
        return redirect('simulator:day_summary', day_id=day.id)

    if day.energy <= 0:
        messages.error(request, "¡Estás agotado! No te queda energía para seguir prospectando hoy. Termina la jornada.")
        return redirect('simulator:street_view', day_id=day.id)

    # Iniciar interacción
    knock_door(door)
    return redirect('simulator:door_encounter', door_id=door.id)


def door_encounter(request, door_id):
    """
    Vista cara a cara de la puerta: muestra al prospecto, medidores y opciones de diálogo.
    """
    door = get_object_or_404(Door, id=door_id)
    day = door.simulation_day
    scenario = get_scenario(door.archetype)

    current_node_data = scenario['dialogue_nodes'].get(door.current_node, {})
    is_resolved = door.status in ['SALE_CLOSED', 'APPOINTMENT', 'REJECTED', 'NOT_HOME']

    context = {
        'door': door,
        'day': day,
        'scenario': scenario,
        'node_data': current_node_data,
        'is_resolved': is_resolved,
        'last_log': door.dialogue_history[-1] if door.dialogue_history else None,
    }
    return render(request, 'simulator/door_encounter.html', context)


def dialogue_step_view(request, door_id):
    """
    Procesa un turno de conversación (HTMX o POST estándar).
    """
    door = get_object_or_404(Door, id=door_id)
    day = door.simulation_day

    if request.method == 'POST':
        option_id = request.POST.get('option_id')
        step_result = process_dialogue_step(door, option_id)
        
        # Si la petición proviene de HTMX, renderizamos solo el fragmento dinámico
        if request.headers.get('HX-Request'):
            scenario = get_scenario(door.archetype)
            current_node_data = scenario['dialogue_nodes'].get(door.current_node, {})
            is_resolved = door.status in ['SALE_CLOSED', 'APPOINTMENT', 'REJECTED', 'NOT_HOME']

            context = {
                'door': door,
                'day': day,
                'scenario': scenario,
                'node_data': current_node_data,
                'is_resolved': is_resolved,
                'last_log': door.dialogue_history[-1] if door.dialogue_history else None,
            }
            return render(request, 'simulator/door_dialog_fragment.html', context)

    return redirect('simulator:door_encounter', door_id=door.id)


def finish_day(request, day_id):
    """
    Concluye la jornada activa y lleva al informe de desempeño.
    """
    day = get_object_or_404(SimulationDay, id=day_id)
    if not day.is_completed:
        finish_simulation_day(day)
        messages.success(request, "¡Jornada finalizada con éxito! Revisa tu reporte de resultados.")
    return redirect('simulator:day_summary', day_id=day.id)


def day_summary(request, day_id):
    """
    Vista de resumen final: funnel de conversión, comisiones, XP y feedback pedagógico.
    """
    day = get_object_or_404(SimulationDay, id=day_id)
    if not day.is_completed:
        finish_simulation_day(day)

    # Cálculo de métricas para embudo visual
    opened_rate = round((day.doors_opened / day.doors_knocked * 100), 1) if day.doors_knocked > 0 else 0
    pitch_rate = round((day.pitches_started / day.doors_knocked * 100), 1) if day.doors_knocked > 0 else 0
    success_rate = round(((day.sales_closed + day.appointments_booked) / day.doors_knocked * 100), 1) if day.doors_knocked > 0 else 0

    logs = DoorInteractionLog.objects.filter(door__simulation_day=day).select_related('door')

    context = {
        'day': day,
        'opened_rate': opened_rate,
        'pitch_rate': pitch_rate,
        'success_rate': success_rate,
        'logs': logs,
    }
    return render(request, 'simulator/day_summary.html', context)
