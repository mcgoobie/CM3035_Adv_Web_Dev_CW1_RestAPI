from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import *
from .serializers import *

# I wrote this code

# POST - add a new record
@api_view(['POST'])
def add_protein(request):
    if request.method == 'POST':
        serializer = Create_New_ProteinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET - Return the protein sequence and all we know about it
@api_view(['GET'])
def protein_detail(request, protein_id):
    try:
        # Fetch matching protein of the kwarg protein_id entered.
        protein = Proteins.objects.get(protein_id=protein_id)
    except Proteins.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProteinSerializer(protein)
        return Response(serializer.data)

# GET - Return the domain and it's descriptions
@api_view(['GET'])
def pfam_detail(request, domain_id):
    try:
        # Fetch matching domain descriptions based on domain id passed
        domain_pfam = Domain_Pfam.objects.get(domain_id=domain_id)
        # print(domain_pfam)
    except Domain_Pfam.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DomainPfamSerializer(domain_pfam)
        return Response(serializer.data)

# Return list of all proteins for given organism
@api_view(['GET'])
def list_proteins(request, taxa_id):
    try:
        # Fecth matching organism based on taxa id passed
        organism = Organisms.objects.get(taxa_id=taxa_id)
    except Organisms.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = Organism_All_ProteinsSerializer(organism)

        response = []
        for protein_id in serializer.data['organisms']:
            # Fetch associated proteins's domain's seq pk value
            protein = Proteins.objects.get(protein_id=protein_id)
            domain = Domains.objects.get(protein=protein)
            id = domain.id
            # turn serializer data into a list of objects,
            # each containing associated protein_id of the organism,
            # rather than a list of protein_ids of the organism
            response.append({
                'id': id,
                'protein_id': protein_id
            })

        # Convert list to str with .dumps and str to json with .loads
        json_response = json.dumps(response)
        json_response = json.loads(json_response)

        return Response(json_response)

# GET - Return list of all domains in all the proteins for a given organism
@api_view(['GET'])
def list_domains(request, taxa_id):
    try:
        # fetch all domain pfams of proteins in the organism matching the taxa id kwarg.
        organism = Organisms.objects.get(taxa_id=taxa_id)
        all_proteins = Proteins.objects.filter(taxonomy=organism)
        domains_list = []
        domain_pk_list = []
        for protein in all_proteins:
            domain = Domains.objects.get(protein_id=protein.protein_id)
            domain_pk_list.append(domain.id)
            domains_list.append(domain)
    except Organisms.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        domain_contents = []
        # Use enumerate so we can iterate and assign the domain's seq pk value,
        # that we saved in a list prior to this
        for domain in enumerate(domains_list):
            serializer = Proteins_All_DomainsSerializer(domain[1])
            id = domain_pk_list[domain[0]]
            domain_contents.append({
                'id': id,
                'pfam_id': serializer.data['pfam_id'],
            })

        json_response = json.dumps(domain_contents)
        json_response = json.loads(json_response)

        return Response(json_response)

# GET - Return domain coverage for a given protein
@api_view(['GET'])
def protein_coverage(request, protein_id):
    try:
        start_list = []
        end_list = []

        # As some proteins have more than one domain, fetch all associated
        # domains of the protein and put them in lists
        protein_domains = Domains.objects.filter(protein_id=protein_id)
        for entry in protein_domains:
            start_list.append(entry.start)
            end_list.append(entry.end)

        # Get and store the length of a protein
        protein = Proteins.objects.get(protein_id=protein_id)
        length = protein.length

        # Use formula: sum of end_list - sum of start list / length,
        # to find coverage of domain
        coverage = (sum(end_list) - sum(start_list)) / (length)
        coverage = {"coverage": coverage}
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return Response(coverage)

# end of code i wrote
