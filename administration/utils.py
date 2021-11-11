from fpdf import FPDF
import numpy as np, os
from PIL import Image, ImageDraw
from django.conf import settings


def make_round_image(path):
    img=Image.open(path)
    height,width = img.size
    lum_img = Image.new('L', [height,width] , 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (height,width)], 0, 360, fill = 255, outline = "white")
    img_arr =np.array(img)
    lum_img_arr =np.array(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    return Image.fromarray(final_img_arr)



pdf = FPDF()
pdf.add_page()

def add_data(h, d, d1, d2):
    pdf.set_xy(60,h)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(w=210.0, h=40.0, align='L', txt=d1)

    pdf.set_xy(d,h)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(w=210.0, h=40.0, align='L', txt=d2, border=0)



def print_pdf(profile, logo):
    keys = ["Date de naissance:", "Pays de naissance:", "Lieu de naissance:", "Departement:", "Formation:", "Numero Etudient:", "Numero de telephone:", "Annee universitaire:", "Nom du personne a contacter:", "Pays de residence:", "Inscit le:"]
    values = [profile.date_de_naissance ,profile.pays_de_naissacne ,profile.lieu_de_naissacne ,profile.departement ,profile.formation ,profile.numero_etudiant ,profile.numero_de_telephone  ,profile.anne_universitaire ,profile.nom_du_personne_a_contacter ,profile.numero_du_telephone_personne_a_contacter ,profile.pays_de_residence ,profile.cree_le]
    pdf.set_xy(90,5)
    pdf.image(logo,  link='', type='', w=30, h=25)

    pdf.set_xy(0.0,40)
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(54, 153, 232)
    pdf.cell(w=210.0, h=40.0, align='C', txt=profile.nom + ' ' + profile.prenom, border=0)

    pdf.set_xy(90,70)
    pdf.image(os.path.join(settings.BASE_DIR, 'static/' + profile.image.url),  link='', type='', w=32, h=32)

    pdf.set_xy(0.0,90)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=210.0, h=40.0, align='C', txt=profile.user.email, border=0)

    j = 0
    for i in range(len(keys)):
        add_data(120 + j, 113, str(keys[i]), str(values[i]))
        j += 10
    pdf_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'temp', 'pdf.pdf')
    pdf.output(pdf_path ,'F')
    return pdf_path
