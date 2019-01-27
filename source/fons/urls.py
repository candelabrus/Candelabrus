from django.urls import path
from fons import views


app_name = 'fons'

urlpatterns = [
    path('', views.index, name='index'),
]
