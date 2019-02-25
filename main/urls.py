from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.views.generic import RedirectView
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='docs')),
    url(r'^api/docs/$', get_swagger_view(title='Citix Server API'), name='docs'),
    url(r'^api/', include(('apps.authentication.urls', 'authentication'), namespace='authentication')),
    url(r'^api/', include(('apps.events.urls', 'events'), namespace='events')),
    url(r'^admin/', admin.site.urls),
]
