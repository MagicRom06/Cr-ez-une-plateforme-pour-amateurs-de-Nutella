from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from django.db.models import Q

# Create your views here.

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'openfoodfacts/search_results.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        return Product.objects.filter(
            Q(name__icontains=search)
        )


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'openfoodfacts/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        categories = self.object.categories.all()
        try:
            context['substitutes'] = Product.objects.order_by('nutriscore').filter(
                Q(categories__name__icontains=categories[0].name) & 
                Q(categories__name__icontains=categories[1].name) &
                (Q(nutriscore='a') | Q(nutriscore='b')))
            return context
        except IndexError:
            context['substitutes'] = Product.objects.order_by('nutriscore').filter(
                Q(categories__name__icontains=categories[0].name) & 
                (Q(nutriscore='a') | Q(nutriscore='b')))
            return context


class SubstituteDetailView(DetailView):
    model = Product
    context_object_name = 'substitute'
    template_name = 'openfoodfacts/substitute_detail.html'


class SubstituteCreateView(CreateView):
    pass
