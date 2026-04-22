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
        """GET /api/unites/{id}/etudiants/"""
        unite     = self.get_object()
        etudiants = unite.etudiants.prefetch_related('unites').order_by('nom', 'prenom')
        serializer = EtudiantSerializer(etudiants, many=True)
        return Response({
            'unite'    : UniteEnseignementSerializer(unite).data,
            'etudiants': serializer.data,
            'total'    : etudiants.count(),
            'masculins': etudiants.filter(genre='M').count(),
            'feminins' : etudiants.filter(genre='F').count(),
        })

    @action(detail=False, methods=['get'], url_path='statistiques-genre')
    def statistiques_genre(self, request):
        """GET /api/unites/statistiques-genre/"""
        unites = UniteEnseignement.objects.annotate(
            total     = Count('etudiants'),
            masculins = Count('etudiants', filter=Q(etudiants__genre='M')),
            feminins  = Count('etudiants', filter=Q(etudiants__genre='F')),
        ).order_by('nom_unite')
        return Response([
            {
                'id'       : u.id,
                'nom_unite': u.nom_unite,
                'nom_prof' : u.nom_prof,
                'total'    : u.total,
                'masculins': u.masculins,
                'feminins' : u.feminins,
            }
            for u in unites
        ])


class EtudiantViewSet(viewsets.ModelViewSet):
    queryset         = Etudiant.objects.prefetch_related('unites').all()
    serializer_class = EtudiantSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['matricule', 'nom', 'prenom', 'ethnie', 'unites__nom_unite']
    ordering_fields  = ['matricule', 'nom', 'age', 'date_inscription', 'genre']

    @action(detail=True, methods=['get'])
    def fiche(self, request, pk=None):
        etudiant = self.get_object()
        return Response({
            'matricule'  : etudiant.matricule,
            'nom_complet': f"{etudiant.prenom} {etudiant.nom}",
            'age'        : etudiant.age,
            'naissance'  : f"{etudiant.date_naissance} à {etudiant.lieu_naissance}",
            'ethnie'     : etudiant.ethnie,
            'genre'      : etudiant.get_genre_display(),
            'unites'     : [u.nom_unite for u in etudiant.unites.all()],
        })
