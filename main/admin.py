from django.contrib import admin

from .models import Anime, Category, ImageSlider, Review, Like, Ip, CustomUser, Communication


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'updated_at', 'draft')
    list_display_links = ('title', )
    filter_horizontal = ('studios', 'licensors', 'producers', 'genres', 'themes')
    list_editable = ('draft', )
    search_fields = ('title', 'english_title', 'japanese_title')
    list_filter = ('draft', 'created_at')
    autocomplete_fields = ('type', 'source')
    save_on_top = True
    save_as = True


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'created_at', 'updated_at')
    search_fields = ('text',)
    list_filter = ('created_at',)
    readonly_fields = ('user', 'text', 'anime', 'parent')


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ip', 'request_date')
    search_fields = ('=ip',)
    list_filter = ('request_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at')
    search_fields = ('title', )
    list_filter = ('created_at', )

@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'sent_at')
    list_display_links = ('name',)
    search_fields = ('name', 'email')
    list_filter = ('sent_at',)

@admin.register(ImageSlider)
class ImageSliderAdmin(admin.ModelAdmin):
    autocomplete_fields = ('anime',)

admin.site.register(Like)
admin.site.register(CustomUser)