import random
from django.utils import timezone
from .models import SimulationDay, Door, DoorInteractionLog
from .scenarios import SCENARIOS, get_scenario

RESIDENT_NAMES = [
    "Don Fernando López", "Sra. Carmen Morales", "Ing. Roberto Garza",
    "Mariana Fuentes", "Lic. Agustín Sánchez", "Doña Elena Ramos",
    "Javier Treviño", "Dra. Patricia Ortiz", "Carlos Méndez", "Sra. Beatriz Luna",
    "Guillermo Castro", "Sofía Valenzuela"
]

HOUSE_FACADES = [
    ("🏡 Casa residencial de dos pisos con jardín", "left"),
    ("🏠 Casa contemporánea con portón blanco y timbre", "right"),
    ("🏢 Casa con pequeño despacho / oficina al frente", "left"),
    ("🏡 Casa familiar con coche en cochera y reja alta", "right"),
    ("🏪 Local de abarrotes y miscelánea de barrio", "left"),
    ("🏠 Casa estilo minimalista con interfono", "right"),
    ("🏡 Casa tradicional con macetas y timbre ruidoso", "left"),
    ("🏠 Fachada moderna con cámara de seguridad en la entrada", "right"),
    ("🏪 Taller / Estética con puerta abierta y música", "left"),
    ("🏡 Casa de una planta con reja de herrería", "right"),
]


def create_simulation_day(profile, neighborhood, product):
    """
    Crea una nueva jornada de prospección y genera proceduralmente
    las casas/puertas de la calle según el vecindario.
    """
    day = SimulationDay.objects.create(
        profile=profile,
        neighborhood=neighborhood,
        product=product,
        energy=100,
        morale=100,
        current_time_str='09:00 AM',
    )

    door_count = neighborhood.door_count
    open_rate = neighborhood.open_rate  # ej. 75%

    # Repartición de arquetipos según dificultad del barrio
    archetype_pool = ['BUSY', 'SKEPTICAL', 'POLITE_EVASIVE', 'IDEAL_LEAD']
    if neighborhood.difficulty == 'Avanzado':
        archetype_pool.extend(['HOSTILE', 'HOSTILE', 'BUSY'])
    elif neighborhood.difficulty == 'Intermedio':
        archetype_pool.extend(['HOSTILE', 'SKEPTICAL', 'BUSY'])
    else:
        archetype_pool.extend(['IDEAL_LEAD', 'POLITE_EVASIVE'])

    names_copy = list(RESIDENT_NAMES)
    random.shuffle(names_copy)
    facades_copy = list(HOUSE_FACADES)
    random.shuffle(facades_copy)

    doors_to_create = []
    for i in range(1, door_count + 1):
        # Determinar si hay alguien en casa
        roll_open = random.randint(1, 100)
        if roll_open > open_rate:
            archetype = 'NOT_HOME'
            resident = 'Sin respuesta'
        else:
            archetype = random.choice(archetype_pool)
            resident = names_copy[i % len(names_copy)]

        scenario = get_scenario(archetype)
        facade, side = facades_copy[i % len(facades_copy)]
        
        # Alternar izquierda y derecha en la calle
        street_side = 'LEFT' if (i % 2 != 0) else 'RIGHT'
        door_number = 100 + i * 2 if street_side == 'LEFT' else 101 + i * 2

        doors_to_create.append(
            Door(
                simulation_day=day,
                door_number=door_number,
                street_side=street_side,
                house_facade=facade,
                resident_name=resident,
                archetype=archetype,
                status='UNVISITED',
                interest=scenario['initial_interest'],
                patience=scenario['initial_patience'],
                current_node='start',
                dialogue_history=[]
            )
        )

    Door.objects.bulk_create(doors_to_create)
    return day


