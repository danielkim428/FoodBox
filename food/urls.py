from django.urls import path
from . import views
from . import apiViews

urlpatterns = [
    path("", views.index, name='index'),
    path("restaurant/<int:restaurantId>", views.restaurant, name='restaurant'),
    path("cuisine/<currentCuisine>", views.cuisine, name='cuisine'),
    path("cuisines", views.cuisines, name='cuisines'),
    path("address", views.address, name='address'),

    path("orders", views.orders, name='orders'),

    path("login", views.login_view, name='login'),
    path("logout", views.logout_view, name='logout'),
    path("register", views.register, name='register'),

    path("about", views.about, name='about'),

    path("api/menu/addOrderItem/<int:restaurantId>/<int:menuId>", apiViews.addItem),
    path("api/menu/removeOrderItem/<int:orderedId>", apiViews.removeItem)
]
