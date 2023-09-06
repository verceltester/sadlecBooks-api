from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# admin.site.register(Books)
# admin.site.register(Chapter)
# admin.site.register(Subhead1)
# admin.site.register(Subhead2)

class bookixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...
class chapixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...
class sub1ixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...
class sub2ixAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


@admin.register(Books)
class BookAdmin(bookixAdmin, admin.ModelAdmin):
    list_display = ['id','bookTitle','bookAuthor', 'bookPrice', "aurokart"]
    ordering = ['id']


@admin.register(Chapter)
class ChapterAdmin(chapixAdmin, admin.ModelAdmin):
    list_display = ['id','chapTitle', 'Books', 'hastext']
    ordering = ['id']


@admin.register(Subhead1)
class Subhead1Admin(sub1ixAdmin, admin.ModelAdmin):
    list_display = ['id','subhead1Titles', 'Chapter', 'hastext']
    ordering = ['id']


@admin.register(Subhead2)
class Subhead2Admin(sub2ixAdmin, admin.ModelAdmin):
    list_display = ['id','subhead2Titles', 'Subhead1', 'hastext']
    ordering = ['id']