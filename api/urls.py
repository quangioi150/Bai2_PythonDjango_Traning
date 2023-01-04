from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import NewsViewSet, UserLoginAPI

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls), name='api_index'),
    path("login/", UserLoginAPI.as_view(), name="user_login_api"),
]
