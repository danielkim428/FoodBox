from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count, Exists, OuterRef
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *

import datetime

# Create your views here
def index(request):
    context = {
        "restaurants": Restaurant.objects.all(),
        "cuisine": Cuisine.objects.all(),
        "currentTime": datetime.datetime.now(),
    }

    # For restaurant owners
    if request.user.is_authenticated:
        context["ownedRestaurant"] = request.user.profile.ownedRestaurant

    return render(request, "food/index.html", context)

def orders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        context = {
            "choosingOrders": request.user.orders.annotate(num_items=Count('items')).filter(status=0).exclude(num_items=0),
            "pendingOrders": request.user.orders.filter(status=1),
            "deliveringOrders": request.user.orders.filter(status=2),
            "deliveredOrders": request.user.orders.filter(status=3),
            "phoneNumber": request.user.profile.phoneNumber
        }

        return render(request, "food/orders.html", context)

def restaurantOrders(request, restaurantId):
    restaurant = Restaurant.objects.get(id=restaurantId)

    if request.user.profile.ownedRestaurant == restaurant:
        if request.method == 'POST':
            action = request.POST['action']
            orderId = request.POST['order-id']
            order = Order.objects.get(id=orderId)

            if action == 'confirm':
                # Pending --> Delivering status
                order.status = 2

                # TODO WhatsApp bot to customer
            elif action == 'delivered':
                # Delivering --> Delivered status
                order.status = 3

                # TODO WhatsApp bot to customer
            elif action == 'reject':
                # Pending --> Choosing status
                order.status = 0

                # TODO WhatsApp bot to customer

            order.save()
            return HttpResponseRedirect(reverse('restaurantOrders', args=[restaurantId]))
        else:
            context = {
                "restaurant": restaurant,
                "pendingOrders": restaurant.orders.filter(status=1),
                "deliveringOrders": restaurant.orders.filter(status=2),
                "deliveredOrders": restaurant.orders.filter(status=3),
            }

            return render(request, "food/restaurantOrders.html", context)
    else:
        return HttpResponseRedirect(reverse('index'))

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
        raise Http404("Restaurant does not exist")

    context = {
        "restaurant": restaurant,
        "categories": restaurant.categories.all(),
        "currentTime": datetime.datetime.now(),
        "phoneNumber": request.user.profile.phoneNumber
        # "menuItems": MenuItem.objects.filter(category__restaurant=restaurant)
    }

    if request.user.is_authenticated:
        if request.method == 'POST':
            orderId = request.POST['orderId']
            order = Order.objects.get(id=orderId)

            if request.user.profile.phoneNumber == '':
                return HttpResponseRedirect(reverse('phoneNumber'))

            return HttpResponseRedirect(reverse('address', args=[restaurantId]))
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

@login_required
def address(request, restaurantId):
    try:
        restaurant = Restaurant.objects.get(pk=restaurantId)
    except Post.DoesNotExist:
        raise Http404("Restaurant does not exist")

    context = {
        "restaurant": restaurant
    }

    if request.user.is_authenticated:
        if request.method == 'POST':
            address = request.POST['address']
            if address == "":
                return HttpResponseRedirect(reverse('address', args=[restaurantId]))
            else:
                orderId = request.POST['orderId']
                order = Order.objects.get(id=orderId)
                order.address = address
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
                return HttpResponseRedirect(reverse('restaurant', args=[restaurantId]))
                print('Something went wrong.')
    else:
        context['loggedIn'] = False
    return render(request, "food/address.html", context)


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

# People who register are redirected to this view to confirm their phone number
# TODO WhatsApp bot integration
def phoneNumber(request):
    try:
        lastURL = request.META.get('HTTP_REFERER')[-1:]
        if lastURL.isnumeric():
            context = {
                "url": lastURL
            }
        else:
            context = {
                "url": ""
            }
    except:
        context = {
            "url": ""
        }

    if request.user.is_authenticated:
        if request.method == 'POST':
            phoneNumber = request.POST['phoneNumber']
            print(phoneNumber)

            # TODO
            user = request.user
            user.profile.phoneNumber = phoneNumber
            user.save()

            pageNumber = request.POST['pageNumber']
            if pageNumber == "":
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('address', args=[pageNumber]))
        else:
            return render(request, 'food/phoneNumber.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def logout_view(request):
    logout(request)
    return render(request, "food/login.html", {"message": "Logged out."})

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        try:
            new_user = User.objects.create_user(username, password=password, first_name=first_name, last_name=last_name)
            new_user.save()

        except IntegrityError:
            return render(request, 'food/register.html', {"message": "User already exists"})
        except:
            return render(request, 'food/register.html', {"message": "Invalid credentials."})

        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'food/register.html')
