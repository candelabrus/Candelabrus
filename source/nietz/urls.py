from django.urls import path
from nietz import views

app_name = 'nietz'

urlpatterns = [
    path('', views.index, name='index'),
    path('f/', views.fallacies, name='fallacies'),
]
