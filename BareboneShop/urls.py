from django.urls import path
from . import views

app_name = 'BareboneShop'
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('product/all/', views.allproduct, name='allproduct'),
    path('product/<int:product_id>/buy', views.buyproduct, name='buyproduct'),
    path('product/all/avl', views.avlproducts, name='avlproducts'),
    path('product/<int:product_id>/success', views.purchase, name='purchase'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('completecart/', views.completecart, name='completecart'),
    path('completecart/success', views.successcart, name='successcart')
]
