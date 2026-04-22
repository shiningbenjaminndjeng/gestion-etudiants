# etudiants/admin.py
from django.contrib import admin
from .models import Etudiant, UniteEnseignement

@admin.register(UniteEnseignement)
class UniteAdmin(admin.ModelAdmin):
    list_display  = ['nom_unite', 'nom_prof']
    search_fields = ['nom_unite', 'nom_prof']

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display   = ['matricule', 'nom', 'prenom', 'age', 'genre', 'date_inscription']
    list_filter    = ['genre', 'ethnie', 'unites']
    search_fields  = ['matricule', 'nom', 'prenom']
    filter_horizontal = ['unites']
