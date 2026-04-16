# etudiants/models.py
from django.db import models


class UniteEnseignement(models.Model):
    nom_unite   = models.CharField(max_length=200)
    nom_prof    = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Unité d'enseignement"
        ordering = ['nom_unite']

    def __str__(self):
        return f"{self.nom_unite} — Prof : {self.nom_prof}"


class Etudiant(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Identité
    nom            = models.CharField(max_length=100)
    prenom         = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=150)
    age            = models.PositiveIntegerField()
    ethnie         = models.CharField(max_length=100, blank=True)
    genre          = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        default='M',
        verbose_name='Genre'
    )

    # Rattachement pédagogique
    unite = models.ForeignKey(
        UniteEnseignement,
        on_delete=models.SET_NULL,
        null=True,
        related_name='etudiants'
    )

    # Métadonnée
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Étudiant"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom}"
