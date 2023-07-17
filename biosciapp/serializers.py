from rest_framework import serializers
from biosciapp.models import Organisms, Proteins, Domains, Domain_Pfam

# I wrote this code

# Serializer to return the domain and its description
class DomainPfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain_Pfam
        fields = ['domain_id', 'domain_desc']

class DomainSerializer(serializers.ModelSerializer):
    pfam_id = DomainPfamSerializer(source='domain')

    class Meta:
        model = Domains
        fields = ['pfam_id', 'desc', 'start', 'end']

# Serializer to return Organism
class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisms
        fields = ['taxa_id', 'clade', 'genus', 'species']

# Serializer to create new protein with its associated organism
class Create_New_ProteinSerializer(serializers.ModelSerializer):
    taxonomy= OrganismSerializer()

    class Meta:
        model = Proteins
        fields = ['protein_id', 'sequence', 'length', 'taxonomy']

    def create(self, validated_data):
        taxonomy = self.initial_data.get('taxonomy')
        protein = Proteins(**{**validated_data,
                              'taxonomy': Organisms.objects.create(
                                  taxa_id=taxonomy['taxa_id'],
                                  clade=taxonomy['clade'],
                                  genus=taxonomy['genus'],
                                  species=taxonomy['species']
                              ),
                              })
        protein.save()
        return protein

# Serializer to fetch protein sequence and all we know about it
class ProteinSerializer(serializers.ModelSerializer):
    taxonomy = OrganismSerializer()
    domains = DomainSerializer(many=True)

    class Meta:
        model = Proteins
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']

# Serializer to return list of all proteins in a given organism
class Organism_All_ProteinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisms
        fields = ['organisms']

# Serializer to return list of all domains in all proteins in a given organism
class Proteins_All_DomainsSerializer(serializers.ModelSerializer):
    pfam_id = DomainPfamSerializer(source='domain')

    class Meta:
        model = Domains
        fields = ['pfam_id']


# End of code I wrote