def knock_door(door):
    """
    Inicia la interacción con una puerta.
    Avanza contadores de jornada y perfil.
    """
    day = door.simulation_day
    profile = day.profile

    if door.status == 'UNVISITED':
        door.status = 'IN_PROGRESS'
        day.doors_knocked += 1
        profile.total_doors_knocked += 1

        # Consumo de energía al caminar y tocar puerta (reducido si hay buena resiliencia)
        energy_cost = max(2, 6 - int(profile.resilience * 0.4))
        day.energy = max(0, day.energy - energy_cost)
        
        day.advance_time()

        if door.archetype == 'NOT_HOME':
            door.status = 'NOT_HOME'
        else:
            day.doors_opened += 1
            day.pitches_started += 1
            profile.total_doors_opened += 1

        day.save()
        profile.save()
        door.save()

    return door


def process_dialogue_step(door, option_id):
    """
    Procesa la elección del jugador en un nodo de diálogo.
    Aplica modificadores de habilidades del vendedor (empatía, persuasión, cierre, resiliencia),
    actualiza paciencia e interés, registra el historial y gestiona el desenlace.
    """
    day = door.simulation_day
    profile = day.profile
    product = day.product
    scenario = get_scenario(door.archetype)

    current_node_data = scenario['dialogue_nodes'].get(door.current_node)
    if not current_node_data:
        return {'status': 'finished'}

    # Encontrar la opción elegida
    selected_option = None
    for opt in current_node_data.get('options', []):
        if opt['id'] == option_id:
            selected_option = opt
            break

    if not selected_option:
        return {'status': 'invalid_option'}

    # Modificadores de habilidades del prospector
    interest_change = selected_option['interest_change']
    patience_change = selected_option['patience_change']

    # Si la opción es positiva, las habilidades de persuasión y empatía potencian el resultado
    if interest_change > 0:
        boost = int(profile.persuasion * 0.6 + profile.empathy * 0.4)
        interest_change += boost

    # Si hay pérdida de paciencia, la empatía del vendedor mitiga el enojo del prospecto
    if patience_change < 0:
        reduction = int(profile.empathy * 0.5)
        patience_change = min(0, patience_change + reduction)

    # Actualizar medidores de la puerta
    door.interest = max(0, min(100, door.interest + interest_change))
    door.patience = max(0, min(100, door.patience + patience_change))

    # Registrar el intercambio en el historial
    log_entry = {
        'prospect': current_node_data['statement'],
        'player': selected_option['text'],
        'tactic': selected_option['tactic'],
        'coach_feedback': selected_option['coach_feedback'],
        'interest_change': interest_change,
        'patience_change': patience_change,
    }
    history = door.dialogue_history or []
    history.append(log_entry)
    door.dialogue_history = history

    # Registrar en base de datos
    DoorInteractionLog.objects.create(
        door=door,
        turn_index=len(history),
        prospect_statement=current_node_data['statement'],
        player_choice_text=selected_option['text'],
        coach_critique=selected_option['coach_feedback'],
        tactic_type=selected_option['tactic'],
        interest_change=interest_change,
        patience_change=patience_change,
    )
    profile.total_objections_handled += 1

    next_node_id = selected_option['next_node']
    door.current_node = next_node_id

    # Evaluar desenlaces
    outcome = None

    # Si la paciencia se agotó por completo
    if door.patience <= 0 and next_node_id not in ['success_sale', 'success_appointment']:
        door.status = 'REJECTED'
        door.current_node = 'door_rejected_hostile'
        morale_loss = max(4, 18 - profile.resilience * 2)
        day.morale = max(0, day.morale - morale_loss)
        profile.total_rejections += 1
        profile.add_xp(15)
        outcome = 'REJECTED'

    elif next_node_id == 'success_sale':
        door.status = 'SALE_CLOSED'
        day.sales_closed += 1
        comm = product.commission_per_sale
        day.earnings += comm
        profile.cash_earned += comm
        profile.total_sales += 1
        # Subida de moral por éxito
        day.morale = min(100, day.morale + 20)
        profile.add_xp(130)
        outcome = 'SALE_CLOSED'

    elif next_node_id == 'success_appointment':
        door.status = 'APPOINTMENT'
        day.appointments_booked += 1
        comm = product.commission_per_appointment
        day.earnings += comm
        profile.cash_earned += comm
        profile.total_appointments += 1
        day.morale = min(100, day.morale + 10)
        profile.add_xp(70)
        outcome = 'APPOINTMENT'

    elif next_node_id in ['door_rejected_hostile', 'door_rejected_soft', 'door_rejected_polite']:
        door.status = 'REJECTED'
        morale_loss = max(3, 14 - profile.resilience * 2)
        day.morale = max(0, day.morale - morale_loss)
        profile.total_rejections += 1
        profile.add_xp(20)
        outcome = 'REJECTED'

    elif next_node_id == 'not_home_finished':
        door.status = 'NOT_HOME'
        outcome = 'NOT_HOME'

    # Consumo menor de energía por turno de conversación
    day.energy = max(0, day.energy - 2)

    door.save()
    day.save()
    profile.save()

    return {
        'door': door,
        'next_node_id': next_node_id,
        'outcome': outcome,
        'last_log': log_entry,
        'interest': door.interest,
        'patience': door.patience,
    }


