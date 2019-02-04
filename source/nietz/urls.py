from django.urls import path
from nietz import views

app_name = 'nietz'

urlpatterns = [
    path('', views.index, name='index'),
    path('c/', views.concepts, name='concepts'),
    path('f/', views.fallacies, name='fallacies'),
    path('f/<int:identifier>/', views.fallacy, name='fallacy'),
]
