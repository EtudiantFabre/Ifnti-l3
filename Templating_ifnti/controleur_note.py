from jinja2 import Environment
from os.path import dirname, abspath
from latex import build_pdf


def generate_pdf_note(context):
    """INSTANCIATION D’UN NOUVEL ENVIRONNEMENT
    AVEC DES OPTIONS DE BALISES PERSONNALIS´EES"""

    j2_env = Environment(variable_start_string="\VAR{",
                         variable_end_string="}", block_start_string="\BLOCK{",
                         block_end_string="}", comment_start_string="\COMMENT{",
                         comment_end_string="}")

    """DECLARATION DE FICHIER"""

    # fichier `a lire contenant le template avec les balises
    fichier_in = open("ifnti/note_eleves.tex", 'r')
    # fichier en sortie accueillant les donn´eesfournies
    fichier_out = open("out/template_out_note.tex", 'w')
    template = fichier_in.read()  # lecture du template
    monContext = context
    monContext["image_path"] = dirname(abspath(__file__)) + "out/images/"

    """APPLICATION DE L’ENVIRONNEMENT EDITE SUR LE TEMPLATE"""
    j2_template = j2_env.from_string(template)
    # ´ecriture dans le fichier en sortie
    fichier_out.write(j2_template.render(monContext))
    fichier_out.close()
    mon_pdf = build_pdf(open("out/template_out_note.tex", 'r'))
    mon_pdf.save_to("out/note_eleves.pdf")
    """ FERMETURE DE """
    fichier_in.close()
