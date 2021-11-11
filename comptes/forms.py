from django import forms
from .models import Profile, Message, Demande
import datetime


class DateInput(forms.DateInput):
    input_type = "date"


class ProfileForm(forms.ModelForm):
    class Meta:

        model = Profile
        fields = "__all__"
        exclude = ('user', 'email_confirmed')
        widgets = {
            "date_de_naissance": DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'type': 'date',
                    "min": "1960-01-01",
                    "max": str(datetime.date.today()),
                }
            ),
        }


class DemandeForm(forms.ModelForm):
    class Meta:

        model = Demande
        fields = "__all__"
        exclude = ('user', )
        widgets = {
            "date_de_retret": DateInput(
                format=('%Y-%m-%Y'),
                attrs={
                    'type': 'date',
                    "min": "1960-01-01",
                    "max": str(datetime.date.today()),
                }
            ),

        }


class MessageForm(forms.ModelForm):
    class Meta:

        model = Message
        fields = ["name", "email", "message"]


class LoginForm(forms.Form):
    login_email = forms.EmailField()
    login_password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    register_email = forms.EmailField()
    register_password1 = forms.CharField(max_length=255, widget=forms.PasswordInput)
    register_password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)
