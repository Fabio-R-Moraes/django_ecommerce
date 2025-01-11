from django.shortcuts import render, redirect
from .models import Cart
from products.models import Products
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm

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

def checkout_home(request):
    #Aqui você pega o carrinho
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    #Se o carrinho acabou de ser criado, ele está zerado
    #ou se o carrinho já existe, mas não tem nada dentro
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
    }

    return render(request, "carts/checkout.html", context)