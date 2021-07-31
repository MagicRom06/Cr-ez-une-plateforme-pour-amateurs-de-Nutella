import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .models import SubscribedUsers

# Create your views here.


class HomePageView(TemplateView):
    """
    Home page access
    """
    template_name = 'home_page/home.html'


def newsletterPage(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        name = post_data.get("name", None)
        try:
            subscribedUsers = SubscribedUsers()
            subscribedUsers.email = email
            subscribedUsers.name = name
            subscribedUsers.save()
            subject = 'Souscription NewsLetter'
            message = render_to_string(
                'email/newsletter_sub_email.html',
                {
                    'name': name,
                    'email': email
                }
            )
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email, ]
            email_response = EmailMessage(
                subject,
                message,
                email_from,
                recipient_list)
            email_response.content_subtype = "html"
            email_response.send()
            response = {
                'msg': render_to_string(
                    'messages/newsletter_subscribed.html'
                ),
            }
        except Exception:
            response = {
                'msg': render_to_string(
                    'messages/newsletter_subscribed_fail.html'
                ),
            }
        return HttpResponse(
            json.dumps(response),
            content_type='application/json',
        )
    return render(request, 'home_page/newsletter.html')
