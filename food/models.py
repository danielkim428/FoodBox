from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_item', blank=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.cost)


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    nick = models.CharField(max_length=10, blank=True)
    cuisine = models.ManyToManyField(Cuisine, related_name='restaurants')
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    menu = models.ManyToManyField(MenuItem, blank=True, related_name="items")

    def __str__(self):
        return self.name
