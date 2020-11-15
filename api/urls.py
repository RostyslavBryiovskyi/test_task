from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.users, name="users"),
    path('users_filter/', views.users_filter, name="users_filter"),
    path('users/<int:pk>/', views.users, name="users"),
    path('signup/', views.signup, name="signup")
]
