from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from .models import Product

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
            context['substitutes'] = Product.objects.order_by(
                'nutriscore').filter(
                Q(categories__name__icontains=categories[0].name) &
                Q(categories__name__icontains=categories[1].name) &
                (Q(nutriscore='a') | Q(nutriscore='b')))
            return context
        except IndexError:
            context['substitutes'] = Product.objects.order_by(
                'nutriscore').filter(
                Q(categories__name__icontains=categories[0].name) &
                (Q(nutriscore='a') | Q(nutriscore='b')))
            return context


class SubstituteDetailView(DetailView):
    model = Product
    context_object_name = 'substitute'
    template_name = 'openfoodfacts/substitute_detail.html'


"""
class SubstituteUpdateView(UpdateView):
    model = CustomUser
    fields = ('substitute', )
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        print(pk)
"""


class UserSubstitutesListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    context_object_name = 'user_substitutes_list'
    template_name = 'openfoodfacts/user_substitutes.html'

    def get_queryset(self):
        products = Product.objects.filter(
            Q(
                id__in=get_user_model().objects.filter(
                    id=self.request.user.id).values('substitute'))
        )
        return products


@login_required(login_url='account_login')
def saveSubstitute(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    user.substitute.add(product)
    user.save()
    return redirect('home')
