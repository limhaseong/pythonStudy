from django.urls import path
from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index, name='index'),
    path('write.html', views.m_new, name='m_new'),
    path('list.html', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('edit/<int:pk>', views.edit, name='edit' ),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
]