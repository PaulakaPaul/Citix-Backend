from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from apps.authentication import views


routerUser = DefaultRouter();
routerUser.register(r'users', views.UserViewSet, 'user');

urlpatterns = [
]