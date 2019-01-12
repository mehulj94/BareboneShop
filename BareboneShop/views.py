from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import ast


def index(request):
    return HttpResponse(render(request, 'BareboneShop/index.html', ))


def product(request, product_id):
    amc = get_object_or_404(Product, pk=product_id)
    return HttpResponse(render(request, 'BareboneShop/product.html', {'product': amc}))


def allproduct(request):
    amc = Product.objects
    return HttpResponse(render(request, 'BareboneShop/allproduct.html', {'products': amc}))


def avlproducts(request):
    amc = Product.objects.filter(inventory_cnt__gt=1)
    return HttpResponse(render(request, 'BareboneShop/allproduct.html', {'products': amc}))


def purchase(request, product_id):
    amc = get_object_or_404(Product, pk=product_id)
    return HttpResponse(render(request, 'BareboneShop/purchase.html', {'products': amc}))


def viewcart(request):
    cart = request.session.get('cart', [])
    product_dic = cart
    total_amt = 0

    for i in cart:
        amc = get_object_or_404(Product, pk=i[0])
        if i[3] > amc.inventory_cnt:
            return HttpResponse(
                render(request, 'BareboneShop/cartview.html',
                       {'error_message': 'Quantity not available! Please Start Session again'}))

        total_amt += i[2] * i[3]

    return HttpResponse(render(request, 'BareboneShop/cartview.html', {'products': product_dic, 'total': total_amt}))


def completecart(request):
    cart_data = ast.literal_eval(request.POST.get('Checkout'))
    for i in range(len(cart_data)):
        amc = get_object_or_404(Product, pk=cart_data[i][0])
        amc.inventory_cnt = amc.inventory_cnt - cart_data[i][3]
        amc.save()

    del request.session['cart']
    return HttpResponseRedirect(reverse('BareboneShop:successcart', args=()))


def successcart(request):
    return HttpResponse(render(request, 'BareboneShop/purchase.html'))


@require_http_methods(["POST"])
def buyproduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_qty = 1

    if product.inventory_cnt > 0 and request.POST.get('buybutton') == 'Buy!':

        product.inventory_cnt = product.inventory_cnt - 1
        product.save()

    elif product.inventory_cnt > 0 and request.POST.get('addcart') == 'Add to cart':

        cart = request.session.get('cart', [])
        buy1 = [product.product_id, product.title, product.price, product_qty]
        flag = False
        if len(cart) > 0:
            for i in range(len(cart)):
                if product.product_id != cart[i][0]:
                    flag = True
                else:
                    flag = False
                    cart[i][3] += 1
                    break
        else:
            cart.append(buy1)

        if flag == True:
            cart.append(buy1)

        request.session['cart'] = cart
        return redirect('BareboneShop:avlproducts')

    else:
        return HttpResponse(render(request, 'BareboneShop/EmptyInventory.html',
                                   {'product': product, 'error_message': "Inventory is empty!!!"}))
    return HttpResponseRedirect(reverse('BareboneShop:purchase', args=(product.product_id,)))
