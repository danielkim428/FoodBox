from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

# Create your views here
def index(request):
    context = {
        "restaurants": Restaurant.objects.all(),
        "cuisine": Cuisine.objects.all(),
    }
    return render(request, "food/index.html", context)

def cuisine(request, currentCuisine):
    category = Cuisine.objects.get(name=currentCuisine)

    context = {
        "cuisine": currentCuisine,
        "restaurants": Restaurant.objects.filter(cuisine__name=category).all()
    }
    return render(request, "food/cuisine.html", context)

def restaurant(request, restaurant_id):
  try:
      restaurant = Restaurant.objects.get(pk=restaurant_id)
  except Post.DoesNotExist:
      raise Http404("Post does not exist")
  context = {
      "restaurant": restaurant,
  }
  return render(request, "food/restaurant.html", context)
