from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('state_api_call', views.state_api_call),
    path('country_api_call', views.country_api_call),
    path('msa_api_call', views.msa_api_call),
]