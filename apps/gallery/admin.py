from django.contrib import admin

from apps.gallery.models import Picture


class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture')


admin.site.register(Picture, PictureAdmin)
