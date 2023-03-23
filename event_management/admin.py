from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

from django.db.models import Count, When, F, Q, Case, Sum


# -------------------------------Customer Admin--------------------------------------------------------------------------------------------
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon_name = 'person_pin'
    list_display = ['name', 'phone', 'gender',
                    'pincode', 'events', 'mutual_Events']
    list_per_page = 10
    list_filter = ['gender']
    ordering = ['name']
    search_fields = ['name__icontains', 'phone__icontains', 'pincode']
    actions_selection_counter = False

    fieldsets = [
        (None, {
            'fields': [('name', 'phone')]
        }),
        ('Other Options', {
            'fields': [('gender', 'pincode')],
            'description': 'these fields are optional, But Better to fill!'
        })]

    @admin.display(ordering='events')
    def events(self, customer: models.Customer):
        url = reverse('admin:event_management_event_changelist') + '?' + \
            urlencode({'customer__id': customer.id})
        return format_html(f'<a href="{url}">{customer.events}</a>')

    @admin.display(ordering='events')
    def mutual_Events(self, customer: models.Customer):
        url = reverse('admin:event_management_event_changelist') + '?' + \
            urlencode({'mutuals__id': customer.id})
        return format_html(f'<a href="{url}">{customer.mutual_Events}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(events=Count('event', distinct=True)).annotate(mutual_Events=Count('mutualEvents', distinct=True))


# -------------------------------Event Admin----------------------------------------------------------------------------------------------
class WorkStatusInline(admin.TabularInline):
    model = models.EventWorkStatus
    min_num = 1
    max_num = 1
    extra = 0

    def has_delete_permission(self, request, obj):
        return False


class TransactionInline(admin.StackedInline):
    model = models.Transaction
    min_num = 0
    max_num = 1000
    extra = 1


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    icon_name = 'pages'
    list_display = ['title', 'Customer', 'date',
                    'category', 'city', 'status', 'Albums', 'payment', 'work_status']
    list_per_page = 10
    autocomplete_fields = ['customer', 'mutuals']
    ordering = ['-date']
    search_fields = ['title__icontains',
                     'customer__name__icontains', 'customer__phone__icontains']
    list_filter = ['category', 'city', 'status']
    date_hierarchy = 'date'
    list_select_related = ['customer']
    inlines = [WorkStatusInline, TransactionInline]

    fieldsets = [
        (None, {
            'fields': ['status', ('title', 'date', 'quotation'), ('customer', 'category', 'city')]
        }),
        ('Venue Details', {
            'fields': [('venue', 'address')],
            'description': 'this data is used in the APK, make sure to give properly!'
        }),
        ('Mutual Connections', {
            'fields': [('mutuals')],
        })]

    @admin.display(ordering='albums')
    def Albums(self, event):
        if event.albums == 0:
            return '0'
        url = reverse('admin:event_management_album_changelist') + \
            '?' + urlencode({'event__id': event.id})
        return format_html(f'<a href="{url}">{str(event.albums)}</a>')

    @admin.display(ordering='payment')
    def payment(self, event):
        if event.payment == None:
            return '0%'
        url = reverse('admin:event_management_transaction_changelist') + \
            '?' + urlencode({'event__id': event.id})
        return format_html(f'<a href="{url}">{str(event.payment)}%</a>')

    def work_status(self, event):
        url = reverse('admin:event_management_eventworkstatus_changelist') + \
            '?' + urlencode({'event__id': event.id})
        return format_html(f'<a style="color:#000000;" href="{url}"><i class="material-icons large-icon">lassignment_turned_in keyboard_arrow_right</i></a>')

    @admin.display(ordering='customer__name')
    def Customer(self, event: models.Event):
        return event.customer.name + ' - ' + event.customer.phone

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(payment=(Sum('transaction__value', distinct=True)/F('quotation'))*100).annotate(albums=Count('album', distinct=True))


# ---------------------Event WorkStatus------------------------------------------------------------------------------------------------
@ admin.register(models.EventWorkStatus)
class EventWorkStatusAdmin(admin.ModelAdmin):
    icon_name = 'assignment_turned_in'
    list_display = ['Event', 'S_T_D', 'Promo',
                    'Reels', 'Trailer', 'Song', 'Full_Video', 'photos', 'Raw']
    list_per_page = 10
    list_filter = ['photos']
    list_select_related = ['event']

    fieldsets = [
        (None, {
            'fields': ['event']
        }),
        ('Video Works', {
            'fields': [('saveTheDate', 'promo', 'reels', 'trailer'), ('song', 'fullVideo')],
            'description': 'NOTE: Please Keep None if the service is not providing to this event. '
        }),
        ('Photo Works', {
            'fields': [('photos')],
            'description': 'NOTE: Please Keep None if Photos work is not yet Started. '
        }),
        ('Data', {
            'fields': [('rawData')],
            'description': 'NOTE: Please Keep UnKnown if Data is Not Created. '
        })]

    # *****************************************************
    # @admin.display(ordering='event')
    def Event(self, EventWorkStatus: models.EventWorkStatus):
        return EventWorkStatus.event.title + ' - ' + str(EventWorkStatus.event.customer.phone)

    def S_T_D(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.saveTheDate == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.saveTheDate == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Promo(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.promo == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.promo == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Reels(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.reels == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.reels == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Trailer(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.trailer == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.trailer == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Song(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.song == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.song == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Full_Video(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.fullVideo == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.fullVideo == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')

    def Raw(self, EventWorkStatus: models.EventWorkStatus):
        if EventWorkStatus.rawData == 'D':
            return format_html('<i class="material-icons green-color medium-icon">check_circle</i>')
        elif EventWorkStatus.rawData == 'P':
            return format_html('<i class="material-icons red-color medium-icon">remove_circle</i>')
        else:
            return format_html('<i class="material-icons green-color medium-icon">radio_button_unchecked</i>')
    # -------------------------------------------------------------

    def get_queryset(self, request):
        query = super().get_queryset(request).select_related(
            'event').exclude(event__status='C')
        return query.annotate(payment=(Sum('event__transaction__value', distinct=True)/F('event__quotation'))*100).order_by('-payment', 'event__date')


# ---------------------Quotation Transaction---------------------------------------------------------------------------------------------
@ admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    icon_name = 'attach_money'
    list_display = ['event', 'date', 'paymode', 'value']
    list_per_page = 10
    ordering = ['-date']
    search_fields = ['event__icontains', 'customer__icontains']
    date_hierarchy = 'date'
    list_filter = ['paymode']
    autocomplete_fields = ['event', 'paymode']

    fieldsets = [
        (None, {
            'fields': [('event', 'paymode', 'value')]
        })]


# ---------------------Event Albums----------------------------------------------------------------------------------------------------
class imagesInline(admin.TabularInline):
    model = models.AlbumImage
    fields = ['imageId', 'link', 'is_selected']

    def has_add_permission(self, request, obj) -> bool:
        return False

    def has_delete_permission(self, request, obj) -> bool:
        return False


@ admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    icon_name = 'burst_mode'
    list_display = ['event', 'title', 'is_uploaded', 'images', 'selected']
    list_per_page = 10
    search_fields = ['event', 'title']
    inlines = [imagesInline]
    ordering = ['-createdAt']

    def is_uploaded(self, album: models.Album):
        if album.isUploaded == False:
            return format_html('<i class="material-icons black-color medium-icon">cloud_upload</i>')
        return format_html('<i class="material-icons black-color medium-icon">cloud_done</i>')

    @ admin.display(ordering='image_count')
    def images(self, album: models.Album):
        if album.image_count == 0:
            return '0'
        url = reverse('admin:event_management_albumimage_changelist') + \
            '?' + urlencode({'album__id': album.id})
        return format_html(f'<a href="{url}">{str(album.image_count)}</a>')

    @ admin.display(ordering='selected', boolean=False)
    def selected(self, album: models.Album):
        if album.selected == None:
            return '0'
        elif album.selected == True:
            album.selected = 1
        url = reverse('admin:event_management_albumimage_changelist') + \
            '?' + urlencode({'album__id': album.id, 'is_selected': True})
        return format_html(f'<a href="{url}">{str(album.selected)}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(image_count=Count('images')).annotate(selected=Sum('images__is_selected'))


# ---------------------Event Albums-----------------------------------------------------------------------------------------------------
@ admin.register(models.AlbumImage)
class AlbumImageAdmin(admin.ModelAdmin):
    icon_name = 'art_track'
    list_display = ['album', 'imageId', 'Is_Selected']

    def Is_Selected(self, image: models.AlbumImage):
        if image.is_selected == 1:
            return format_html('<i style="color:#D10000;" class="material-icons red-color medium-icon">favorite</i>')
        return format_html('<i class="material-icons black-color medium-icon">favorite_border</i>')