def finish_simulation_day(day):
    """
    Finaliza la jornada, computa estadísticas finales y genera el informe pedagógico
    del Sales Coach con consejos aplicados al desempeño real de la jornada.
    """
    if day.is_completed:
        return day

    profile = day.profile
    profile.total_days_worked += 1

    # Cálculo de métricas
    knocked = day.doors_knocked
    opened = day.doors_opened
    sales = day.sales_closed
    citas = day.appointments_booked
    efectividad = round(((sales + citas) / opened * 100), 1) if opened > 0 else 0

    # Construcción de feedback del Coach
    coach_paragraphs = []
    coach_paragraphs.append(f"### 📋 Evaluación de la Jornada por el Coach de Ventas:")
    coach_paragraphs.append(f"- **Puertas tocadas**: {knocked} | **Atendidas**: {opened} | **Citas**: {citas} | **Ventas**: {sales}")
    coach_paragraphs.append(f"- **Tasa de conversión sobre puertas abiertas**: **{efectividad}%**")

    if sales >= 2:
        coach_paragraphs.append("🔥 **¡Rendimiento Sobresaliente!** Supiste conectar el dolor del prospecto con una oferta clara y pediste el cierre con decisión. Tu asertividad en calle fue clave.")
    elif (sales + citas) >= 1:
        coach_paragraphs.append("✅ **Buen trabajo de campo.** Aseguraste prospectos y citas concretas. El seguimiento y la puntualidad serán el 80% de tus comisiones futuras.")
    else:
        coach_paragraphs.append("💡 **Jornada de aprendizaje duro.** En la venta puerta a puerta el rechazo es la materia prima del éxito. Revisa si hablaste demasiado pronto del producto en lugar de preguntar por sus problemas.")

    # Análisis de objeciones cometidas
    logs = DoorInteractionLog.objects.filter(door__simulation_day=day)
    mistake_logs = [l for l in logs if l.patience_change < 0 or l.interest_change < 0]
    if mistake_logs:
        coach_paragraphs.append("#### ⚠️ Errores tácticos recurrentes observados:")
        unique_mistakes = set([l.tactic_type for l in mistake_logs])
        for m in list(unique_mistakes)[:3]:
            coach_paragraphs.append(f"- *{m}*: Cuidado con esta respuesta, provocó caídas de interés o molestia en el prospecto.")

    coach_paragraphs.append("#### 🎯 Regla de oro para tu próxima salida:")
    tips = [
        "1. Nunca dejes un folleto sin antes hacer una pregunta de dolor o asegurar una llamada de seguimiento.",
        "2. Con prospectos ocupados, da un límite de tiempo creíble (15 segundos) y no hables de la historia de tu empresa.",
        "3. Con prospectos escépticos, no digas 'confíe en mí'; usa pruebas sociales de vecinos cercanos.",
        "4. Cuando el cliente diga que le interesa, deja de explicar características y pide el cierre de inmediato."
    ]
    coach_paragraphs.append(random.choice(tips))

    day.coach_summary = "\n\n".join(coach_paragraphs)
    day.is_completed = True
    day.completed_at = timezone.now()
    day.save()
    profile.save()

    return day
