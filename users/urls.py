from django.urls import path

from .views import AccountPageView, UserUpdateView

urlpatterns = [
    path('account/', AccountPageView.as_view(), name='account'),
    path('account/<int:pk>/change/',
         UserUpdateView.as_view(),
         name='user_update')
]
