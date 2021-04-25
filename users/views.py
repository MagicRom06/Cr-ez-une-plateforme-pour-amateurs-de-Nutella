from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AccountPageView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'
