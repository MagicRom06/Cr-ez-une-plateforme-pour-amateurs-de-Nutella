from django.urls import path

from .views import LegalTemplateView

urlpatterns = [
    path('', LegalTemplateView.as_view(), name="legal")
]
