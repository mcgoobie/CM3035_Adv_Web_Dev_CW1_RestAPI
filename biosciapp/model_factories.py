import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *


class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = 4155
    clade = 'E'
    genus = 'Erythranthe'
    species = 'guttata'

    class Meta:
        model = Organisms


class DomainsPfamFactory(factory.django.DjangoModelFactory):
    domain_id = 'PFTEST'
    domain_desc = 'Test Desc'

    class Meta:
        model = Domain_Pfam


class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = 'A0A0TEST'
    sequence = 'Test Desc'
    length = 338
    taxa = factory.SubFactory(OrganismFactory)

    class Meta:
        model = Proteins


class DomainsFactory(factory.django.DjangoModelFactory):
    desc = 'Test Desc'
    start = 1
    end = 10
    domain = factory.SubFactory(DomainsPfamFactory)
    protein = factory.SubFactory(ProteinFactory)