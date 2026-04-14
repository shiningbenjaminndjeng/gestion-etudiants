# etudiants/serializers.py
from rest_framework import serializers
from .models import Etudiant, UniteEnseignement


class UniteEnseignementSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UniteEnseignement
        fields = '__all__'


class EtudiantSerializer(serializers.ModelSerializer):
    # Affiche le nom de l'unité + prof au lieu du simple ID
    unite_detail = UniteEnseignementSerializer(
        source='unite', read_only=True
    )

    class Meta:
        model  = Etudiant
        fields = [
            'id', 'nom', 'prenom',
            'date_naissance', 'lieu_naissance', 'age',
            'ethnie', 'unite', 'unite_detail',
            'date_inscription'
        ]
        read_only_fields = ['date_inscription', 'unite_detail']