from django.contrib import admin
from shopApp.models import Product
from . import models
from django.contrib import admin


# admin_site = admin.AdminSite(name='myadmin')
# admin_site.site_header = 'مدیریت'

# admin.site.site_title = 'مدیریت سایت فروشگاه امیر'


admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Tedad)
# @admin.register(models.Color)
# class ColorAdmin(admin.ModelAdmin):
#     list_display = ('name',)

