from django.contrib import admin
#remove group
from django.contrib.auth.models import Group

# Register your models here.
from . import models
#Remove group from admin
admin.site.unregister(Group)

#import export
from import_export.admin import ImportExportActionModelAdmin
# admin custom
admin.site.site_title = "Artel Blog API"
admin.AdminSite.site_header = "Artel Blog API"
admin.site.index_title = "Artel Bloga hush kelibsiz"

# for blogs language
@admin.register(models.PostLanguage)
class BlogLangAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title','language', 'active' ]
    list_filter = ['active',]
    list_display_links = ('id', 'title')

# For blog
@admin.register(models.Blog)
class BlogAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'author', 'title','published_at' ]
    list_filter = ['active',]
    list_display_links = ('id', 'author', 'title')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    search_fields = ['title', 'content']
# for blog category
admin.site.register(models.Category)
