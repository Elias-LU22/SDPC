from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upgrade-skill/<str:skill_name>/', views.upgrade_skill, name='upgrade_skill'),
    path('reset-career/', views.reset_career, name='reset_career'),
]
