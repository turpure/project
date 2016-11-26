from django.contrib import admin

from models import User, Shops, Products
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


class ShopsAdmin(admin.ModelAdmin):
    list_display = (
        'shopname', 'userid',
        'curdate', 'feedbackscore'
    )


class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'itemid',
        'uid'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(Products, ProductsAdmin)