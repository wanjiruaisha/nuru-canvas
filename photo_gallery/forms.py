from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


INPUT_CLASSES = (
    'w-full rounded-lg border border-slate-300 px-4 py-3 '
    'focus:border-amber-500 focus:outline-none'
)


class RegistrationForm(UserCreationForm):
    """Register a user with a username, email and password."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Email address',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Username',
        })

        self.fields['password1'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'placeholder': 'Confirm password',
        })

    def clean_email(self):
        """Prevent different accounts from using the same email."""

        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    """Style Django's built-in login form."""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Password',
            }
        )
    )