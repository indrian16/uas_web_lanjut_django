from django.contrib import admin
from . models import Biodata, API

class BiodataAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')

class APIAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_key')

admin.site.register(Biodata, BiodataAdmin)

admin.site.register(API, APIAdmin)