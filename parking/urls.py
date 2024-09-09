from django.urls import path
from . import views
from .views import simular_transaccion_view

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('simular-transaccion/<str:id_usuario>/', simular_transaccion_view, name='simular-transaccion'),
]