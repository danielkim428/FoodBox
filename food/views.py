from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count, Exists, OuterRef
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

import datetime

# Create your views here
def index(request):
    context = {
        "restaurants": Restaurant.objects.all(),
        "cuisine": Cuisine.objects.all(),
        "currentTime": datetime.datetime.now()
    }

    return render(request, "food/index.html", context)

def address(request):
    context = {
        "restaurants": Restaurant.objects.all(),
        "cuisine": Cuisine.objects.all(),
    }
    return render(request, "food/address.html", context)

def orders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        context = {
            "orders": request.user.orders.all()
        }

        return render(request, "food/orders.html", context)

def about(request):
    return render(request, "food/about.html")

def cuisines(request):
    context = {
        "cuisines": Cuisine.objects.all(),
    }
    return render(request, "food/cuisines.html", context)

def cuisine(request, currentCuisine):
    #currentCuisine = currentCuisine.lower()
    currentCuisine = currentCuisine
    print(currentCuisine)

    try:
        category = Cuisine.objects.get(name=currentCuisine)
    except:
        raise Http404("Cuisine does not exist")

    context = {
        "cuisine": currentCuisine,
        "restaurants": Restaurant.objects.filter(cuisine__name=category).all(),
        "currentTime": datetime.datetime.now(),
    }

    return render(request, "food/cuisine.html", context)

def restaurant(request, restaurantId):
    try:
        restaurant = Restaurant.objects.get(pk=restaurantId)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    context = {
        "restaurant": restaurant,
        "categories": restaurant.categories.all(),
        "currentTime": datetime.datetime.now()
        # "menuItems": MenuItem.objects.filter(category__restaurant=restaurant)
    }

    if request.user.is_authenticated:
        if request.method == 'POST':
            orderId = request.POST['orderId']
            order = Order.objects.get(id=orderId)
            order.status = 1
            order.save()

            return HttpResponseRedirect(reverse('orders'))
        else:
            context['loggedIn'] = True

            try:
                currentOrder = Order.objects.get(user=request.user, restaurant=restaurant, status=0)

                # subquery = OrderItem.objects.filter(orderList=currentOrder, menuItem=OuterRef('pk'))
                # context["menuItems"] = MenuItem.objects.filter(category__restaurant=restaurant)\
                    # .annotate(userOrdered=Exists(subquery))

                context['currentOrder'] = currentOrder
            except:
                print('No current order')
    else:
        context['loggedIn'] = False

    return render(request, "food/restaurant.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'food/login.html', {"message": "Invalid credentials."})
    else:
        return render(request, 'food/login.html')

def logout_view(request):
    logout(request)
    return render(request, "food/login.html", {"message": "Logged out."})

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        try:
            new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            new_user.save()

        except IntegrityError:
            return render(request, 'food/register.html', {"message": "User already exists"})
        except:
            return render(request, 'food/register.html', {"message": "Invalid credentials."})

        return HttpResponseRedirect(reverse('login'))

    else:
        return render(request, 'food/register.html')
