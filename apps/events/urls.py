from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.events import views

router_user = DefaultRouter()
router_user.register(r'events', views.EventViewSet, 'event')

urlpatterns = [
    url(r'^', include(router_user.urls)),
]
