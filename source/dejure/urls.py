from django.urls import path
from dejure import views

app_name = 'dejure'

urlpatterns = [
    path('', views.index, name='index'),
]
