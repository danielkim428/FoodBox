from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.serializers import serialize
from .models import *

def addItem(request, restaurantId, menuId):
    if not request.user.is_authenticated:
        context = {
            'status': 'Not allowed.'
        }
    else:
        menuItem = MenuItem.objects.get(id=menuId)
        restaurant = Restaurant.objects.get(id=restaurantId)

        context = {
            'name': menuItem.name,
            'category': menuItem.category.name,
            'price': menuItem.price
        }

        # Does the order list exist?
        try:
            orderList = Order.objects.get(user=request.user, status=0, restaurant=restaurant)
            print('Order list already exists')
        # If not, create
        except:
            print('New order list created.')
            orderList = Order(user=request.user, status=0, restaurant=restaurant)
            orderList.save()

        # Has this item been ordered yet?
        try:
            orderItem = OrderItem.objects.get(menuItem=menuItem, orderList=orderList)
            print('Item already been ordered.')

            # Alert the API that this orderItem is NOT new
            context['new'] = False
        except:
            print('Never been ordered before.')
            orderItem = OrderItem(menuItem=menuItem, orderList=orderList, price=menuItem.price, count=0)
            orderItem.save()

            # Alert the API that this orderItem is new
            context['new'] = True

        orderItem.count += 1

        # Update orderItem price
        orderItem.price = orderItem.count * menuItem.price
        context['orderId'] = orderItem.id

        orderList.totalPrice += orderItem.price

        orderItem.save()
        orderList.save()
    return JsonResponse(context)

def removeItem(request, orderedId):
    if not request.user.is_authenticated:
        context = {
            'status': 'Not allowed.'
        }
    else:
        orderItem = OrderItem.objects.get(id=orderedId)
        orderList = orderItem.orderList

        orderList.totalPrice -= orderItem.price
        orderList.save()

        # If only one ordered, then the OrderItem model should be deleted
        if (orderItem.count == 1):
            orderItem.delete()

            context = {
                'count': 0
            }
        else:
            orderItem.count -= 1
            orderItem.save()

            context = {
                'count': orderItem.count
            }
    return JsonResponse(context)
