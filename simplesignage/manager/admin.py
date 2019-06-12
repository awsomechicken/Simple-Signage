from django.contrib import admin

# Register your models here.
from .models import Show, File, Page

#admin.site.register(Show)
#admin.site.register(Page)
#admin.site.register(File)

class Files(admin.StackedInline):
    model = File
    extra = 1


class ShowAdmin(admin.ModelAdmin):
    inlines = [Files]

admin.site.register(Show, ShowAdmin)
