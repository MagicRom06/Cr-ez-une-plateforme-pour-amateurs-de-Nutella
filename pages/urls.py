from django.urls import path

from .views import HomePageView, AccountPageView

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('account', AccountPageView.as_view(), name='account'),
]
