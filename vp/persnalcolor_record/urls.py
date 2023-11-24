from django.urls import path

from . import views

urlpatterns = [
    path('', views.record, name='persnalcolor_record'),
    path('save_recording/', views.save_recording, name='save_recording'),
]