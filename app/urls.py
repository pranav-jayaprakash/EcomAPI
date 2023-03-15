from django.urls import path

from .views import (
    CategoryList,
    ProductList,
    ProductOfferList,
    ProductDetail,
    AddToCart,
    Checkout,
    ContactCreate,
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    Categorycreate,
)

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/offers/', ProductOfferList.as_view(), name='product_offer_list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('cart/add/<int:pk>/', AddToCart.as_view(), name='add_to_cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('contact/create/', ContactCreate.as_view(), name='contact_create'),
    path('product/create/', ProductCreate.as_view(), name='product_create'),
    path('category/create/', Categorycreate.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),
]
