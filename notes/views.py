from cgitb import text
from re import M
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from Notes.models import Eleve, Matiere, Niveau, Note
from Notes.forms import ADD_NOTE, EleveForm, UserForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from Notes import views

from Templating_ifnti.controleur import generate_pdf
from Templating_ifnti.controleur_note import generate_pdf_note
from django.urls import reverse


@login_required
def index(request):
    output = _('Welcome to Fabrice site.')
    return render(request, "notes/index.html", {'eleves': Eleve.objects.all(), 'niveaux': Niveau.objects.all(), 'matieres':  Matiere.objects.all()})


def index1(request):
    return render(request, "notes/index1.html")


def CreateStudent(request):
    eleveForm = EleveForm()
    userForm = UserForm()
    return render(request, "notes/createStudent.html", {'form': eleveForm, 'userForm': userForm})


def SaveStudent(request):

    if request.method == 'POST':
        eleveForm = EleveForm(request.POST)
        userForm = UserForm(request.POST)
        if eleveForm.is_valid():
            eleveForm.save()
        if userForm.is_valid():
            userForm.save()
        #messages.success(request, 'Acount create succesful')
        return reverse(views.eleves)
    else:
        eleveForm = EleveForm()
        return render(request, "notes/createStudent.html", {'form': eleveForm})


def listeEleves(request):
    listeEleves = []
    for eleve in Eleve.objects.all():
        el = {'matricule': eleve.id_eleve, 'nom': eleve.nom, 'prenom': eleve.prenom,
              'sexe': eleve.sexe, 'dateNais': eleve.date_naissance}
        listeEleves.append(el)
    context = {'eleves': listeEleves}
    generate_pdf(context)

    with open("out/liste_eleves.pdf", 'rb') as pdf:
        # Chargez le contenu du fichier PDF dans une variable
        response = HttpResponse(pdf.read(), content_type='application/pdf')

        response['Content-Disposition'] = 'filename=%s' % "out/liste_eleves.pdf"
        # Retournez la réponse

        return response


def liste_niveauElv(request, id):
    listeEleves = []
    for eleve in Eleve.objects.all():
        #print("vOICI LE NIVEAU")
        # print(eleve.niveau.id)
        if eleve.niveau.id == id:
            el = {'matricule': eleve.id_eleve, 'nom': eleve.nom, 'prenom': eleve.prenom,
                'sexe': eleve.sexe, 'dateNais': eleve.date_naissance}
            listeEleves.append(el)
    context = {'eleves': listeEleves}
    generate_pdf(context)

    with open("out/liste_eleves.pdf", 'rb') as pdf:
        # Chargez le contenu du fichier PDF dans une variable
        response = HttpResponse(pdf.read(), content_type='application/pdf')

        response['Content-Disposition'] = 'filename=%s' % "out/liste_eleves.pdf"
        # Retournez la réponse

        return response

# Create your views here.


def noteEleves(request, mat_id):
    eleve_mat_note = []
    #listeEleves = Eleve.objects.all()
    listeNotes = Note.objects.all()
    mat = get_object_or_404(Matiere, pk=mat_id)

    #print("voici la matiere : " + str(mat.id))
    for note in listeNotes:
        #print("Équivalence : " + str(note.matiere.id))
        #print("Équivalence : " + str(str(note.matiere.id) == str(mat.id)))
        if str(note.matiere.id) == str(mat.id):
            el = {'matricule': note.eleve.id_eleve, 'nom': note.eleve.nom, 'prenom': note.eleve.prenom,
                  'sexe': note.eleve.sexe, 'dateNais': note.eleve.date_naissance,
                  'mat': note.matiere.nomDeMat, 'note': note.valeur,
                  'valide': str(note.valeur > 12)}

            eleve_mat_note.append(el)

    context = {'eleves': eleve_mat_note, 'matiere': mat.nomDeMat}
    #print("le contexte")
    # print(context)
    generate_pdf_note(context)

    with open("out/note_eleves.pdf", 'rb') as pdf:
        # Chargez le contenu du fichier PDF dans une variable
        response = HttpResponse(pdf.read(), content_type='application/pdf')

        response['Content-Disposition'] = 'filename=%s' % "out/note_eleves.pdf"
        # Retournez la réponse

        return response
        #print("Table : " + eleve_mat_note.__str__())
        # return render(request, "notes/noteEleves.html", {"notes": eleve_mat_note})


def Niveaux(request):
    niveaux = Niveau.objects.all()
    return render(request, "notes/niveaux.html", {'niveaux': niveaux})


def test(request):
    return render(request, "test")


@login_required
@permission_required('Notes.add_matiere')
def matiere(request, id):
    matiere = get_object_or_404(Matiere, pk=id)
    return render(request, "notes/uneMatiere.html",  {"mat": matiere})


@login_required
@permission_required('Notes.view_matiere')
def matieres(request):
    matieres = Matiere.objects.all()
    return render(request, "notes/listeMatiere.html", {"matieres": matieres})


@login_required
@permission_required('Notes.view_eleve')
def eleves(request):
    #texte = "<h1>Voici la liste des élèves disponible dans la base de donné :</h1><br>"
    listeEleves = Eleve.objects.all()
    # for elt in listeEleves:
    #    text
    return render(request, "notes/listeEleves.html", {"le": listeEleves})


@login_required
@permission_required('Notes.view_eleve')
def eleve(request, id):
    eleve = get_object_or_404(Eleve, pk=id)
    return render(request, "notes/unEleve.html",  {"el": eleve})


@login_required
@permission_required('Notes.view_niveau')
def niveau(request, id):
    niveau = get_object_or_404(Niveau, pk=id)
    return render(request, "notes/unNiveau.html",  {"niv": niveau})

# type: ignore


@login_required
@permission_required('Notes.add_note')
def add_note(request, id_eleve, id_matiere):
    eleve = get_object_or_404(Eleve, pk=id_eleve)
    mat = get_object_or_404(Matiere, pk=id_matiere)
    if request.method == 'POST':
        form = ADD_NOTE(request.POST)

        if form.is_valid():
            valeur = form.cleaned_data['valeur']
            print(valeur)

            note = Note(valeur=valeur,
                        eleve_id=eleve.id_eleve, matiere_id=mat.id)  # type: ignore
            note.save()
        # print(request.POST)
        else:
            # pass
            return HttpResponse("Echèque 👎️👎️👎️ !!!")

        return HttpResponse("Note créé avec succès !!!")
    else:
        form = ADD_NOTE()
        # print(eleve.matieres.all())
        if mat in eleve.matieres.all():
            # return HttpResponse("Note d'un élève dans une matière")
            return render(request, "notes/add_note.html",  {"el": eleve, "mat": mat, "formulaire": form})
        # else:
        return HttpResponse("L'élève spécifié ne suis la matière !!!")
