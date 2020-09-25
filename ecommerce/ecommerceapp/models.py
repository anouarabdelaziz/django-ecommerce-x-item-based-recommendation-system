from django.db import models
from django.conf import settings
from urllib.parse import urlparse
import os

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    asin = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(null = True, max_digits=7, decimal_places=2)
    description = models.CharField(max_length=6000, blank=True, null=True)
    #img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
        
    
    @property
    def imgURL(self):
        base_dir = os.getcwd()
        path=os.path.join(base_dir, 'static/images')
        o = os.listdir(path)

        url = 'http://127.0.0.1:8000/images/not_available.jpg'
        for i in o:
            if(i.startswith(self.asin)):
                print(i)
                url = f'http://127.0.0.1:8000/images/{self.asin}-image.png'
            
        return url



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    complete = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    @property
    def order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(i.quantity*i.item.price for i in orderitems)
        return total

class Orderitem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity*self.item.price
        return total
    


