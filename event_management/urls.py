from django.urls import path, include
from . import views

from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('events', views.eventViewSet)

events_router = routers.NestedSimpleRouter(router, 'events', lookup='event')
events_router.register('albums', views.albumViewSet, basename='event-album')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(events_router.urls)),
]

#    path('events/<int:event_pk>/albums/<int:album_pk>/images',
#    views.albumImage_list.as_view()),
