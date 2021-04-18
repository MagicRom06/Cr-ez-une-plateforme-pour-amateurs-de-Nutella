from django.urls import path

from .views import HomePageView, AccountPageView, SearchResultsListView, ProductDetailView, SubstituteDetailView

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('account/', AccountPageView.as_view(), name='account'),
	path('search/', SearchResultsListView.as_view(), name='search_results'),
	path('product/<uuid:pk>', ProductDetailView.as_view(), name='product_detail'),
	path('substitute/<uuid:pk>', SubstituteDetailView.as_view(), name='substitute_detail')
]
