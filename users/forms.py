from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, forms
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """
    Personalize user creation form
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    """
    Personalize user creation form
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = kwargs.pop(
                'password_url', """Le mot de passe peut être changé
                 <a href="/users/password/change/">ici</a>"""
            )

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)
        help_texts = {
            'password': _('Some useful help text.'),
        }
