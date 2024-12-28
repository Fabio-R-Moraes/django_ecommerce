from django.shortcuts import render, redirect
from .models import Cart
from products.models import Products

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, "carts/home.html", {})

def cart_update(request):
    product_id = 5
    #Pega o produto com o ID = 5
    product_obj = Products.objects.get(id=product_id)
    print(product_obj)
    #Cria ou pega a instância já existente do carrinho
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    #E o produto se associa a instância do campo M2M
    #cart_obj.products.add(product_obj) #cart_obj.products.add(product_id)
    #cart_obj.products.remove(product_obj) #cart_obj.products.remove(product_id)

    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        #E o produto se associa a instância do campo M2M
        cart_obj.products.add(product_obj)

    return redirect("carts:home")