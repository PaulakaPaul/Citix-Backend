from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.events import views

router_events = DefaultRouter()
router_events.register(r'events', views.EventViewSet, 'event')

urlpatterns = [
    url(r'^events/reaction/$', views.EventUserReactionViewSet.as_view({'post': 'create'}), name='event-reaction'),
    url(r'^events/photo/$', views.EventAddPhotoView.as_view(), name='event-add-photo'),

    url(r'^', include(router_events.urls)),  # This include has to be after the normal /events/* to not be overridden.
]
