from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer/<str:idnum>/', views.customer, name='customer'),
    path('products/', views.products, name='products'),

    path('order_form/<str:idnum>/', views.createOrder, name='order_form'),
    path('update_form/<str:idnum>/', views.updateOrder, name='update_form'),
    path('delete_form/<str:idnum>/', views.deleteOrder, name='delete_form'),

    path('register/', views.registrationPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('user/', views.userPage, name='user_page'),
    path('user/user_settings/', views.userSettings, name='user_settings'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='account/reset_password.html'),
         name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/reset_password_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/reset_password_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/reset_password_done.html'),
         name='password_reset_conplete'),
]
