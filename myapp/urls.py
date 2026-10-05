from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('supplements/', views.supplements_page_view, name='supplements_page'),
    path('supplements/add/', views.add_product_action, name='add_product_action'),
    path('supplements/delete/<int:product_id>/', views.delete_product_action, name='delete_product_action'),
    path('memberships/add/', views.add_membership_action, name='add_membership_action'),
    path('cart/decrease/<int:item_id>/', views.decrease_cart_quantity, name='decrease_cart_quantity'),
    path('memberships/delete/<int:product_id>/', views.delete_membership_action, name='delete_membership_action'),
    path('supplements/edit/<int:product_id>/', views.edit_product_action, name='edit_product_action'),
    path('memberships/cancel/', views.cancel_membership_view, name='cancel_membership'),
    path('about/', views.about_view, name='about'),
]