from django.urls import path
from parking.views import home, add_balance

urls_patterns = [
    path('', home, name='home'),
    path('add_balance/', add_balance, name='add_balance'),
]