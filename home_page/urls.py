from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .views import HomePageView

urlpatterns = [
    path('', cache_page(60 * 15)(HomePageView.as_view()), name='home'),
    path('newsletter/', views.newsletterPage, name='newsletter')
]
