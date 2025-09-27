from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('timeline/<int:user_id>/', views.user_timeline, name='user_timeline'),
]
