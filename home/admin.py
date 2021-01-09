from django.contrib import admin

from product.models import Product,Comment, ProductCategories
from order.models import ShopCart, Order, OrderProduct
from home.models import Setting, ContactMessage
from user.models import UserProfile

# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at','status']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'update_at','image']

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user', 'quantity','price','amount']
    list_filter = ['user']

admin.site.register(ProductCategories)
admin.site.register(Product,ProductAdmin)
admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage)
admin.site.register(UserProfile)
admin.site.register(Comment)


#start from here https://www.youtube.com/watch?v=OvTs8BMLb7o&list=PLIUezwWmVtFXaHcJ63ZM6uOJdhMrnZFFk&index=17