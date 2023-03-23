from oneset.models import Category, Location, PayMode, Role

from django.db import models

from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


# --------------------------------------Customer-------------------------------------------------
class Customer(models.Model):
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=10, unique=True)
    pincode = models.CharField(max_length=7, blank=True, null=True, validators=[
        MinLengthValidator(5), MaxLengthValidator(7)])

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_OPTIONS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_OPTIONS, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


# --------------------------------------Event-----------------------------------------------------
class Event(models.Model):
    title = models.CharField(max_length=225)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    mutuals = models.ManyToManyField(Customer, related_name='mutualEvents')

    PENDING = 'P'
    WORKING = 'W'
    NOT_RESPONDING = 'R'
    DELIVERD = 'D'
    CLOSED = 'C'
    STATUS = [
        (PENDING, 'Pending'),
        (WORKING, 'Working'),
        (NOT_RESPONDING, 'No Response'),
        (DELIVERD, 'Delivered'),
        (CLOSED, 'Closed'),
    ]
    status = models.CharField(
        max_length=1, choices=STATUS, default=PENDING)

    venue = models.CharField(max_length=225)  # PVR function hall
    address = models.CharField(max_length=225)
    city = models.ForeignKey(Location, on_delete=models.PROTECT)

    quotation = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

# -----------------------------Event Work Status--------------------------------------------------


class EventWorkStatus(models.Model):
    event = models.OneToOneField(Event, on_delete=models.PROTECT)

    DONE = 'D'
    PENDING = 'P'
    NONE = 'N'
    OPTIONS = [
        (DONE, 'Done'),
        (PENDING, 'Pending'),
        (NONE, 'None')
    ]
    saveTheDate = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    promo = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    reels = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    trailer = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    song = models.CharField(max_length=1, choices=OPTIONS, default=NONE)
    fullVideo = models.CharField(max_length=1, choices=OPTIONS, default=NONE)

    rawData = models.CharField(max_length=1, choices=OPTIONS, default=NONE)

    LIGHT_ROOM = 'L'
    ALBUM_DESIGNING = 'D'
    ALBUM_PRINTING = 'P'
    NONE = 'N'
    PHOTO_OPTIONS = [
        (LIGHT_ROOM, 'Light Room'),
        (ALBUM_DESIGNING, 'Album Designing'),
        (ALBUM_PRINTING, 'Album Printing'),
        (NONE, 'None')
    ]
    photos = models.CharField(
        max_length=1, choices=PHOTO_OPTIONS, default=NONE)

    def __str__(self) -> str:
        return self.event.title + ' - ' + ' Work Status'

    class Meta:
        verbose_name = 'Event Work Status'
        verbose_name_plural = 'Event Work Status'


# -----------------------------Event quotation Transaction----------------------------------------
class Transaction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    paymode = models.ForeignKey(PayMode, on_delete=models.PROTECT)
    value = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.event.title + ' - ' + str(self.value) + '₹' + ' - ' + self.paymode.title + ' - ' + str(self.date)


# -----------------------------Event Albums--------------------------------------------------
class Album(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    pcloudFolderId = models.CharField(max_length=250)
    isUploaded = models.BooleanField(default=False)
    createdAt = models.DateField(auto_now_add=True)
    thumb = models.URLField()

    def __str__(self) -> str:
        return self.event.title + ' - ' + self.title


# -----------------------------Event Albums ImageLinks----------------------------------------
class AlbumImage(models.Model):
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='images')
    imageId = models.CharField(max_length=300)
    link = models.URLField(unique=True)
    thumb = models.URLField(unique=True)
    is_selected = models.BooleanField(default=False)
    pcloudFileId = models.CharField(max_length=250)

    def __str__(self):
        return self.imageId
