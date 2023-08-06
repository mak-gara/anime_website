from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import Post, Tag

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_display = ('pk', 'title', 'visible_date', 'created_at', 'updated_at', 'draft')
    list_display_links = ('title',)
    filter_horizontal = ('tags',)
    list_filter = ('visible_date', 'created_at', 'updated_at')
    list_editable = ('draft',)
    save_as = True
    save_on_top = True

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at')
    list_display_links = ('title',)

