from django.db import models

# I wrote this code


# Organism Table
class Organisms(models.Model):
    taxa_id = models.IntegerField(primary_key=True, null=False, blank=False)
    clade = models.CharField(max_length=1)
    genus = models.CharField(max_length=200)
    species = models.CharField(max_length=200)

    def __str__(self):
        return str(self.taxa_id)


# Protein Table
class Proteins(models.Model):
    protein_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.CharField(max_length=200)
    length = models.IntegerField(null=False, blank=False)
    taxonomy = models.ForeignKey(
        Organisms,
        on_delete=models.CASCADE,
        related_name='organisms',
    )

    def __str__(self):
        return str(self.protein_id)


# Domain and Domain Pfam Tables
class Domain_Pfam(models.Model):
    domain_id = models.CharField(max_length=7, primary_key=True)
    domain_desc = models.CharField(max_length=200)

    def __str__(self):
        return str(self.domain_id)


class Domains(models.Model):
    # Use AUTO_INCREMENT pk for Domains model as specified in rest_specifications_and_examples
    desc = models.CharField(max_length=200)
    start = models.IntegerField(null=False, blank=False)
    end = models.IntegerField(null=False, blank=False)
    domain = models.ForeignKey(
        Domain_Pfam,
        on_delete=models.CASCADE,
        related_name='domain_pfam',
        blank=True,
        null=True,
    )
    protein = models.ForeignKey(
        Proteins,
        on_delete=models.CASCADE,
        related_name='domains',
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)
    

# End of code i wrote