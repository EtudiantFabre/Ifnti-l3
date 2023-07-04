from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms
from Notes.models import Eleve, Note, User


"""class AjouterNote(forms.Form):
    note = forms.FloatField(required=True)
"""


class ADD_NOTE(ModelForm):

    class Meta:
        model = Note
        fields = ['valeur']
        labels = {"valeur": "Note sur 20"}

    def clean(self):
        cleand_data = super().clean()
        # print(cleand_data['valeur'])

        if cleand_data["valeur"] < 0 or cleand_data['valeur'] > 20:

            #self.add_error("valeur", "Votre valeur entré est incorrect !")

            #raise forms.ValidationError('Erreur')
            raise ValidationError(
                'Champs ne recevant que des valeurs positives allant de 0 à 20')
        return cleand_data


class EleveForm(ModelForm):

    class Meta:
        model = Eleve
        fields = '__all__'
        exclude = ("user", )

    def clean(self):
        cleaned_data = super().clean()

        print(cleaned_data)

        niveau = cleaned_data['niveau']
        # print(niveau)
        try:
            matieres = cleaned_data['matieres']
        except:
            matieres = niveau.matieres.all()
        print(matieres)

        for matiere in matieres:
            if matiere not in niveau.matieres.all():
                raise ValidationError(
                    'Cette matière n\'appartient pas au niveau spécifié ! ')

        nom = cleaned_data['nom']
        #print("nom ", nom)
        for lettre in nom:
            if lettre.isdecimal():
                raise ValidationError(
                    'Attention !!! Votre nom ne doit pas contenir de chiffre.')
            else:
                pass


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "password", ]
