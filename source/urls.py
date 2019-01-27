from django.contrib import admin
from django.urls import path, include
from candelabrus import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('fo/', include('fons.urls')),
    path('dj/', include('dejure.urls')),
    path('dw/', include('darwin.urls')),
    path('nz/', include('nietz.urls')),
    path('mk/', include('mereokratos.urls')),
]
