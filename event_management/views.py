from . models import Album, AlbumImage, Event
from . serializer import AlbumSerializer, AlbumImageSerializer, EventSerializer
from .filters import EventFilter
from core.views import getAuth
from django.db.models import Count, Q, Value, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from uuid import uuid1, uuid3, uuid4, uuid5


class eventViewSet(ModelViewSet):
    queryset = Event.objects.select_related('customer').exclude(status='C')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['date', 'quotation']
    search_fields = ['title', 'category__title']
    filterset_class = EventFilter
    pagination_class = PageNumberPagination

    def destroy(self, request, *args, **kwargs):
        if (Album.objects.filter(event=kwargs['pk']).count() > 0):
            return Response({"error": "this event contains albums, delete them before"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class albumViewSet(ModelViewSet):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = Album.objects.filter(event=self.kwargs['event_pk']).annotate(imgCount=Count('images')).annotate(
            selectedCount=Sum('images__is_selected'))
        return queryset

    def create(self, request, *args, **kwargs):
        response = getAuth()
        if response:
            serializer = AlbumSerializer(
                data=request.data, context={'auth': response, 'event_id': self.kwargs['event_id']})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {**serializer.data, 'auth': response}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({"error": "Cannot get Cloud Auth Credientials"}, status=status.HTTP_401_UNAUTHORIZED)


class albumImage_list(APIView):
    def get(self, request, event_pk, album_pk, *args):
        queryset = AlbumImage.objects.filter(album=album_pk)
        serializer = AlbumImageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, event_pk, album_pk, *args):
        serializer = AlbumImageSerializer(
            data=request.data, many=True, context={'albumId': album_pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ____________________ APIS FOR MOBILE APPLICATIONS _______________________________
