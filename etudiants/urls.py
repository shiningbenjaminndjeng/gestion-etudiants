# etudiants/urls.py
from rest_framework.routers import DefaultRouter
from .views import EtudiantViewSet, UniteEnseignementViewSet

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet)
router.register(r'unites', UniteEnseignementViewSet)

urlpatterns = router.urls