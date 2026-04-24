# gestion_etudiants/pagination.py
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Pagination standard : 20 résultats par défaut,
    jusqu'à 500 via ?page_size=500
    """
    page_size              = 20
    page_size_query_param  = 'page_size'
    max_page_size          = 500
