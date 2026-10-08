from django.shortcuts import render, redirect
from django.http import HttpResponse
from .chat_engine import (
    create_new_door,
    evaluate_response,
    translate_door_state,
    compute_chat_analytics,
    ARCHETYPE_DETAILS,
    RETAIL_SHOPPERS
)
from .i18n_strings import (
    get_ui_strings,
    get_archetype_info,
    get_shopper_info,
    get_resident_role
)

FEMALE_NAMES = {
    "Carmen Morales", "Patricia Ortiz", "Andrea Salazar", "Beatriz Luna",
    "Elena Ramos", "Valeria Ríos", "Marcela Beltrán", "Laura Cárdenas",
    "Gloria Hinojosa", "Verónica Trejo"
}


def get_session_language(request):
    """Retorna el código de idioma activo en la sesión ('es' o 'en')."""
    lang = request.session.get('language', 'es')
    if isinstance(lang, str) and lang.strip().lower().startswith('en'):
        return 'en'
    return 'es'


def ensure_door_gender(door_state):
    """
    Garantiza que door_state contenga el género ('M' o 'F') asignado
    para el prospecto de la puerta o tienda, incluso en sesiones existentes.
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


def set_language(request):
    """
    Cambia el idioma activo de la aplicación ('es' o 'en').
    Actualiza la sesión, traduce el door_state en curso para que no pierda el turno,
    y retorna la vista parcial (HTMX) o redirecciona.
    """
    if request.method == 'POST':
        lang = request.POST.get('language', 'es').strip().lower()
        if lang not in ['es', 'en']:
            lang = 'es'
        request.session['language'] = lang

        door_state = request.session.get('door_state')
        if door_state:
            door_state = translate_door_state(door_state, lang=lang)
            door_state['language'] = lang
            request.session['door_state'] = door_state
        request.session.modified = True

        mode = request.session.get('prospecting_mode', 'RANDOM')
        t = get_ui_strings(lang)

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {
                'door': door_state,
                'prospecting_mode': mode,
                'language': lang,
                't': t
            })

    return redirect('simulator:chat_view')


def chat_view(request):
    """
    Vista principal de pantalla única: simulador de prospección comercial en chat.
    No persiste datos en la base de datos; el estado vive en la sesión del navegador.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    mode = request.session.get('prospecting_mode', 'RANDOM')
    door_state = request.session.get('door_state')
    if not door_state:
        door_state = create_new_door(mode=mode, lang=lang)
        door_state = ensure_door_gender(door_state)
        door_state['language'] = lang
        request.session['door_state'] = door_state
        request.session['prospecting_mode'] = mode
    else:
        door_state = ensure_door_gender(door_state)
        request.session['door_state'] = door_state

    return render(request, 'chat.html', {
        'door': door_state,
        'prospecting_mode': mode,
        'language': lang,
        't': t
    })


