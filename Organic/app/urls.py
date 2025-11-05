from django.urls import path

from . import views

# Register your URL patterns here.
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/add/combo/<int:combo_id>/', views.add_combo_to_cart, name='add_combo_to_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('blog/', views.blog, name='blog'),
    path('productlist/', views.productlist, name='productlist'),
    path('product/<int:product_id>/', views.productdetail, name='productdetail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('policy/', views.policy, name='policy'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('search/', views.search, name='search'),
    path('auth/', views.authpage, name='auth'),
    path('logout/', views.logoutPage, name='logout'),
    path('myaccount/edit/', views.editaccount, name='editaccount'),
    path('applycoupon/', views.applycoupon, name='applycoupon'),
    path('combo/<int:combo_id>/', views.combodetail, name='combodetail'),
    path("cart/clear-or-remove/", views.clear_or_remove_selected, name="clear_or_remove_selected"),
    path("changeavatar/", views.changeavatar, name="changeavatar"),
]


