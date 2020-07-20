from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("restaurant/<int:restaurant_id>", views.restaurant, name='restaurant'),
    path("cuisine/<currentCuisine>", views.cuisine, name='cuisine'),
    path("cuisines", views.cuisines, name='cuisines'),

    path("orders", views.orders, name='orders'),

    path("login", views.login_view, name='login'),
    path("logout", views.logout_view, name='logout'),
    path("register", views.register, name='register'),

    path("about", views.about, name='about'),
]
