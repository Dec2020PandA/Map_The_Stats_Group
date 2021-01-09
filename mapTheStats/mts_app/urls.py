from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('decipher_location_type', views.decipher_location_type),
    path('state_api_call', views.state_api_call),
    path('country_api_call', views.country_api_call),
    path('msa_api_call', views.msa_api_call),
]