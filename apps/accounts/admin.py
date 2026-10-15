from django.contrib import admin
from .models import CustomerProfile, EmailOTP


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'purpose', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('purpose', 'is_verified', 'created_at')
    search_fields = ('email', 'otp_code')
    readonly_fields = ('created_at',)
