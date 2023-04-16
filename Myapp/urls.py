from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('',views.home, name='home'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart-detail',views.cart_detail, name='cart-detail'),
    path('register', views.register, name="register"),
    path('login',views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('details/<slug:slug>',views.details, name="details"),
    path('check-out', views.checkout , name='checkout'),
    path('order',views.order, name='order'),
    path('restaurants',views.restaurants, name = 'restaurants'),
    path('restaurant_details/<slug:slug>',views.restaurant_details, name = 'restaurant-details'),
    path('delete/<str:product_id>', views.delete, name = 'delete'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    
]



# htmx_pattern = [
#      path('delete/<str:product_id>', views.delete, name = 'delete')
# ]
# urlpatterns += htmx_pattern
# if settings.DEBUG:
#     urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)