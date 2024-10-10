from django.contrib import admin
from .models import Product, Report, UserReport


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'price', 'image', 'mobile_number', 'location', 'user')
    search_fields = ('title', 'description', 'category', 'price', 'mobile_number', 'location', 'user__username')
    actions = ['delete_selected']

    def product_title(self, obj):
        return obj.product.title

    def user_username(self, obj):
        return obj.user.username

class UserReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'reported_by', 'reason', 'created_at')
    list_filter = ('user', 'reported_by', 'created_at')
    search_fields = ('user', 'reported_by', 'reason')
    ordering = ('-created_at',)

admin.site.register(UserReport, UserReportAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Report)
