from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.events import views

router_events = DefaultRouter()
router_events.register(r'events', views.EventViewSet, 'event')

urlpatterns = [
    url(r'^', include(router_events.urls)),
    url(r'^events/reactions/$', views.EventUserReactionViewSet.as_view({'post': 'create'})),
]
