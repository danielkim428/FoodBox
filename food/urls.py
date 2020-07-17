from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("restaurant/<int:restaurant_id>", views.restaurant, name='restaurant'),
    path("cuisine/<currentCuisine>", views.cuisine, name='cuisine')
]
