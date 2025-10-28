from django.urls import path

from .views import RoleBasedLoginView, logout_view

urlpatterns = [
    path(
        'login/',
        RoleBasedLoginView.as_view(),
        name='login',
    ),
    path('logout/', logout_view, name='logout'),
]
