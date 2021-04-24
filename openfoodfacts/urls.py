from django.urls import path
from .views import SearchResultsListView, ProductDetailView, SubstituteDetailView

urlpatterns = [
	path('search/', SearchResultsListView.as_view(), name='search_results'),
	path('product/<uuid:pk>', ProductDetailView.as_view(), name='product_detail'),
	path('substitute/<uuid:pk>', SubstituteDetailView.as_view(), name='substitute_detail')
]
