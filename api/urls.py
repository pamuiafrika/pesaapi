from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', views.user_login, name='login'),
    path('signup/', views.register, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordConfirm.as_view(), name='reset_password_confirm'),

    
    path('quote/', views.quote_currency, name='quote_currency'),
    path('convert/', views.convert_currency, name='convert_currency'),
]
