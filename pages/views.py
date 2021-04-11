from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePageView(TemplateView):
	template_name = 'home.html'


class AccountPageView(LoginRequiredMixin, TemplateView):
	template_name = 'account.html'	
