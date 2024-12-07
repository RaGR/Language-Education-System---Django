from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout',views.logout_user, name='logout'),
]
