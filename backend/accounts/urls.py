from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('refresh/', views.refresh_token, name='refresh_token'),
    path('logout/', views.logout, name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-verification-email/', views.resend_verification_email, name='resend_verification_email'),
    path('password-reset-request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('me/', views.get_user_profile, name='get_user_profile'),
    path('profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
