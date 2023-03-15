from rest_framework import serializers
from .models import Product, Category, Contact , OrderItem , CartItem,Checkout


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class CheckoutSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Checkout
        fields = ["pname","delivery"]
    def _str_(self):
        return self.pname
        