from django.db import models
from django.contrib.auth.models import User

class Cuisine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    nick = models.CharField(max_length=10, blank=True)
    cuisine = models.ManyToManyField(Cuisine, related_name='restaurants')
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)

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

    total_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.price}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')

    status = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} -> {self.restaurant}, {self.status}'


class OrderItem(models.Model):
    orderList = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orders')

    price = models.IntegerField(default=0)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.menuItem} {self.count}'
