from django.conf.urls import url
from apps.authentication import views

urlpatterns = [
    url(r'^auth/email/signup/$', views.EmailSignupView.as_view(), name='email-signup'),
    url(r'^auth/email/login/$', views.EmailLoginView.as_view(), name='email-login'),

    url(r'user/$', views.UserView.as_view(), name='user'),

]
