from django.urls import path
from .views import UserCreateView, MyTokenObtainPairView, UserUpdateView
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update/', views.updateUser, name='user-update'),
    path('get/', views.getUser, name='get-user'),
    path('send_otp/', views.send_otp, name='get-user'),
    path('verify_otp/', views.verify_otp, name='get-user'),
]
