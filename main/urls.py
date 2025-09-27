from django.urls import path
from . import views
from api.users.views import login_view, register_view, logout_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
