from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('orders/<int:pk>/', views.UserOrderDetailView.as_view(), name='order_detail'),
]

