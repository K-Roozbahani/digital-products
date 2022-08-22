from django.contrib import admin
from .models import Payment, Gateway


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable']



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'price', 'status', 'created_time', 'phone_number', 'consumed_code']
    list_filter = ['status', 'gateway', 'package']
    search_fields = ['user', 'phone-number', ]