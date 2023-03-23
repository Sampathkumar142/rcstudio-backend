from django.contrib import admin
from django.db.models import Count

from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    icon_name = "dashboard"
    list_display = ['title', 'events']
    search_fields = ['title']

    @admin.display(ordering='eventCount')
    def events(self, category):
        url = reverse('admin:event_management_event_changelist') + \
            '?' + urlencode({'category__id': category.id})
        return format_html(f'<a href={url}>{category.eventCount}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(eventCount=Count('event'))


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    icon_name = "pin_drop"
    list_display = ['title', 'events']
    search_fields = ['title']

    @admin.display(ordering='eventCount')
    def events(self, city):
        url = reverse('admin:event_management_event_changelist') + \
            '?' + urlencode({'city__id': city.id})
        return format_html(f'<a href={url}>{city.eventCount}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(eventCount=Count('event'))


@admin.register(models.PayMode)
class PayModeAdmin(admin.ModelAdmin):
    icon_name = "payment"
    list_display = ['title', 'transaction']
    search_fields = ['title']

    @admin.display(ordering='transactionCount')
    def transaction(self, paymode):
        url = reverse('admin:event_management_transaction_changelist') + \
            '?' + urlencode({'paymode__id': paymode.id})
        return format_html(f'<a href={url}>{paymode.transactionCount}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(transactionCount=Count('transaction'))


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    icon_name = "assignment_ind"
    list_display = ['title']
    search_fields = ['title']
