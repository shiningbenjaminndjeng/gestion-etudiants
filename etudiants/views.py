# etudiants/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q

from .models import Etudiant, UniteEnseignement
from .serializers import EtudiantSerializer, UniteEnseignementSerializer


class UniteEnseignementViewSet(viewsets.ModelViewSet):
    queryset         = UniteEnseignement.objects.all()
    serializer_class = UniteEnseignementSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['nom_unite', 'nom_prof']

    @action(detail=True, methods=['get'], url_path='etudiants')
    def liste_etudiants(self, request, pk=None):
        """
        GET /api/unites/{id}/etudiants/
        Retourne la liste des étudiants inscrits à cette unité,
        avec leurs informations complètes.
        """
        unite     = self.get_object()
        etudiants = unite.etudiants.select_related('unite').order_by('nom', 'prenom')
        serializer = EtudiantSerializer(etudiants, many=True)
        return Response({
            'unite'      : UniteEnseignementSerializer(unite).data,
            'etudiants'  : serializer.data,
            'total'      : etudiants.count(),
            'masculins'  : etudiants.filter(genre='M').count(),
            'feminins'   : etudiants.filter(genre='F').count(),
        })

    @action(detail=False, methods=['get'], url_path='statistiques-genre')
    def statistiques_genre(self, request):
        """
        GET /api/unites/statistiques-genre/
        Retourne, pour chaque unité, le nombre de garçons et de filles.
        Utilisé pour générer le graphique par genre.
        """
        unites = UniteEnseignement.objects.annotate(
            total     = Count('etudiants'),
            masculins = Count('etudiants', filter=Q(etudiants__genre='M')),
            feminins  = Count('etudiants', filter=Q(etudiants__genre='F')),
        ).order_by('nom_unite')

        data = [
            {
                'id'        : u.id,
                'nom_unite' : u.nom_unite,
                'nom_prof'  : u.nom_prof,
                'total'     : u.total,
                'masculins' : u.masculins,
                'feminins'  : u.feminins,
            }
            for u in unites
        ]
        return Response(data)


class EtudiantViewSet(viewsets.ModelViewSet):
    queryset         = Etudiant.objects.select_related('unite').all()
    serializer_class = EtudiantSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['nom', 'prenom', 'ethnie', 'unite__nom_unite']
    ordering_fields  = ['nom', 'age', 'date_inscription', 'genre']

    def perform_create(self, serializer):
        """Après chaque enregistrement, les stats sont disponibles via /api/unites/{id}/etudiants/"""
        serializer.save()

    @action(detail=True, methods=['get'])
    def fiche(self, request, pk=None):
        etudiant = self.get_object()
        data = {
            'nom_complet' : f"{etudiant.prenom} {etudiant.nom}",
            'age'         : etudiant.age,
            'naissance'   : f"{etudiant.date_naissance} à {etudiant.lieu_naissance}",
            'ethnie'      : etudiant.ethnie,
            'genre'       : etudiant.get_genre_display(),
            'unite'       : etudiant.unite.nom_unite if etudiant.unite else None,
            'professeur'  : etudiant.unite.nom_prof  if etudiant.unite else None,
        }
        return Response(data)
