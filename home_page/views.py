from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse
import re
from .models import SubscribedUsers
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import json
from django.http import HttpResponse
from django.template import RequestContext

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
            message = render_to_string('email/newsletter_sub_email.html')
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email, ]
            email_response = EmailMessage(subject, message, email_from, recipient_list)
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
    return render(request, 'home_page/newsLetter.html')
