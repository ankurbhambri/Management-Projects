from django.urls import path
from django.views.generic import TemplateView, ListView
from app1 import views

urlpatterns = [
    path('', views.contact, name='contact'),
]