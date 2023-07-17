from django.urls import path
from .views import *
from . import api

# I wrote this code

urlpatterns = [
    path('api/protein/', api.add_protein, name='add_protein'),
    path('api/protein/<str:protein_id>', api.protein_detail, name='get_protein'),
    path('api/pfam/<str:domain_id>', api.pfam_detail, name='get_pfam_details'),
    path('api/proteins/<str:taxa_id>', api.list_proteins, name='list_proteins'),
    path('api/pfams/<str:taxa_id>', api.list_domains, name='list_domains'),
    path('api/coverage/<str:protein_id>', api.protein_coverage, name='get_coverage')
]

# End of code i wrote
