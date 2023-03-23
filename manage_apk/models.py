from django.db import models

from event_management.models import Event, Category, Customer

from utility.pcloud import uploadFile, deleteFile

from core.views import getAuth


# -------------------------------Streams--------------------------------------------------------------------------------------------
class Stream(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    streamLink = models.URLField(unique=True)
    link = models.URLField(unique=True)
    time = models.TimeField()
    thumbnail = models.ImageField(
        upload_to='thumbnail/', blank=True, null=True)
    pcloudFileId = models.CharField(max_length=300, blank=True)
    pubCode = models.CharField(max_length=1000)

    def save(self, *args, **kwargs) -> None:
        if self.thumbnail:
            data = self.thumbnail
            auth = getAuth()
            if auth:
                response = uploadFile(auth=auth,
                                      data=data, folderPath='/streams')
            if response != 400:
                self.pcloudFileId = response['fileid']
                self.link = response['publiclink']
                self.pubCode = response['code']
        self.thumbnail = None
        return super(Stream, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        auth = getAuth()
        if auth:
            response = deleteFile(auth=auth, fileid=self.pcloudFileId)
            if response == 200:
                super(Stream, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title


# -------------------------------Portfolio--------------------------------------------------------------------------------------------
class PortfolioImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/',
                              null=True, blank=True)
    link = models.URLField(unique=True, blank=True)
    pcloudFileId = models.CharField(max_length=300, blank=True)
    pubCode = models.CharField(max_length=1000)

    def __str__(self):
        return 'To - ' + self.category.title

    def save(self, *args, **kwargs) -> None:
        if self.image:
            data = self.image
            auth = getAuth()
            if auth:
                response = uploadFile(auth=auth,
                                      data=data, folderPath='/portfolio')
                if response != 400:
                    print('step - 5')
                    self.pcloudFileId = response['fileid']
                    self.link = response['publiclink']
                    self.pubCode = response['code']
                    self.image = None
                    return super(PortfolioImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        auth = getAuth()
        if auth:
            response = deleteFile(auth, self.pcloudFileId)
            if response == 200:
                super(PortfolioImage, self).delete(*args, **kwargs)
            else:
                raise ValueError('Image Cannot be Deleted')
        else:
            raise ValueError('Cannot get Auth Token')


# --------------------------------Plans---------------------------------------------------------------
class Plan(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title


# --------------------------------Plan Adons---------------------------------------------------------------
class PlanAddon(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


# --------------------------------Customer Queries---------------------------------------------------------------
class PlanQuerie(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    createdAt = models.DateField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.customer.name + ' - ' + str(self.plan)

    class Meta:
        verbose_name = 'enquire'
        verbose_name_plural = 'enquiries'
