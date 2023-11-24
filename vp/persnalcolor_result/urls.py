from django.urls import path
from . import views

urlpatterns = [
    path('', views.persnalcolor_result, name='persnalcolor_result'),
    path('result/', views.result, name='result'), 
]
