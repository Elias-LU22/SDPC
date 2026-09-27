from django.shortcuts import render, redirect
from django.http import HttpResponse
from .chat_engine import create_new_door, evaluate_response

FEMALE_NAMES = {"Carmen Morales", "Patricia Ortiz", "Andrea Salazar", "Beatriz Luna", "Elena Ramos", "Valeria Ríos"}


def ensure_door_gender(door_state):
    """
    Garantiza que door_state contenga el género ('M' o 'F') asignado
    para el prospecto de la puerta, incluso en sesiones existentes.
    """
    if not door_state or not isinstance(door_state, dict):
        return door_state

    if not door_state.get('resident_gender'):
        resident_name = door_state.get('resident_name', '')
        if resident_name in FEMALE_NAMES:
            door_state['resident_gender'] = 'F'
        else:
            door_state['resident_gender'] = 'M'
    return door_state


def chat_view(request):
    """
    Vista principal de pantalla única: simulador de prospección comercial en chat.
    No persiste datos en la base de datos; el estado vive en la sesión del navegador.
    """
    door_state = request.session.get('door_state')
    if not door_state:
        door_state = create_new_door()
        request.session['door_state'] = door_state
    else:
        door_state = ensure_door_gender(door_state)
        request.session['door_state'] = door_state

    return render(request, 'chat.html', {'door': door_state})


def send_message(request):
    """
    Procesa un mensaje enviado por el vendedor (vía formulario o botón de sugerencia).
    Devuelve la interfaz de chat actualizada con HTMX o redirección normal.
    """
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        door_state = request.session.get('door_state')
        if not door_state:
            door_state = create_new_door()
        else:
            door_state = ensure_door_gender(door_state)

        if user_message and door_state.get('status') == 'IN_PROGRESS':
            door_state = evaluate_response(user_message, door_state)
            door_state = ensure_door_gender(door_state)
            request.session['door_state'] = door_state
            request.session.modified = True

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {'door': door_state})

    return redirect('simulator:chat_view')


def next_door(request):
    """
    Cambia a una nueva puerta garantizando diversidad en residentes y temas,
    sin repetir el prospecto ni el arquetipo inmediato anterior.
    """
    door_state = request.session.get('door_state', {})
    current_name = door_state.get('resident_name') if isinstance(door_state, dict) else None
    current_archetype = door_state.get('archetype') if isinstance(door_state, dict) else None
    current_door_num = door_state.get('door_number') if isinstance(door_state, dict) else None

    visited_residents = request.session.get('visited_residents', [])
    if current_name and current_name not in visited_residents:
        visited_residents.append(current_name)

    new_door = create_new_door(
        exclude_name=current_name,
        exclude_archetype=current_archetype,
        visited_names=visited_residents,
        current_door_num=current_door_num
    )

    if new_door['resident_name'] not in visited_residents:
        visited_residents.append(new_door['resident_name'])

    request.session['visited_residents'] = visited_residents
    request.session['door_state'] = new_door
    request.session.modified = True

    if request.headers.get('HX-Request'):
        return render(request, 'chat_content.html', {'door': new_door})

    return redirect('simulator:chat_view')


def reset_chat(request):
    """
    Reinicia el diálogo de la puerta actual desde cero.
    """
    door_state = request.session.get('door_state')
    if door_state:
        door_state = ensure_door_gender(door_state)
        from .chat_engine import ARCHETYPE_DETAILS
        archetype_data = ARCHETYPE_DETAILS[door_state["archetype"]]
        door_state["patience"] = archetype_data["initial_patience"]
        door_state["interest"] = archetype_data["initial_interest"]
        door_state["status"] = "IN_PROGRESS"
        door_state["turn"] = 1
        door_state["porch_observation"] = archetype_data.get("porch_observation", door_state.get("porch_observation", ""))
        door_state["messages"] = [
            {
                "sender": "prospect",
                "text": archetype_data["initial_message"],
                "coach": None,
                "patience_change": 0,
                "interest_change": 0,
            }
        ]
        door_state["suggestions"] = archetype_data["suggestions"]
        request.session['door_state'] = door_state
        request.session.modified = True

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {'door': door_state})

    return redirect('simulator:chat_view')
