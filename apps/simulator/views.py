from django.shortcuts import render, redirect
from django.http import HttpResponse
from .chat_engine import create_new_door, evaluate_response


def chat_view(request):
    """
    Vista principal de pantalla única: simulador de prospección comercial en chat.
    No persiste datos en la base de datos; el estado vive en la sesión del navegador.
    """
    door_state = request.session.get('door_state')
    if not door_state:
        door_state = create_new_door()
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

        if user_message and door_state.get('status') == 'IN_PROGRESS':
            door_state = evaluate_response(user_message, door_state)
            request.session['door_state'] = door_state
            request.session.modified = True

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {'door': door_state})

    return redirect('simulator:chat_view')


def next_door(request):
    """
    Cambia a una nueva puerta y prospecto al azar, limpiando el chat anterior.
    """
    door_state = create_new_door()
    request.session['door_state'] = door_state
    request.session.modified = True
    return redirect('simulator:chat_view')


def reset_chat(request):
    """
    Reinicia el diálogo de la puerta actual desde cero.
    """
    door_state = request.session.get('door_state')
    if door_state:
        from .chat_engine import ARCHETYPE_DETAILS
        archetype_data = ARCHETYPE_DETAILS[door_state["archetype"]]
        door_state["patience"] = archetype_data["initial_patience"]
        door_state["interest"] = archetype_data["initial_interest"]
        door_state["status"] = "IN_PROGRESS"
        door_state["turn"] = 1
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

    return redirect('simulator:chat_view')
