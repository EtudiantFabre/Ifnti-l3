from datetime import datetime
from django.db import models

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User

# Create your models here.


class Personne(models.Model):
    TYPE_SEXE = [
        ('M', 'Masculin'),
        ('F', 'Féminin')
    ]
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1, choices=TYPE_SEXE)
    date_naissance = models.DateField(auto_now=False, auto_now_add=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # , null=True

    class Meta:
        abstract = True

    def __str__(self):
        return "Nom : " + self.nom + ", Prénom : " + self.prenom + ", sexe : " + self.sexe + ", Date de naissance : " + str(self.date_naissance)


class Niveau(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    matieres = models.ManyToManyField('Matiere')

    def __str__(self):
        return "Nom du niveau : " + self.nom

    class Meta:
        verbose_name_plural = "Niveaux"


class Enseignant(Personne):
    pass


class Matiere(models.Model):
    nomDeMat = models.CharField(max_length=50)
    enseignant = models.ForeignKey('Enseignant', on_delete=models.CASCADE)
    niveaux = models.ManyToManyField('Niveau')

    def __str__(self):
        return "Matière : " + self.nomDeMat + ",\n Enseignant : {" + str(self.enseignant) + "}, \n Niveau(x) : " + str(self.niveaux) + ";"


class Eleve(Personne):
    id_eleve = models.IntegerField(primary_key=True)
    niveau = models.ForeignKey('Niveau', on_delete=models.CASCADE)
    matieres = models.ManyToManyField(
        'Matiere', verbose_name="Matières appartenant au niveau sélectionné ", blank=True)

    def __str__(self):
        """ id :  + str(self.id_eleve) +"""
        return "Nom : " + self.nom + ", Prénom : " + self.prenom  # + ", sexe : " + self.sexe + ", date de naissance : " + str(self.date_naissance)

    def save(self, *args, **kwargs):
        if not self.matieres.all():
            for mat_niv in self.niveau.matiere_set.all():
                self.matieres.add(mat_niv)
            '''    print("****** Voici les matières du niveau :", mat_niv)
            
            self.matieres = mat_niv
            print("****** Voici les matières du niveau :", mat_niv)
            '''

        super().save(*args, **kwargs)


class Note(models.Model):
    valeur = models.FloatField(null=True, validators=[
                               MinValueValidator(0.0), MaxValueValidator(20.0)])
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE)
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)

    def __str__(self):
        return "Valeur : " + str(self.valeur) + "\n Elève : " + str(self.eleve) + "\n  Matière(s) : " + str(self.matiere)
