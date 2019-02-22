from django.conf.urls import url

from apps.authentication import views

urlpatterns = [
    url(r'^auth/email/signup/$', views.EmailSignupView.as_view(), name='email-signup')
]
