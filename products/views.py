from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Products
from carts.models import Cart

class ProductFeaturedListView(ListView):
    template_name= "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Products.objects.featured()
    
class ProductFeaturedDetailView(DetailView):
    queryset = Products.objects.all().featured()
    template_name= "products/featured-detail.html"

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

class ProductDetailSlugView(DetailView):
    queryset = Products.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj

        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Products, slug=slug, active=True)

        try:
            instance = Products.objects.get(slug=slug, active=True)
        except Products.DoesNotExist:
            raise Http404("Não encontrado!!!!")
        except Products.MultipleObjectsReturned:
            qs = Products.objects.filter(slug=slug, active=True)
            instance = qs.first()

        return instance

#Class Based Views
class ProductDetailView(DetailView):
    #queryset = Products.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context
    
    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Products.objects.get_by_id(pk)

        if instance is None:
            raise Http404("Esse produto NÃO existe!!!")
        
        return instance

#Function Based Views
def product_detail_view(request, pk=None, *args, **kwargs):
    instance = Products.objects.get_by_id(pk)
    print(instance)

    if instance is None:
        raise Http404("Esse produto NÃO existe!!!")
    
    context = {
        'object': instance,
    }

    return render(request, "products/detail.html", context)