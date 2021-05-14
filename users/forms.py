from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, forms


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

    class Meta:
        model = get_user_model()
        fields = ('email',)
