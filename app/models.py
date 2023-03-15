from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Contact(models.Model):
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

class Checkout(models.Model):

    pname= models.ForeignKey(CartItem,on_delete=models.CASCADE,related_name="productname")
    delivery= models.ForeignKey(Contact,on_delete=models.CASCADE)
    

    def _str_(self):
        return self.pname