from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('accueil', views.index1, name='index1'),
    path('eleves_pdf', views.listeEleves, name='eleves_pdf'),
    path('niveaux', views.Niveaux, name='niveaux'),
    path('niveau_pdf/<int:id>/', views.liste_niveauElv, name='niveau_pdf'),
    path('noteEleves/<int:mat_id>/', views.noteEleves, name='noteEleves'),
    path('create_student/', views.CreateStudent, name='create_student'),
    path('save_student/', views.SaveStudent, name='save_student'),

    path('eleves/', views.eleves, name='eleves'),
    path('eleve/<int:id>/', views.eleve, name='eleve'),
    path('matieres/', views.matieres, name='matieres'),
    path('matiere/<int:id>/', views.matiere, name='matiere'),
    path('niveau/<int:id>/', views.niveau, name='niveau'),
    path('add_note/<int:id_eleve>/<int:id_matiere>/',
         views.add_note, name='add_note'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)