import site
from django.contrib import admin
from Notes.forms import EleveForm
from Notes.models import Eleve, Niveau, Enseignant, Matiere, Note, Personne


# Register your models here.


class EleveAdmin(admin.ModelAdmin):
    form = EleveForm
    search_fields = ['niveau']
    filter_horizontal = ['matieres']


class NiveauAdmin(admin.ModelAdmin):
    pass


class EnseignantAdmin(admin.ModelAdmin):
    pass


class MatiereAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Eleve)
admin.site.register(Eleve)
admin.site.register(Niveau)
admin.site.register(Enseignant)
admin.site.register(Matiere)
admin.site.register(Note)
# admin.site.register(Personne)
