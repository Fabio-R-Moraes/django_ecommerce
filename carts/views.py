from django.shortcuts import render

def cart_home(request):
    cart_id = request.session.get("cart_id", None)
    
    if cart_id is None:
        print("Criado um novo carrinho!!!")
        request.session["cart_id"] = 12
    else:
        print("CART_ID já existe...")

    return render(request, "carts/home.html", {})