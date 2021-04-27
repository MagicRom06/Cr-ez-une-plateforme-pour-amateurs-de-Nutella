from django.views.generic import TemplateView

# Create your views here.


class LegalTemplateView(TemplateView):
    template_name = 'legal_notice/notice.html'
