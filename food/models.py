from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

class Cuisine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    nick = models.CharField(max_length=10, blank=True)
    cuisine = models.ManyToManyField(Cuisine, related_name='restaurants')
    description = models.TextField(blank=True)
    phoneNumber = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)

    openTime = models.TimeField(blank=True, null=True)
    closeTime = models.TimeField(blank=True, null=True)
    orderTime = models.TimeField(blank=True, null=True)

    totalOrderCount = models.IntegerField(default=0)
    averageOrderTime = models.TimeField(blank=True, null=True)
    averageCost = models.IntegerField(blank=True, null=True)

    def calculateAvgCost(self, newOrder):
        # Create temp variable to store totalOrderCount to prevent data loss from save()
        tempCount = self.totalOrderCount + 1
        self.averageCost = (self.averageCost + newOrder.totalPrice) / tempCount
        self.totalOrderCount = tempCount
        self.save()

    def __str__(self):
        return self.name

class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_item', blank=True)

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='menu', null=True)

    # TODO When you order a MenuItem, it should increase the totalCount
    totalCount = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.price}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=100, blank=True)

    status = models.IntegerField(default=0)

    orderedTime = models.DateTimeField(null=True)
    confirmedTime = models.DateTimeField(null=True)
    deliveredTime = models.DateTimeField(null=True)

    totalPrice = models.IntegerField(default=0)

    # Pending --> Delivering status
    def confirm(self):
        self.status = 2
        self.confirmedTime = datetime.datetime.now()

        # Add cost of order to the average order cost for the restaurant
        restaurant = self.restaurant
        restaurant.calculateAvgCost(self)

        self.save()

        return f'Confirmed at {self.confirmedTime}'

    # Delivering --> Delivered status
    def delivered(self):
        self.status = 3
        self.deliveredTime = datetime.datetime.now()

        print(f'Order took: {self.deliveredTime} - {self.confirmedTime}')
        self.save()

        return f'Delivered at {self.deliveredTime}'

    # Pending --> Choosing status
    def rejected(self):
        self.status = 0
        self.save()

        return f'Rejected {self}'

    def __str__(self):
        return f'{self.user} -> {self.restaurant}, {self.status}'


class OrderItem(models.Model):
    orderList = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orders')

    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.menuItem} {self.count}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=64, blank=True)
    phoneNumber = models.CharField(max_length=64, blank=True)
    woodstock = models.BooleanField(default=False, blank=True)

    ownedRestaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='owners', null=True)

    birthDate = models.DateField(null=True, blank=True)

    totalSpent = models.IntegerField(default=0)

    def addCumulative(self, order):
        self.totalSpent += order.totalPrice
        self.save()

    def __str__(self):
        return f'{self.user}, {self.location}'

# Listeners that save the profile when the user is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        Profile.objects.create(user=instance)
        instance.profile.save()
