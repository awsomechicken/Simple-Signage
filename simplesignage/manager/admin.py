from django.contrib import admin

# Register your models here.
from .models import Show, Content, Screen

#admin.site.register(Show)
#admin.site.register(Page)
admin.site.register(Content)
admin.site.register(Screen)

class Content(admin.StackedInline):
    model = Content
    #extra = 1

class ShowAdmin(admin.ModelAdmin):
    #inlines = [Content]
    model = Show

admin.site.register(Show, ShowAdmin)
