from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
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

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }
    print("Usuário logado!!!")
    #print(request.user.is_authenticated)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        #print(request.user.is_authenticated)

        if user is not None:
            #print(request.user.is_authenticated)
            login(request, user)
            print("Login válido!!!")
            return redirect("/")
        else:
            print("Login inválido...")

    return render(request, "auth/login.html", context)

def logout_page(request):
    context = {
        "content": "Você efetuou o logout com sucesso!!! :)"
    }
    logout(request)
    return render(request, "auth/logout.html", context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {

        "form": form,
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)

    return render(request, "auth/register.html", context)
