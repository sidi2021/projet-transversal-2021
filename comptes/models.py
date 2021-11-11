from django.db import models
from django.contrib.auth.models import User
import uuid, datetime, json, string, random
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.db.models.signals import post_save



def get_choice(key):
    choice = []
    with open("comptes/info.json", "r", encoding="utf8") as stream:
        try:
            for i in json.load(stream).get(key):
                choice.append((i.lower().capitalize(), i.lower().capitalize()))
        except json.JSONDecodeError as exp:
            print(exp)
    return tuple(choice)


departements = get_choice("departements")

formations = get_choice("formations")

pays = get_choice("pays")

annees = ((str(y) + "-" + str(y+1), str(y) + "-" + str(y+1)) for y in range(1970, datetime.date.today().year))

phone_regex = RegexValidator(regex=r"^\+?1?\d{9,15}$",message="Le numéro de téléphone doit être saisi au format : ' 000000000'. Jusqu'à 15 chiffres autorisés.",)


def custom_image(instance, filename):
    name, extension = filename.split(".")
    new_name = "%s.%s" % (str(instance.id), extension)
    dates = datetime.date.today().strftime("images/users/%Y/%m/%d/")
    return dates +  new_name

def custom_doc(instance, filename):
    name, extension = filename.split(".")
    new_name = "%s.%s" % (str(instance.id), extension)
    dates = datetime.date.today().strftime("documents/%Y/%m/%d/")
    return dates +  new_name

def generate_id():
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_lowercase  + string.digits) for _ in range(64))

class Profile(models.Model):
    id = models.CharField(primary_key=True, default = generate_id(), editable=False, max_length = 64)
    user = models.OneToOneField(unique=True, to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=custom_image, default="images/default/user.jpg" , blank = False)
    nom = models.CharField(max_length=255, blank=False)
    prenom = models.CharField(max_length=255, blank=False)
    date_de_naissance = models.DateField(null=True, blank=False)
    pays_de_naissacne = models.CharField(max_length=255, choices=pays, blank=False)
    lieu_de_naissacne = models.CharField(max_length=255, blank=False)
    departement = models.CharField(max_length=255, choices=departements, blank=False)
    formation = models.CharField(max_length=255, choices=formations, blank=False)
    numero_etudiant = models.CharField(max_length=255, blank=False)
    numero_de_telephone = models.CharField(
        validators=[phone_regex], max_length=17, blank=False
    )
    anne_universitaire = models.CharField(max_length=255, choices=annees, blank=False)
    nom_du_personne_a_contacter = models.CharField(max_length=255, blank=False)
    numero_du_telephone_personne_a_contacter = models.CharField(
        validators=[phone_regex], max_length=17, blank=False
    )
    pays_de_residence = models.CharField(max_length=255, choices=pays, blank=False)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifier_le = models.DateTimeField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)
    etapes_validees = models.BooleanField(default=False)

    class Meta:
        ordering = ['-cree_le',]

    def __str__(self):
        return "%s" % self.user.username

    def get_absolute_url(self):
        return reverse("comptes:profile", args=(self.id,))


def auto_profile(sender, **kwargs):
    if kwargs["created"]:
        user_profile = Profile.objects.create(user=kwargs["instance"])


post_save.connect(auto_profile, sender=User)



demende_types = [
    ("Demende de diplome","Demende de diplome"),
    ("Demende d'attestation de passage", "Demende d'attestation de passage"),
    ("Demende de Certificat de reussite", "Demende de Certificat de reussite"),
    ("Demende de diplicata de releve de note", "Demende de diplicata de releve de note"),
    ("Demende de carte d'etudiant", "Demende de carte d'etudiant"),
    ("Demende de certificat d'inscription", "Demende de certificat d'inscription"),
]

class Demande(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices = demende_types, blank=True)
    Scan_cerificat_de_inscription = models.ImageField(upload_to=custom_doc, blank=True)
    Scan_cerificat_de_reussite = models.ImageField(upload_to=custom_doc, blank=True)
    lieu_de_retret = models.CharField(max_length=255, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifier_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-cree_le',]

    def __str__(self):
        return "%s: %s" % (self.user.username, self.type)

    # def get_absolute_url(self):
    #     return reverse("comptes:profile", args=(self.id,))



class Message(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    message = models.TextField(default='', blank=False)
    date = models.DateTimeField(auto_now_add=True)
    repondu = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return "%s" % (self.message[:20] + '...',)

    # def get_absolute_url(self):
    #     return reverse("comptes:profile", args=(self.id,))
