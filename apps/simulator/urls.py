from django.urls import path
from . import views

app_name = 'simulator'

urlpatterns = [
    path('start/', views.start_day, name='start_day'),
    path('day/<int:day_id>/', views.street_view, name='street_view'),
    path('door/<int:door_id>/knock/', views.knock_door_view, name='knock_door'),
    path('door/<int:door_id>/', views.door_encounter, name='door_encounter'),
    path('door/<int:door_id>/step/', views.dialogue_step_view, name='dialogue_step'),
    path('day/<int:day_id>/finish/', views.finish_day, name='finish_day'),
    path('day/<int:day_id>/summary/', views.day_summary, name='day_summary'),
]
