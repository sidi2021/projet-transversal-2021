from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from comptes.models import Message, Demande, Profile
from django.conf import settings
from django.http import HttpResponse
import os
from django.utils.html import strip_tags
from django.urls import reverse
from django.core import mail
from django.template.loader import render_to_string
import json
from .utils import print_pdf



@login_required(login_url="/")
def control_panel(req):
    msgs = Message.objects.all()
    demandes = Demande.objects.all()
    if req.method == "POST":
        if req.POST.get('msg-response-email') and req.POST.get('msg-area-response'):
            date  = req.POST.get('msg-response-date')
            name  = req.POST.get('msg-response-name')
            email = req.POST.get('msg-response-email')
            msg   = req.POST.get('msg-area-response')
            subject = f"Reponce de l'email reçu le {date}"
            html_message = render_to_string('administration/admin_email_template.html', {'msg': msg, 'title': "Reponce de l'email reçu le " + date})
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = email
            msg_non_repondu = Message.objects.filter(email = email, message = msg).update(repondu = True)
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        if req.POST.get('user-email-input'):
            profile = Profile.objects.get(id = req.POST.get('user-email-input'))
            pdf_path = print_pdf(profile, os.path.join(settings.BASE_DIR, 'static/media/images/default/esp.jpg'))
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), headers={'Content-Type':'application/pdf','Content-Disposition':'attachment;filename=dossier.pdf'})
                return response
        if req.POST.get('notify'):
            subject = f"Message de notification"
            msg = "Veuillez Completer les etapes suivante pour validee votre demande"
            html_message = render_to_string('administration/admin_email_template.html', {'msg': msg, 'title': "Votre dossier a ete bien recu"})
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = req.POST.get('notify-email')
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    context = {'msgs': msgs, 'demandes': demandes}
    return render(req, template_name="administration/control_panel.html", context = context)
