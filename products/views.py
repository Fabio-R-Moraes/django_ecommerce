from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
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

#Class Based Views
class ProductDetailView(DetailView):
    queryset = Products.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

#Function Based Views
def product_detail_view(request, pk=None, *args, **kwargs):
    #instance = Products.objects.get(pk=pk)
    #instance = get_object_or_404(Products, pk=pk)
    qs = Products.objects.filter(id=pk)

    if qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Esse produto NÃO está cadastrado!!!")
    
    context = {
        'object': instance,
    }

    return render(request, "products/detail.html", context)