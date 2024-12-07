from django.urls import path
from register import views

urlpatterns = [
    path('register/', views.register, name='register'),
]
