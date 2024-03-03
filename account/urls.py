from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='account/signup.html'), name='회원가입'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.sign, name='sign'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('id_search/', views.RecoveryIdView.as_view(), name='id_search'),
    path('id_search/find/', views.ajax_find_id_view, name='ajax_id'),
    path('pw_search/', views.RecoveryPwView.as_view(), name='pw_search'),
    path('recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset_view, name='pw_reset'),
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
]