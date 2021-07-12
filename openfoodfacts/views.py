from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
import logging

from .models import Product, Substitute

# Create your views here.

logger = logging.getLogger(__name__)


class SearchResultsListView(ListView):
    """
    View used for searching product
    """
    model = Product
    context_object_name = 'product_list'
    template_name = 'openfoodfacts/search_results.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        logger.info('New search', exc_info=True, extra={
            'search':search,
        })
        return Product.objects.filter(
            Q(name__icontains=search)
        )


class ProductDetailView(DetailView):
    """
    View used to get detail product page
    """
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
    """
    View used to get detail substitute page
    """
    model = Product
    context_object_name = 'substitute'
    template_name = 'openfoodfacts/substitute_detail.html'


class UserSubstitutesListView(LoginRequiredMixin, ListView):
    """
    View used to get substitute list saved by user
    """
    model = Substitute
    context_object_name = 'user_substitutes_list'
    template_name = 'openfoodfacts/user_substitutes.html'

    def get_queryset(self):
        substitute = Substitute.objects.filter(
            Q(
                user=self.request.user.id
            )
        )
        return substitute


@login_required(login_url='account_login')
def saveSubstitute(request):
    """
    View used to save substitute
    """
    try:
        user_id = request.user.id
        product_id = request.GET.get('product')
        substitute_id = request.GET.get('substitute')
        insert_substitute = Substitute.objects.create(
            substitute=Product.objects.get(id=substitute_id),
            product=Product.objects.get(id=product_id),
            user=get_user_model().objects.get(id=user_id)
        )
        insert_substitute.save()
        return redirect('home')
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
