from django.shortcuts import render
from .forms import ContactForm

def home_page(request):
    print(request.session.get("first_name", "Unknow"))
    context = {
        "title": "Página Principal",
        "content": "Bem-vindo à página Principal...",
    }

    if request.user.is_authenticated:
        context["premium_content"] = "Você é um usuário premium!!!"

    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title": "Página About",
        "content": "Bem-vindo à Página About...",
    }
    return render(request, "about/view.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Formulário de Contato",
        "content": "Bem-vindo à Página de Contato...",
        "form": contact_form,
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    #if request.method == "POST":
    #    print(request.POST)
    #    print(request.POST.get('fullname'))
    return render(request, "contact/view.html", context)