from django.urls import path

from . import views

urlpatterns = [
    path('', views.record, name='persnalcolor_record'),
]