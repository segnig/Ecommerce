from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True) 
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except: 
            url = '' 
        return url  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(null=True, blank=True, auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        
        return shipping
    
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    date_added = models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product is not None:
            total = self.product.price * self.quantity
        else:
            total = 0
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state= models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.address


