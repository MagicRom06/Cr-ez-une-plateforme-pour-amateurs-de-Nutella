from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView

from users.forms import CustomUserChangeForm


class AccountPageView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'


class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'users/user_update.html'
    form_class = CustomUserChangeForm

    def get(self, request, **kwargs):
        self.object = get_user_model().objects.get(email=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('account')
