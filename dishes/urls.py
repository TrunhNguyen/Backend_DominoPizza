from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomLoginView


urlpatterns = [
    path('api/login', CustomLoginView.as_view(), name='custom_token_obtain_pair'),    
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/uncarting/<int:id>', views.uncarting, name='uncarting'),
    path('api/deletecart', views.deleteall, name='deleteall'),
    path('api/order', views.place_order, name='place_order'),
    path('api/pizza/<int:id>', views.pizza_detail, name = 'pizza_detail'),
    path('api/list', views.pizza_list, name='pizza_list'),
    path('api/orderlist', views.order_list, name='order_list'),
    path('api/carting/<int:id>', views.carting, name='carting'),
    path('api/register', views.register, name='register'),
    path('api/<str:version>/cart', views.view_cart, name='view_cart'),
    path('api/deleteorder/<int:id>', views.delete_order, name='deleteorder'),
    path('api/add', views.add_dish, name='add_dish'),
    path('api/delete/<int:id>', views.delete_dish, name='delete_dish')
]