from django.views.generic import TemplateView

# Create your views here.


class HomePageView(TemplateView):
    """
    Home page access
    """
    template_name = 'home_page/home.html'
