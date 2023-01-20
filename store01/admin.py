from django.contrib import admin
from daterange.filters import DateRangeFilter
from store01.models import category01,product01,Cart,CartItem,Order,OrderItem,BankTransfer
from django.db.models import Count, Sum, Min, Max, DateTimeField
from django.db.models.functions import Trunc
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django import forms
from django.shortcuts import render
from django.urls import path
# from admincharts.admin import AdminChartMixin
# from admincharts.utils import months_between_dates
from functools import total_ordering
from django.db import models
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','updated','available','admin_image']
    list_editable=['price','stock','available']
    list_per_page=10
    search_fields = ['name']

class ItemInline(admin.TabularInline):
    model = OrderItem
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class BankTransferInline(admin.TabularInline):
    model = BankTransfer
    exclude = ['name', 'address', 'city', 'postcode',]
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra
        
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order','product','quantity','price','created',]
    list_per_page=10
    list_filter = [("updated", DateRangeFilter)]
    change_list_template = ["admin/daterange/change_list.html"]
    def has_module_permission(self, request):
        return False
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','name','email','total','created',]
    list_per_page=10
    list_filter = [("updated", DateRangeFilter)]
    change_list_template = ["admin/daterange/change_list.html"]
    inlines = [ItemInline,BankTransferInline]
    exclude = ('token',)

class CartAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class CartItemAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class BankTransferAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': admin.widgets.AdminFileWidget},
    }
    list_display = ['name', 'email','admin_image']
    exclude = 'money_transfer_slip',

class auth(models.Model):
    
    class Meta :
        verbose_name='ใบสั่งซื้อพร้อมสลิปโอนเงิน'
        verbose_name_plural="ใบสั่งซื้อพร้อมสลิปโอนเงิน"
    


admin.site.register(BankTransfer, BankTransferAdmin)
admin.site.site_header = 'Welcome KasetShop'
admin.site.register(product01,ProductAdmin)
admin.site.register(category01)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin,)

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

#admin.site.register(User)
#admin.site.register(Group)