def set_prospecting_mode(request):
    """
    Cambia la modalidad de prospección activa ('RANDOM', 'DOOR', 'STORE')
    y genera inmediatamente un nuevo prospecto acorde al modo elegido.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    if request.method == 'POST':
        mode = request.POST.get('mode', 'RANDOM').upper()
        if mode not in ['RANDOM', 'DOOR', 'STORE']:
            mode = 'RANDOM'
        request.session['prospecting_mode'] = mode

        door_state = request.session.get('door_state', {})
        current_name = door_state.get('resident_name') if isinstance(door_state, dict) else None
        current_archetype = door_state.get('archetype') if isinstance(door_state, dict) else None
        current_door_num = door_state.get('door_number') if isinstance(door_state, dict) else None

        visited_residents = request.session.get('visited_residents', [])
        if current_name and current_name not in visited_residents:
            visited_residents.append(current_name)

        new_door = create_new_door(
            mode=mode,
            exclude_name=current_name,
            exclude_archetype=current_archetype,
            visited_names=visited_residents,
            current_door_num=current_door_num,
            lang=lang
        )
        new_door = ensure_door_gender(new_door)
        new_door['language'] = lang

        if new_door['resident_name'] not in visited_residents:
            visited_residents.append(new_door['resident_name'])

        request.session['visited_residents'] = visited_residents
        request.session['door_state'] = new_door
        request.session.modified = True

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {
                'door': new_door,
                'prospecting_mode': mode,
                'language': lang,
                't': t
            })

    return redirect('simulator:chat_view')


def send_message(request):
    """
    Procesa un mensaje enviado por el vendedor (vía formulario o botón de sugerencia).
    Devuelve la interfaz de chat actualizada con HTMX o redirección normal.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    mode = request.session.get('prospecting_mode', 'RANDOM')
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        door_state = request.session.get('door_state')
        if not door_state:
            door_state = create_new_door(mode=mode, lang=lang)
            door_state['language'] = lang
        else:
            door_state = ensure_door_gender(door_state)

        if user_message and door_state.get('status') == 'IN_PROGRESS':
            door_state = evaluate_response(user_message, door_state, lang=lang)
            door_state = ensure_door_gender(door_state)
            door_state['language'] = lang
            if door_state.get('status') in ['SALE_CLOSED', 'APPOINTMENT', 'REJECTED'] and not door_state.get('analytics'):
                door_state['analytics'] = compute_chat_analytics(door_state, lang=lang)
            request.session['door_state'] = door_state
            request.session.modified = True

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {
                'door': door_state,
                'prospecting_mode': mode,
                'language': lang,
                't': t
            })

    return redirect('simulator:chat_view')


def next_door(request):
    """
    Cambia a una nueva puerta o tienda garantizando diversidad en residentes y temas,
    sin repetir el prospecto ni el arquetipo inmediato anterior.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    mode = request.session.get('prospecting_mode', 'RANDOM')
    door_state = request.session.get('door_state', {})
    current_name = door_state.get('resident_name') if isinstance(door_state, dict) else None
    current_archetype = door_state.get('archetype') if isinstance(door_state, dict) else None
    current_door_num = door_state.get('door_number') if isinstance(door_state, dict) else None

    visited_residents = request.session.get('visited_residents', [])
    if current_name and current_name not in visited_residents:
        visited_residents.append(current_name)

    new_door = create_new_door(
        mode=mode,
        exclude_name=current_name,
        exclude_archetype=current_archetype,
        visited_names=visited_residents,
        current_door_num=current_door_num,
        lang=lang
    )
    new_door = ensure_door_gender(new_door)
    new_door['language'] = lang

    if new_door['resident_name'] not in visited_residents:
        visited_residents.append(new_door['resident_name'])

    request.session['visited_residents'] = visited_residents
    request.session['door_state'] = new_door
    request.session.modified = True

    if request.headers.get('HX-Request'):
        return render(request, 'chat_content.html', {
            'door': new_door,
            'prospecting_mode': mode,
            'language': lang,
            't': t
        })

    return redirect('simulator:chat_view')


def ring_doorbell(request):
    """
    Registra el timbre sonado en la puerta actual (o abordaje en tienda) y devuelve la vista actualizada.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    mode = request.session.get('prospecting_mode', 'RANDOM')
    door_state = request.session.get('door_state')
    if not door_state:
        door_state = create_new_door(mode=mode, lang=lang)
    else:
        door_state = ensure_door_gender(door_state)

    door_state['doorbell_rung'] = True
    door_state['language'] = lang
    request.session['door_state'] = door_state
    request.session.modified = True

    if request.headers.get('HX-Request'):
        return render(request, 'chat_content.html', {
            'door': door_state,
            'prospecting_mode': mode,
            'language': lang,
            't': t
        })

    return redirect('simulator:chat_view')


