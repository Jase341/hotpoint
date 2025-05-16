from django.contrib import admin
from .models import PricingPlan
from .models import Voucher

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'duration_minutes', 'used', 'created_at']
    list_filter = ['used', 'created_at']
    search_fields = ['code']
    
@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['amount', 'duration_minutes']