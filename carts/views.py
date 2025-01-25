from django.shortcuts import render, redirect
from .models import Cart
from products.models import Products
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address
from django.http import JsonResponse

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, "carts/home.html", {"cart": cart_obj})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

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
            added = False
        else:
            #E o produto se associa a instância do campo M2M
            cart_obj.products.add(product_obj)
            added = True

        request.session['cart_itens'] = cart_obj.products.count()
        #return redirect(product_obj.get_absolute_url())

        if is_ajax(request=request):
            print("Essa é uma requisição Ajax!!!")
            json_data = {
                "added":added,
                "removed": not added,
                "cartItemCount":cart_obj.products.count()
            }

            return JsonResponse(json_data)

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
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]

        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]

        if shipping_address_id or billing_profile:
            order_obj.save()

    if request.method == "POST":
        #Verifica se o pedido foi feito
        is_done = order_obj.check_done()

        if is_done:
            order_obj.mark_paid()
            request.session["cart_items"] = 0
            del request.session["cart_id"]

            return redirect("cart:success")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }

    return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
    return render(request, "carts/checkout_done.html", {})