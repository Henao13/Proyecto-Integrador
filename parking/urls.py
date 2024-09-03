from django.urls import path
<<<<<<< HEAD
from parking.views import home, add_balance

urls_patterns = [
    path('', home, name='home'),
    path('add_balance/', add_balance, name='add_balance'),
=======
from .views import home

urlpatterns = [
    path('', home, name='home'),
>>>>>>> progress
]