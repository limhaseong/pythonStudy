from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.chati, name='chati'),
    path('<str:room_name>/', views.room, name='room'),
]
