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
        "restaurants": Restaurant.objects.all()
    }
    return render(request, "food/index.html", context)

def cuisine(request, currentCuisine):
    category = Cuisine.objects.get(name=currentCuisine)

    context = {
        "cuisine": currentCuisine,
        "restaurants": Restaurant.objects.filter(cuisine=category).all()
    }
    return render(request, "food/cuisine.html", context)
