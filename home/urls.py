from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name = "home"),
    path('product/<int:id>', views.product_detail, name = "product_detail"),
    path('product/addcomment/<int:id>', views.addcomment, name="addcomment"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.logout_func, name='logout'),
    path('signup/', views.signup, name="signup"),
    path('checkout/', views.checkout, name = "checkout"),
    path('cart/', views.cart, name = "cart"),
    path('about/', views.aboutus, name = "about"),
    path('contact/', views.contact, name = "contact"),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name="addtoshopcart"),
    path('cart/deletefromcart/<int:id>', views.deletefromcart, name = "deletefromcart"),
    path('store/', views.viewall,name="store"),
    path('women/',views.women, name = "women"),
    path('men/',views.men, name = "men"),
    path('user_profile/',views.user_profile, name="user_profile"),
    path('user_update/',views.user_update, name = "user_update"),
    path('user_profile/user_orders',views.user_orders, name = "user_orders")
]