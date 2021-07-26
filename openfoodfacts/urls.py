from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (ProductDetailView, SearchResultsListView,
                    SubstituteDetailView, UserSubstitutesListView,
                    saveSubstitute)

urlpatterns = [
    path(
           'search/', cache_page(60 * 15)(SearchResultsListView.as_view()),
           name='search_results'
    ),
    path(
           'product/<uuid:pk>',
           ProductDetailView.as_view(),
           name='product_detail'
    ),
    path(
           'substitute/<uuid:pk>',
           SubstituteDetailView.as_view(),
           name='substitute_detail'
    ),
    path(
           'save/',
           saveSubstitute,
           name='save_substitute'
    ),
    path(
           'user/substitutes/',
           UserSubstitutesListView.as_view(),
           name='user_substitutes'
    )
]