def reset_chat(request):
    """
    Reinicia el diálogo de la puerta o tienda actual desde cero en el estado inicial de llegada.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    mode = request.session.get('prospecting_mode', 'RANDOM')
    door_state = request.session.get('door_state')
    if door_state:
        door_state = ensure_door_gender(door_state)
        arch_data = ARCHETYPE_DETAILS[door_state["archetype"]]
        door_state["patience"] = arch_data["initial_patience"]
        door_state["interest"] = arch_data["initial_interest"]
        door_state["status"] = "IN_PROGRESS"
        door_state["turn"] = 0
        door_state["doorbell_rung"] = False
        door_state["messages"] = []
        door_state["language"] = lang
        door_state.pop("analytics", None)

        if lang == 'en':
            arch_info = get_archetype_info(door_state["archetype"], 'en')
            if door_state.get("encounter_type") == "STORE":
                shopper_info = get_shopper_info(door_state.get("resident_name"), 'en')
                door_state["porch_observation"] = shopper_info.get("store_observation", "")
                door_state["context_observation"] = shopper_info.get("store_observation", "")
                door_state["suggestions"] = shopper_info.get("opening_hooks", arch_info.get("opening_hooks", []))
            else:
                door_state["porch_observation"] = arch_info.get("porch_observation", "")
                door_state["context_observation"] = arch_info.get("porch_observation", "")
                door_state["suggestions"] = arch_info.get("opening_hooks", arch_info.get("suggestions", []))
        else:
            if door_state.get("encounter_type") == "STORE":
                shopper_match = next((s for s in RETAIL_SHOPPERS if s["name"] == door_state.get("resident_name")), None)
                if shopper_match:
                    door_state["porch_observation"] = shopper_match["store_observation"]
                    door_state["context_observation"] = shopper_match["store_observation"]
                    door_state["suggestions"] = shopper_match.get("opening_hooks", arch_data["suggestions"])
                else:
                    door_state["porch_observation"] = door_state.get("porch_observation", "")
                    door_state["context_observation"] = door_state.get("porch_observation", "")
                    door_state["suggestions"] = arch_data.get("opening_hooks", arch_data["suggestions"])
            else:
                door_state["porch_observation"] = arch_data.get("porch_observation", door_state.get("porch_observation", ""))
                door_state["context_observation"] = arch_data.get("porch_observation", door_state.get("porch_observation", ""))
                door_state["suggestions"] = arch_data.get("opening_hooks", arch_data["suggestions"])

        request.session['door_state'] = door_state
        request.session.modified = True

        if request.headers.get('HX-Request'):
            return render(request, 'chat_content.html', {
                'door': door_state,
                'prospecting_mode': mode,
                'language': lang,
                't': t
            })

    return redirect('simulator:chat_view')


def finish_chat(request):
    """
    Concluye voluntariamente la sesión de diálogo actual para generar el informe analítico
    completo de desempeño comercial y áreas de mejora.
    """
    lang = get_session_language(request)
    t = get_ui_strings(lang)
    mode = request.session.get('prospecting_mode', 'RANDOM')
    door_state = request.session.get('door_state')
    if door_state:
        door_state = ensure_door_gender(door_state)
        if door_state.get('status') == 'IN_PROGRESS':
            door_state['status'] = 'COMPLETED'
        door_state['language'] = lang
        door_state['analytics'] = compute_chat_analytics(door_state, lang=lang)
        request.session['door_state'] = door_state
        request.session.modified = True

    if request.headers.get('HX-Request'):
        return render(request, 'chat_content.html', {
            'door': door_state,
            'prospecting_mode': mode,
            'language': lang,
            't': t
        })

    return redirect('simulator:chat_view')


def tts_view(request):
    """
    Endpoint para streaming de audio neuronal MP3 (Microsoft Edge TTS).
    Recibe text, gender y lang vía GET. Retorna audio/mpeg o HTTP 204 para fallback del cliente.
    """
    text = request.GET.get('text', '').strip()
    gender = request.GET.get('gender', 'M').strip()
    lang = request.GET.get('lang', '').strip().lower()
    if not lang:
        lang = get_session_language(request)

    if not text:
        return HttpResponse(status=204)

    from .tts_service import synthesize_speech
    audio_data = synthesize_speech(text, gender, lang=lang)

    if audio_data:
        response = HttpResponse(audio_data, content_type='audio/mpeg')
        response['Cache-Control'] = 'public, max-age=86400'
        return response

    return HttpResponse(status=204)
