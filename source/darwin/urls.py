from django.urls import path
from darwin import views

app_name = 'darwin'

urlpatterns = [
    path('', views.index, name='index'),
]
