from django.urls import path
from .views import AccountPageView

urlpatterns = [
	path('account/', AccountPageView.as_view(), name='account'),
]
