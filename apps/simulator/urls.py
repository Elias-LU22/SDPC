from django.urls import path
from . import views

app_name = 'simulator'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send/', views.send_message, name='send_message'),
    path('ring/', views.ring_doorbell, name='ring_doorbell'),
    path('tts/', views.tts_view, name='tts_view'),
    path('next/', views.next_door, name='next_door'),
    path('reset/', views.reset_chat, name='reset_chat'),
    path('mode/', views.set_prospecting_mode, name='set_prospecting_mode'),
]

