from django.shortcuts import render
from django.views.generic import ListView
from products.models import Products

class SearchProductView(ListView):
    template_name= "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        context["query"] = query
        #SearchQuery.objects.create(query=query)

        return context 

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print("Solicitação", request)
        result = request.GET
        print("Resultado", result)
        query = result.get("q", None) #result['q']
        print("Consulta", query)

        if query is not None:
            return Products.objects.search(query)

        return Products.objects.featured()
