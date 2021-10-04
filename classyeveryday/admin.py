from django.contrib import admin

from .models import Item, OrderItem , Order, Payment, Address, Coupon , UserProfile, Refund, Wishlist,Contact,Variation,Multipleimages


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                    ]
    search_fields = [
        'user__username',
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'order_id',
        'pincode',
        'state',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type','state','order_id']
    search_fields = ['user', 'street_address', 'apartment_address','order_id', 'pincode','state']

class VariationAdmin(admin.ModelAdmin):
    list_display = [
        'item',
        'size'
    ]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'price', 'discount_price', 'subcategory','label']
    list_filter = ['subcategory', 'slug', 'discount_price', 'category']
    list_editable = ['price', 'category', 'label']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Refund)
admin.site.register(Wishlist)
admin.site.register(Order,OrderAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(UserProfile)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Contact)
admin.site.register(Multipleimages)



