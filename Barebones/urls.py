from django.urls import path
from Barebones import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/<int:pk>/purchase/', views.ProductPurchase.as_view()),
    path('products/<int:pk>/addcart/', views.AddCart.as_view()),
    path('products/avl/', views.ProductAvlList.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.api_root),
    path('cart/', views.ViewCart.as_view(),name='cart-list'),
    path('cart/checkout/', views.CheckoutCart.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
