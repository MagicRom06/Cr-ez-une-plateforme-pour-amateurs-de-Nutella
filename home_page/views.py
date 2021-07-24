from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse
import re
from .models import SubscribedUsers
from django.core.mail import send_mail
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
        subscribedUsers = SubscribedUsers()
        subscribedUsers.email = email
        subscribedUsers.name = name
        subscribedUsers.save()
        subject = 'Souscription NewsLetter'
        message = 'Bonjour ' + name + ', Merci pour votre inscription, vous serez notifié des dernières actualités de notre site. Merci de ne pas répondre à ce mail'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        response = {
            'msg': render_to_string(
                'messages/newsletter_subscribed.html'
            ),
        }
        return HttpResponse(
            json.dumps(response),
            content_type='application/json',
        )
    return render(request, 'home_page/newsLetter.html')
