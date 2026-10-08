from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.templatetags.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=static('img/txu_door_logo.svg'), permanent=True)),
    path('', include('apps.simulator.urls')),
]
