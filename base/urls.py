from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('charge/', views.charge, name="charge"),
    path('payment/', views.addPayment),
    path('success/<str:args>/', views.successMsg, name="success"),
]
