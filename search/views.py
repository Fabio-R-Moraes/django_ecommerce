from django.shortcuts import render
from django.views.generic import ListView
from products.models import Products

class SearchProductView(ListView):
    template_name= "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print("Solicitação", request)
        result = request.GET
        print("Resultado", result)
        query = result.get("q", None) #result['q']
        print("Consulta", query)

        if query is not None:
            return Products.objects.filter(title__icontains=query)

        return Products.objects.featured()
