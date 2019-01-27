from django.urls import path
from mereokratos import views

app_name = 'mereokratos'

urlpatterns = [
    path('', views.index, name='index'),
]
