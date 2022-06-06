from django.contrib import admin

# Register your models here.
from . import models
#remove group
from django.contrib.auth.models import Group
admin.site.unregister(Group)


#import export
from import_export.admin import ImportExportActionModelAdmin


# Register your models here.
admin.site.site_title = "Artel Blog API"
admin.AdminSite.site_header = "Artel Blog API"
admin.site.index_title = "Artel Bloga hush kelibsiz"

# for blog language
@admin.register(models.PostLanguage)
class BlogLangAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title','language','active' ]
    list_filter = ['active',]
    list_display_links = ('id', 'title')

# For blog
@admin.register(models.Blog)
class BlogAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'author', 'title','language','published_at' ]
    list_filter = ['active',]
    list_display_links = ('id', 'author', 'title')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'created_at']
    list_display_links = ('id', 'name', 'code')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
admin.site.register(models.Category)
