from django.urls import path
from fons import views

app_name = 'nietz'

urlpatterns = [
    path('', views.index, name='index'),
]
