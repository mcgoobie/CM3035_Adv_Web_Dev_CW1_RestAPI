from rest_framework.test import APITestCase
from django.urls import reverse
from .serializers import *

import json
from rest_framework import status
from django.test import TestCase, Client
from .models import *


# I wrote this code
client = Client()


# Test cases for the models used in biosciapp
class biosciapp_Models(TestCase):
    def setUp(self):
        self.organism = Organisms(
            taxa_id=1234, clade="E", genus="Test Genus", species="Test Species")
        self.pfam_family = Domain_Pfam(
            domain_id='PFTESTID', domain_desc='test domain desc')
        # These 2 model objects contain FKs
        self.protein = Proteins(
            protein_id="A0A0TESTID", sequence="A12B34C56", length=101, taxonomy=self.organism)
        self.domain = Domains(
            id=1, desc="example desc", start=1, end=10, domain=self.pfam_family, protein=self.protein)

    # Test to check if django model returns the right objs
    def test_Organisms_Model(self):
        self.assertEqual(self.organism.__str__(), "1234")

    def test_DomainsPfam_Model(self):
        self.assertEqual(self.pfam_family.__str__(), "PFTESTID")

    def test_Proteins_Model(self):
        self.assertEqual(self.protein.__str__(), "A0A0TESTID")

    def test_Domains_Model(self):
        self.assertEqual(self.domain.__str__(), "1")


# Test cases for the rest_api and serializers used in biosciapp
class biosciapp_REST_Api(TestCase):
    def setUp(self):
        self.organism = Organisms.objects.create(
            taxa_id=2711, clade="E", genus="Citrus", species="sinensis")
        self.pfam_family = Domain_Pfam.objects.create(
            domain_id='PFTESTID', domain_desc='test domain desc')
        # These 2 model objects contain FKs
        self.protein = Proteins.objects.create(
            protein_id="A0A0TESTID", sequence="A12B34C56", length=101, taxonomy=self.organism)
        self.domain = Domains.objects.create(
            id=1, desc="example desc", start=1, end=10, domain=self.pfam_family, protein=self.protein)
        self.test_protein = {
            "protein_id": "A0A0TestPost",
            "sequence": "Test Sequence",
            "length": 123,
            "taxonomy": {
                "taxa_id": 1234,
                "clade": "E",
                "genus": "Test Genus",
                "species": "Test Species"
            },
        }

    # Test for POST specification of "/api/protein/"
    def test_create_protein(self):
        response = client.post(reverse('add_protein'),
                               data=json.dumps(self.test_protein),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # This test checks for the same POST route, but with an existing pk
    def test_create_protein_existing(self):
        exs_protein_id = "A0A0EXISTING"
        exs_protein = Proteins.objects.create(
            protein_id="A0A0EXISTING", sequence="A12B34C56", length=101, taxonomy=self.organism)
        # Bad protein as protein_id already exists in db
        test_bad_protein = {
            "protein_id": exs_protein_id,
            "sequence": "Test Sequence",
            "length": 123,
            "taxonomy": {
                "taxa_id": 1234,
                "clade": "E",
                "genus": "Test Genus",
                "species": "Test Species"
            },
        }
        response = client.post(reverse('add_protein'),
                               data=json.dumps(test_bad_protein),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test for GET specification of "api/protein/[PROTEIN ID]"
    """
    # Test Case 1: get protein sequence
    def test_get_protein_sequence(self):
        response = client.get(
            reverse('get_protein', kwargs={'protein_id': self.protein.protein_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 2: get non-existing protein sequence
    def test_get_missing_protein_sequence(self):
        response = client.get(
            reverse('get_protein', kwargs={'protein_id': 'randomId'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Test for GET specification of "api/pfam/[PFAM ID]"
    """
    # Test Case 1: get pfam family id and desc
    def test_get_domain_desc(self):
        response = client.get(
            reverse('get_pfam_details', kwargs={'domain_id': self.pfam_family.domain_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 2: get pfam family id and desc of non-existent pfam
    def test_get_missing_domain_desc(self):
        response = client.get(
            reverse('get_pfam_details', kwargs={'domain_id': 'randomId'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    """
    Test for GET specification of "api/proteins/[TAXA ID]"
    """
    # Test Case 1: get all proteins of an organism
    def test_get_organism_proteins(self):
        response = client.get(
            reverse('list_proteins', kwargs={'taxa_id': self.organism.taxa_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 2: get all proteins of a non-existent organism
    def test_get_missing_organism_proteins(self):
        response = client.get(
            reverse('list_proteins', kwargs={'taxa_id': 101}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    """
    Test for GET specification of "api/pfams/[TAXA ID]"
    """
    # Test Case 1: get all domains found in the proteins of an organism
    def test_get_organism_protein_domains(self):
        response = client.get(
            reverse('list_domains', kwargs={'taxa_id': self.organism.taxa_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 2: get all domains found in the proteins of a non-existent organism
    def test_get_missing_organism_protein_domains(self):
        response = client.get(
            reverse('list_domains', kwargs={'taxa_id': 101}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    """
    Test for GET specification of "api/coverage/[PROTEIN ID]"
    """
    # Test Case 1: get domain coverage of specified protein
    def test_get_protein_coverage(self):
        response = client.get(
            reverse('get_coverage', kwargs={'protein_id': self.protein.protein_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 2: get domain coverage of non-existent protein
    def test_get_missing_protein_coverage(self):
        response = client.get(
            reverse('get_coverage', kwargs={'protein_id': 'fakeId'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
# End of code I wrote
