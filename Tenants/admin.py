from django.contrib import admin
from .models import *


@admin.register(Caretaker)
class CaretakerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'sur_name', 'last_name', 'id_number']


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['apartment_name', 'units', 'caretaker']


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['apartment', 'house_code', 'house_type', 'vacant']


@admin.register(Lease)
class Leaseadmin(admin.ModelAdmin):
    list_display = ['apartment', 'house', 'id', 'current_status', 'running_balance']


admin.site.register(HouseType)
admin.site.register(Tenant)
admin.site.register(Invoice)
admin.site.register(PaidRent)

