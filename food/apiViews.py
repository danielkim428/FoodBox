from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.serializers import serialize
from .models import *

from twilio.rest import Client

import random

import os

os.environ['TWILIO_ACCOUNT_SID'] = 'ACcd99094db783d1141bf1de6a0f4c1e5a'
os.environ['TWILIO_AUTH_TOKEN'] = 'e7b1fad4a5bff4685a0444bb77aba376'

def addItem(request, restaurantId, menuId):
    if not request.user.is_authenticated:
        context = {
            'status': 'Not allowed.'
        }
    else:
        menuItem = MenuItem.objects.get(id=menuId)
        restaurant = Restaurant.objects.get(id=restaurantId)

        # EXPLOIT CHECK: If restaurant ID = MenuItem's restaurant ID
        if (menuItem.category.restaurant.id != restaurant.id):
            return False

        context = {
            'name': menuItem.name,
            'category': menuItem.category.name,
            'price': menuItem.price
        }

        # Does the order list exist?
        try:
            orderList = Order.objects.get(user=request.user, status=0, restaurant=restaurant)
            context['newOrderList'] = False
            print('Order list already exists')
        # If not, create
        except:
            print('New order list created.')
            orderList = Order(user=request.user, status=0, restaurant=restaurant)
            orderList.save()

            context['newOrderList'] = True

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

        orderList.totalPrice += menuItem.price
        context['totalPrice'] = orderList.totalPrice

        orderItem.save()
        orderList.save()

        context['orderListId'] = orderList.id

        # Previously, there were NO ITEMS ordered
        if (orderList.items.count() == 1):
            print('No items WERE ordered.')
            context['newOrderList'] = True

    return JsonResponse(context)

def removeItem(request, orderedId):
    if not request.user.is_authenticated:
        context = {
            'status': 'Not allowed.'
        }
    else:
        context = {}

        orderItem = OrderItem.objects.get(id=orderedId)
        orderList = orderItem.orderList

        context['orderId'] = orderedId

        orderList.totalPrice -= orderItem.menuItem.price
        orderList.save()

        # If only one ordered, then the OrderItem model should be deleted
        if (orderItem.count == 1):
            orderItem.delete()

            context['count'] = 0
        else:
            orderItem.count -= 1
            orderItem.save()

            context['count'] = orderItem.count

        # If there is NO ITEM ORDERED, tell the user
        if (orderList.items.count() == 0):
            print('No items ordered.')
            context['none'] = True
        else:
            context['none'] = False

        context['totalPrice'] = orderList.totalPrice
    return JsonResponse(context)

def phoneNumberAPI(request, phoneNumber):
    client = Client()

    from_whatsapp_number="whatsapp:+14155238886"
    to_whatsapp_number="whatsapp:+82" + phoneNumber

    otp = str(random.randint(123456, 987654))

    user = request.user
    user.profile.otp = otp
    user.profile.save()

    print(user.profile.otp)

    client.messages.create(body='[OrderIn]\nYour OTP code is ' + otp,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)

    context = {
        'otp': otp
    }

    return JsonResponse(context)
