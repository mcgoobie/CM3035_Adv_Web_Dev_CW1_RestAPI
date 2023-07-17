from biosciapp.models import Organisms, Proteins, Domains, Domain_Pfam
import csv
import pandas as pd

# i wrote this code

def run():
    # Initialize empty list to store each sorted row of data
    organisms_list = []
    proteins_list = []
    sequences_list = []
    domains_list = []
    pfams_list = []

    with open('csv_files/assignment_data_set.csv') as data_set:

        print('reading "assignment_data_set.csv" file.')

        dataset_file_content = csv.reader(data_set)

        for row in dataset_file_content:
            new_line = []
            # Handling of data in Organisms Table
            new_line.append(row[1])  # taxa_id
            new_line.append(row[2])  # clade

            # Scientific Name
            scientific_name = row[3].split(' ')

            # Splitting Sci. name into Genus and Species, Sci. Name w/ > 2 tokens will keep
            # '... sp.' as genus name and remaining tokens as species name
            if (len(scientific_name) != 2):
                genus = scientific_name[0] + ' ' + scientific_name[1]
                species = ''
                for s_token in scientific_name[2:]:
                    if (s_token == scientific_name[-1]):
                        species += s_token
                    else:
                        species += s_token
                        species += ' '

                new_line.append(genus)  # genus
                new_line.append(species)  # species
            else:
                new_line.append(scientific_name[0])  # genus
                new_line.append(scientific_name[1])  # species

            # Each new_line's list contents will be : [taxa_id, clade, genus, species]
            organisms_list.append(new_line)

            # Handling of data in Proteins Table
            new_line = []
            # Proteins df
            new_line.append(row[0])  # protein_id
            new_line.append(row[8])  # length of protein
            new_line.append(row[1])  # taxa_id

            proteins_list.append(new_line)

            # Handling of data in Domains Table
            new_line = []
            # Proteins df
            new_line.append(row[0])  # protein_id
            new_line.append(row[5])  # pfam_id
            new_line.append(row[4])  # desc
            new_line.append(row[6])  # start
            new_line.append(row[7])  # end

            domains_list.append(new_line)

    with open('csv_files/assignment_data_sequences.csv') as data_set:

        print('reading "assignment_data_sequences.csv" file.')

        dataset_file_content = csv.reader(data_set)

        for row in dataset_file_content:
            new_line = []
            # Handling of data in Protein Sequences Table
            new_line.append(row[0])  # protein_id
            new_line.append(row[1])  # sequence

            sequences_list.append(new_line)

    with open('csv_files/pfam_descriptions.csv') as data_set:

        print('reading "pfam_descriptions.csv" file.')

        dataset_file_content = csv.reader(data_set)

        for row in dataset_file_content:
            new_line = []
            # Handling of data in Protein Sequences Table
            new_line.append(row[0])  # pfam_id
            new_line.append(row[1])  # pfam_family desc.

            pfams_list.append(new_line)

    # Add sorted lines of data into a Dataframe that resembles the table via column name
    organisms_df = pd.DataFrame(
        organisms_list, columns=['taxa_id', 'clade', 'genus', 'species'])

    proteins_df = pd.DataFrame(
        proteins_list, columns=['protein_id', 'length', 'taxa_id'])
    sequences_df = pd.DataFrame(
        sequences_list, columns=['protein_id', 'sequence']
    )

    domains_df = pd.DataFrame(
        domains_list, columns=['protein_id', 'domain_id', 'desc', 'start', 'end'])
    pfams_df = pd.DataFrame(
        pfams_list, columns=['domain_id', 'domain_desc'])

    print('Populated DataFrames using .csv files.')

    # Drop duplicated rows in the DataFrame
    organisms_df.drop_duplicates(keep='first')
    proteins_df.drop_duplicates(keep='first')
    domains_df.drop_duplicates(keep='first')
    pfams_df.drop_duplicates(keep='first')

    print('Removed duplicated rows in DataFrames from .csv files.')

    # Clear existing records if any
    Organisms.objects.all().delete()
    Proteins.objects.all().delete()
    Domains.objects.all().delete()
    Domain_Pfam.objects.all().delete()

    print('Existing records in tables dropped.')

    # Insertion of rows into Organisms Model
    for index, row in organisms_df.iterrows():
        new_organism = Organisms(
            taxa_id=row['taxa_id'],
            clade=row['clade'],
            genus=row['genus'],
            species=row['species'],
        )
        new_organism.save()
    print('Organisms Table populated.')

    # use pd.merge to join both proteins and sequences df (similar to INNER JOIN in SQL)
    proteins_df = pd.merge(proteins_df, sequences_df, on='protein_id')

    # Insertion of rows into Proteins and Protein Sequences
    for index, row in proteins_df.iterrows():
        new_protein = Proteins(
            protein_id=row['protein_id'],
            sequence=row['sequence'],
            length=row['length'],
            taxonomy=Organisms.objects.get(
                taxa_id=row['taxa_id'])
        )
        new_protein.save()
    print('Proteins Tables populated.')

    domains_df = pd.merge(domains_df, pfams_df, on='domain_id')

    # Insertion of rows into Domains and Domain_Pfam
    for index, row in domains_df.iterrows():
        new_domain_pfam = Domain_Pfam(
            domain_id=row['domain_id'],
            domain_desc=row['domain_desc']
        )
        new_domain_pfam.save()

        new_domain = Domains(
            # domain_id=row['domain_id'],
            desc=row['desc'],
            start=row['start'],
            end=row['end'],
            # There exists some domains with proteins not found in the dataset,
            # in such a case a value of None will be given.
            protein=check_for_protein_ref(row['protein_id']),
            domain=new_domain_pfam,
        )
        new_domain.save()

    print('Domains and Pfam Families Tables populated.')


# Function checks for protein_id in Proteins table that matches corresponding row in Domains DataFrame.
# The reference Proteins object will be returned if found, if None value will be used.
def check_for_protein_ref(protein_id):
    try:
        protein = Proteins.objects.get(protein_id=protein_id)
        return protein
    except Proteins.DoesNotExist:
        protein = None
        return protein


# end of code i wrote