from django.contrib import admin
from django.db.models import Count, Q, Value, Sum
from utility.pcloud import getPubSmallThumb, deleteFile
from . models import Stream, PortfolioImage, Plan, PlanAddon, PlanQuerie
from django.utils.html import format_html

from core.views import getAuth


# -------------------------------Stream Admin--------------------------------------------------------------------------------------------
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    icon_name = "ondemand_video"
    list_display = ['event', 'title',  'time', 'streamLink', 'Thumbnail']
    search_fields = ['event', 'title']
    list_per_page = 10
    autocomplete_fields = ['event']

    def Thumbnail(self, stream):
        component = f"""
            <a href="{stream.link}" target="_blank">
                <div style="width: 10rem;
                    height: 5.5rem;
                    background-image: url({getPubSmallThumb(stream.pubCode, 300)});
                    background-size: cover;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 0px 10px 0 #0000006e;
                    border-radius: 0.5rem;">
                </div>
	        </a>
        """
        return format_html(component)

    fieldsets = (
        (None, {
            "fields": ('event', ('title',  'time'), 'streamLink', 'thumbnail'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for object in queryset:
            response = deleteFile(
                getAuth(), object.pcloudFileId)
            if response == 200:
                continue
            else:
                break
        else:
            return super().delete_queryset(request, queryset)


# -------------------------------Portfolio Admin--------------------------------------------------------------------------------------------
@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    icon_name = "photo_library"
    list_display = ['category', 'Image']
    list_filter = ['category']
    autocomplete_fields = ['category']
    list_per_page = 10
    list_display_links = None
    actions_selection_counter = False

    def Image(self, image):
        component = f"""
            <a href="{image.link}" target="_blank">
                <div style="width: 10rem;
                    height: 5.5rem;
                    background-image: url({getPubSmallThumb(image.pubCode, 300)});
                    background-size: cover;
                    display: inline-block;
                    transition: all 0.3s ease;
                    box-shadow: 0 0px 10px 0 #0000006e;
                    border-radius: 0.5rem;">
                </div>
	        </a>
        """
        return format_html(component)

    fieldsets = (
        (None, {
            "fields": ('category', 'image'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for object in queryset:
            response = deleteFile(
                getAuth(), object.pcloudFileId)
            if response == 200:
                continue
            else:
                break
        else:
            return super().delete_queryset(request, queryset)


# -------------------------------Plans--------------------------------------------------------------------------------------------
class AddonInline(admin.TabularInline):
    model = PlanAddon
    min_num = 1
    max_num = 100
    extra = 0


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    icon_name = 'view_carousel'
    list_display = ['title', 'price', 'queries',]
    ordering = ['-price']

    inlines = [AddonInline]

    @admin.display(ordering='query_count')
    def queries(self, plan):
        return plan.query_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(query_count=Count('planquerie', distinct=True))


# -------------------------------Plans--------------------------------------------------------------------------------------------
@admin.register(PlanQuerie)
class PlanQuerieAdmin(admin.ModelAdmin):
    icon_name = 'message'
    list_display = ['createdAt', 'plan', 'Customer', 'read']
    list_filter = ['plan']
    actions = ['mark_as_read']
    list_display_links = None
    search_fields = ['Customer']
    date_hierarchy = 'createdAt'

    def Customer(self, query):
        return query.customer.name + ' - ' + query.customer.phone
    # ---------------------------------------

    def has_add_permission(self, request) -> bool:
        return False
    # ---------------------------------------

    @admin.action(description='Mark As Read')
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
    # ---------------------------------------

    def get_queryset(self, request):
        return super().get_queryset(request)
