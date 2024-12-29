from django.shortcuts import render, redirect
from .models import Cart
from products.models import Products

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get("product_id")

    if product_id is not None:
        try:
            product_obj = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            print("Mostrar mensagem ao usuário...  Esse produto acabou!!!")
            return redirect("cart:home")

    #Cria ou pega a instância já existente do carrinho
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        #E o produto se associa a instância do campo M2M
        cart_obj.products.add(product_obj)

    request.session['cart_itens'] = cart_obj.products.count()

    return redirect("carts:home")