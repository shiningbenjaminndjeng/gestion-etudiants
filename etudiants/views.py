# etudiants/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Etudiant, UniteEnseignement
from .serializers import EtudiantSerializer, UniteEnseignementSerializer


class UniteEnseignementViewSet(viewsets.ModelViewSet):
    queryset         = UniteEnseignement.objects.all()
    serializer_class = UniteEnseignementSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['nom_unite', 'nom_prof']

    class EtudiantViewSet(viewsets.ModelViewSet):
        queryset         = Etudiant.objects.select_related('unite').all()
        serializer_class = EtudiantSerializer
        filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
        search_fields    = ['nom', 'prenom', 'ethnie', 'unite__nom_unite']
        ordering_fields  = ['nom', 'age', 'date_inscription']
    
        # Endpoint bonus : /api/etudiants/{id}/fiche/
        @action(detail=True, methods=['get'])
        def fiche(self, request, pk=None):
            etudiant = self.get_object()
            data = {
                'nom_complet': f"{etudiant.prenom} {etudiant.nom}",
                'age': etudiant.age,
                'naissance': f"{etudiant.date_naissance} à {etudiant.lieu_naissance}",
                'ethnie': etudiant.ethnie,
                'unite': etudiant.unite.nom_unite if etudiant.unite else None,
                'professeur': etudiant.unite.nom_prof if etudiant.unite else None,
            }
            return Response(data)