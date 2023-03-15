from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import status
from .models import Product, Category, Contact  
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Category, Contact,Checkout, OrderItem  , CartItem
from .serializers import ProductSerializer, CategorySerializer, ContactSerializer,CheckoutSerializer,CartItemSerializer,OrderItemSerializer


# Create your views here.
#JWT token authentication

class ObtainTokenPairWithCookieView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['access']
        print(token)
        response.set_cookie('jwt', token, max_age=3600, httponly=True)
        return response



class TokenBlacklistView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")


# Category List
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product List
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    #product filter
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if category:
            queryset = queryset.filter(category__name=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

#Product on offer
class ProductOfferList(generics.ListAPIView):
    queryset = Product.objects.filter(discount__isnull=False)
    serializer_class = ProductSerializer

#Product Detail
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#Add product to cart
class AddToCart(generics.CreateAPIView):
    queryset = CartItem.objects.all() 
    serializer_class = CartItemSerializer  

    def post(self, request, pk):
        Prod_name = Product.objects.get(id=pk)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            # Check if item is already in the cart
            try:
                cart_item = CartItem.objects.get(product=Prod_name)
                cart_item.quantity += quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                # Add item to cart
                cart_item = CartItem(product=Prod_name, quantity=quantity)
                cart_item.quantity = quantity
                cart_item.save()
            # return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Checkout Product
class Checkout(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSerializer

    def perform_create(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        pname = serializer.data["pname"]

        # Send mail
        user_email = self.request.user.email
        subject = 'Thank you for your purchase'
        message = 'Dear {},\n\nThank you for your purchase. Your order for {} has been successfully processed.'.format(
            self.request.user.username, pname)
        from_email = 'pranavjayaprakashn1998@gmail.com'
        recipient_list = [user_email]
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=True)
        return Response("pname")

#Category Create
class Categorycreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#Contact Create
class ContactCreate(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

#Product Create
class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#Product Update/Edit
class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#Product Delete
class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

#Logout
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            TokenRefreshView().post(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)