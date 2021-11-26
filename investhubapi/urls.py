"""investhubapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.views import auth
from core.views.user import profile


@api_view(['GET'])
def index(_):
    return Response("InvestHub System powered by Python and Django")


urlpatterns = [
    path('', index),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='auth-token'),
    path('api/auth/login/facebook/', auth.login_facebook),

    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='auth-token-verify'),

    # path('api/auth/change-password/', auth.change_password),

    path('api/user/profile/', profile.profile),
    path('api/user/profile/author-registration/', profile.profile),
]
