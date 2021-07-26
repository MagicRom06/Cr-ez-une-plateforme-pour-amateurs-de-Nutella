from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HomePageView

urlpatterns = [
    path('', cache_page(60 * 15)(HomePageView.as_view()), name='home'),
]
