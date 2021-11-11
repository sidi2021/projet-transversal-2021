from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.utils.html import strip_tags
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import ProfileForm, LoginForm, RegistrationForm, MessageForm, DemandeForm
from .models import Profile, Message, Demande
import datetime
import random


def view_404(req, exption):
    return render(req, template_name="errors/404.html")


def view_500(req):
    return render(req, template_name="errors/500.html")




def index(req):
    if req.method == "POST":
        message_form = MessageForm(req.POST)
        login_form = LoginForm(req.POST)
        register_form = RegistrationForm(req.POST)
        if message_form.is_valid():
            Message.objects.create(
                name =  message_form.cleaned_data["name"],
                email = message_form.cleaned_data["email"],
                message =  message_form.cleaned_data["message"]
            )

        if login_form.is_valid():
            try:
                email = login_form.cleaned_data["login_email"]
                password = login_form.cleaned_data["login_password"]
                user_object = User.objects.get(email=email) or None
                user = authenticate(req, username=user_object.username, password=password)
                if user is not None:
                    if user.is_active:
                        login(req, user)
                        remember_me = req.POST.get("login_remember_me")
                        if not remember_me:
                            req.session.set_expiry(0)
                            req.session.modified = True
                        if user.is_superuser:
                            messages.success(
                                req, f"Bienvenue Adminstrateur !"
                            )
                            return redirect(
                                reverse("administration:control_panel")
                            )
                        elif not user.is_superuser and user.profile.email_confirmed:
                            messages.success(
                                req, f"Bienvenue {req.user.username} !"
                            )
                            return redirect(
                                reverse("comptes:profile", kwargs={"id": req.user.profile.id})
                            )
            except User.DoesNotExist:
                messages.error(
                    req, f"Cet email ou mot de pass ne correspond pas a un utilisteur"
                )



        else:
            ...

        if register_form.is_valid():
            email     = register_form.cleaned_data["register_email"]
            username  = email.strip().split('@')[0]
            password1 = register_form.cleaned_data["register_password1"]
            password2 = register_form.cleaned_data["register_password2"]

            if password1 == password2:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    is_active=False,
                )
                user.save()
                remember_me = req.POST.get("register_remember_me")
                if not remember_me:
                    req.session.set_expiry(0)
                    req.session.modified = True
                current_site = get_current_site(req)
                subject = "Activez votre compte de ESP Team"
                message = render_to_string(
                    "comptes/email_verification_template.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                user.email_user(subject, "", html_message=message)
                messages.info(
                    req,
                    "Veuillez confirmer votre e-mail pour terminer l'inscription."
                )
                return redirect(reverse("comptes:verification_message"))
            else:
                messages.error(
                    req, f"Un probleme exist Veriver que les deux mots de passe correspondent !"
                )
    else:
        message_form = MessageForm()
        login_form = LoginForm()
        register_form = RegistrationForm()
    if req.user.is_authenticated:
        if req.user.is_superuser:
            return redirect(
                reverse("administration:control_panel")
            )
        else:
            return redirect(
                reverse("comptes:profile", kwargs={"id": req.user.profile.id})
            )
    return render(
        req,
        template_name="base.html",
        context={
            "login_form": login_form,
            "register_form": register_form,
            "message_form": message_form,
        },
    )


@login_required(login_url="/")
def changer_profile(req, id):
    profile = get_object_or_404(Profile, id=id)
    if req.method == "POST":
        form = ProfileForm(req.POST, req.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = profile.user
            instance.save()
    else:
        form = ProfileForm(instance=profile)
    return render(
        req, "comptes/changer_profile.html", {"form": form, "profile": profile}
    )


@login_required(login_url="/")
def profile(req, id):
    profile = get_object_or_404(Profile, id=id)
    demandes = Demande.objects.filter(user = profile.user)
    if req.method == 'POST':
        demande_form = DemandeForm(req.POST, req.FILES)
        if demande_form.is_valid():
            instance = demande_form.save(commit = False)
            instance.user = profile.user
            demande_form.save()
        else:
            messages.error(req, ("Verifier que touts les champs sont remplis"))
    else:
        demande_form = DemandeForm()
    return render(req, "comptes/profile.html", {"profile": profile, 'is_profile': True ,'demandes': demandes, 'demande_form': demande_form})

@login_required(login_url="/")
def remove_user(req):
    user = get_object_or_404(User, username=req.user.username, email=req.user.email)
    user.delete()
    return redirect(reverse('comptes:index'))


def verification_message(req):
    if req.user.is_active and req.user.profile.email_confirmed:
        return redirect(
            reverse("comptes:changer_profile", kwargs={"id": req.user.profile.id})
        )
    else:
        messages.info(
            req, ("Veuillez confirmer votre e-mail pour terminer l'inscription.")
        )
    return render(req, template_name="comptes/verification_message.html")


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active=True
            Profile.objects.filter(user=user).update(email_confirmed=True)
            user.save()
            login(request, user)
            messages.success(request, ("Votre compte a été confirmé."))
            return redirect(
                reverse("comptes:changer_profile", kwargs={"id": user.profile.id})
            )
        else:
            messages.warning(
                request,
                (
                    "Le lien de confirmation n'était pas valide, peut-être parce qu'il a déjà été utilisé."
                )
            )
            return redirect(reverse("comptes:index"))


def test(req):
    context = {'data': req.user.id}
    return render(req, template_name="test.html", context = context)
