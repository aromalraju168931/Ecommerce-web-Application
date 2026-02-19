from django.urls import path
from .import views
urlpatterns = [
    path('',views.otp_login,name="verification_part1"),
    path('verification/',views.verify_otp,name="verification_part2"),
    path('index_page/',views.index_page,name='index_page'),
    path('add_products/',views.products_upload,name='add_products'),
    path('registration/',views.user_reg,name="user_reg"),
    path('profile/',views.profile_view,name="profile_view"),
    path('category/',views.addCategory,name="add_cat"),
    path('subcategory/',views.addsubCategory,name="add_sub_cat"),
    path('list_your_products/',views.list_products,name="list_products"),
    path('add_to_cart/<int:id>/',views.add_to_cart,name="add_to_cart"),
    path('cart/',views.cart_view,name="cart_view"),
    path('delete_cart/<int:id>/',views.del_cart_items,name="del_cart"),
    path('update_cart/<int:id>/',views.update_cart,name="update_cart"),
]