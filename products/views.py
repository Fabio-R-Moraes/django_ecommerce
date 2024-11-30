from django.views.generic import ListView
from django.shortcuts import render
from .models import Products

#Class Based Views
class ProductListView(ListView):
    queryset = Products.objects.all()
    template_name= "products/list.html"

#Function Based Views
def product_list_view(request):
    queryset = Products.objects.all()
    context = {
        'object_list': queryset,
    }

    return render(request,"products/list.html", context)