from django.contrib import admin
from .models import Topic, Entry
# Register your models here.
#
admin.site.register(Topic)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("text", "date_added")
    search_fields = ("topic", "text")
