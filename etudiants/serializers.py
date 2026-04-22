# etudiants/serializers.py
from rest_framework import serializers
from .models import Etudiant, UniteEnseignement


class UniteEnseignementSerializer(serializers.ModelSerializer):
    nb_etudiants  = serializers.SerializerMethodField()
    nb_masculins  = serializers.SerializerMethodField()
    nb_feminins   = serializers.SerializerMethodField()

    class Meta:
        model  = UniteEnseignement
        fields = [
            'id', 'nom_unite', 'nom_prof', 'description',
            'nb_etudiants', 'nb_masculins', 'nb_feminins',
        ]

    def get_nb_etudiants(self, obj):
        return obj.etudiants.count()

    def get_nb_masculins(self, obj):
        return obj.etudiants.filter(genre='M').count()

    def get_nb_feminins(self, obj):
        return obj.etudiants.filter(genre='F').count()


class EtudiantSerializer(serializers.ModelSerializer):
    unite_detail  = UniteEnseignementSerializer(source='unite', read_only=True)
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)

    class Meta:
        model  = Etudiant
        fields = [
            'id', 'nom', 'prenom',
            'date_naissance', 'lieu_naissance', 'age',
            'ethnie', 'genre', 'genre_display',
            'unite', 'unite_detail',
            'date_inscription',
        ]
        read_only_fields = ['date_inscription', 'unite_detail', 'genre_display']
