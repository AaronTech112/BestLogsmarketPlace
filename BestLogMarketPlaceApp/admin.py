# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Product, Transaction,BankPaymentDetail,Cart,CartItem


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order',)  # Display the order field
    list_editable = ('order',)         # Make the order field editable directly from the list view
    ordering = ('order',)              # Sort the categories by the 'order' field in the admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','category', 'view_link')
    list_filter = ('category',)
    search_fields = ('name',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_status', 'transaction_date')
    list_filter = ('transaction_status',)
    search_fields = ('user__username',)
    actions = ['approve_transactions', 'decline_transactions']

    def approve_transactions(self, request, queryset):
        queryset.update(transaction_status='approved')
        for transaction in queryset:
            for product in transaction.products.all():
                product.delete()  # Mark the product as inactive

    approve_transactions.short_description = 'Approve selected transactions'

    def decline_transactions(self, request, queryset):
        queryset.update(transaction_status='declined')

    decline_transactions.short_description = 'Decline selected transactions'

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BankPaymentDetail)
admin.site.register(Cart)
admin.site.register(CartItem)
