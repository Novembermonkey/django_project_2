from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login-page/', views.login_page, name='login_page'),
    path('register-page/', views.register_page, name='register_page'),
]