
from django.contrib import admin
from django.urls import path, include
from parking import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parking.urls')),
    path('login/', views.user_login, name='login'),
]

