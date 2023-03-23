from datetime import datetime

from rest_framework import serializers

from utility.pcloud import createFolder

from . models import Album, AlbumImage, Event, Customer

from core.views import getAuth


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'event', 'title',
                  'pcloudFolderId', 'isUploaded', 'createdAt', 'imgCount', 'selectedCount', 'thumb']

    id = serializers.IntegerField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    imgCount = serializers.IntegerField(read_only=True)
    selectedCount = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateField(read_only=True)
    pcloudFolderId = serializers.CharField(max_length=200, read_only=True)

    def create(self, validated_data):
        response = createFolder(auth=self.context['auth'], path='albums/',
                                name=f'{validated_data["title"]} - {str(datetime.now().timestamp())}')
        if response != 400:
            validated_data['pcloudFolderId'] = response
            validated_data['event'] = Event.objects.get(
                id=self.context['event_id'])
            return super().create(validated_data)
        else:
            return serializers.ValidationError(
                'pcloud Folder Not Yet Created', code=404)


class AlbumImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    album = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AlbumImage
        fields = ['id', 'album', 'imageId',
                  'link', 'thumb', 'is_selected', 'pcloudFileId']

    def create(self, validated_data):
        validated_data['album'] = Album.objects.get(id=self.context['albumId'])
        return super().create(validated_data)


class CustomerListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone']


class EventSerializer(serializers.ModelSerializer):
    customer = CustomerListingSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
