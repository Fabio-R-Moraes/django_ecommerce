from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    context = {
        "title": "Página Principal",
        "content": "Bem-vindo à página Principal...",
    }
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title": "Página About",
        "content": "Bem-vindo à Página About...",
    }
    return render(request, "about/view.html", context)

def contact_page(request):
    context = {
        "title": "Página Contact",
        "content": "Bem-vindo à Página Contact...",
    }
    return render(request, "contact/view.html", context)