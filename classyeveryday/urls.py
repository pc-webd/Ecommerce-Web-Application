from django.urls import path
from . import views

app_name='classyeveryday'

urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('product/<slug>/',views.ItemDetailView.as_view(),name='productDetail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('allproducts/', views.allprod, name='allprod'),
    path('contact/', views.contact, name='contact'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-cart/<slug>',views.add_to_cart,name='add-to-cart'),
    path('add-qty-to-cart/<slug>',views.add_qty_to_cart,name='add-qty-to-cart'),
    path('add-to-wishlist/<slug>',views.add_to_wishlist,name='add-to-wishlist'),
    path('remove-to-wishlist/<slug>',views.remove_to_wishlist,name='remove-to-wishlist'),
    path('success/',views.success,name='success'),
    path('payment/',views.PaymentView.as_view(),name='payment'),
    path('remove-from-cart/<slug>',views.remove_from_cart,name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/',views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('myorders/', views.order, name='order'),
    path('products/', views.products, name='products'),
    path('items/', views.catprod, name='catprod'),
    path('privacy/', views.privacy, name='privacy'),
    path('tnc/', views.tnc, name='tnc'),
    path('refund/', views.refund, name='refund'),   
    path('search/', views.search,name='search'),
    path('token/',views.token,name='token'),
    path('verify/<auth_token>',views.verify_user),
    path('success_verified_user/',views.success_verified),
    path('forgot_psw/',views.forgot_psw,name='forgot_psw'),
    path('change_psw/<reset_psw_token>',views.change_psw)
]   