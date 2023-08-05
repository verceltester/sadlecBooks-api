from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Books)
# admin.site.register(Chapter)
# admin.site.register(Subhead1)
# admin.site.register(Subhead2)

@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','bookTitle','bookAuthor', 'bookPrice', "aurokart"]
    ordering = ['id']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id','chapTitle', 'Books', 'hastext']
    ordering = ['id']


@admin.register(Subhead1)
class Subhead1Admin(admin.ModelAdmin):
    list_display = ['id','subhead1Titles', 'Chapter', 'hastext']
    ordering = ['id']


@admin.register(Subhead2)
class Subhead2Admin(admin.ModelAdmin):
    list_display = ['id','subhead2Titles', 'Subhead1', 'hastext']
    ordering = ['id']