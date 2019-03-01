from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.authentication import views

router_user = DefaultRouter()
router_user.register(r'users', views.UserViewSet, 'user')

urlpatterns = [
    url(r'^auth/email/signup/$', views.EmailSignupView.as_view(), name='email-signup'),
    url(r'^auth/email/login/$', views.EmailLoginView.as_view(), name='email-login'),

    url(r'^', include(router_user.urls)),
]
