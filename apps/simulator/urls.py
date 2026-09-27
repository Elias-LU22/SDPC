from django.urls import path
from . import views

app_name = 'simulator'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send/', views.send_message, name='send_message'),
    path('next/', views.next_door, name='next_door'),
    path('reset/', views.reset_chat, name='reset_chat'),
]
