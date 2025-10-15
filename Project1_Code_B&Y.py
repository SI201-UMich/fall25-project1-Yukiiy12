# Name: Xi (Benson) Chen, Zhiyu (Yuki) Pu
# Student ID: Chen: 3617 1540, Pu: 2783 7481
# Email: chexfeii@umich.edu, zhiyupu@umich.edu
# How we used generative AI:

import os
import csv

#Read penguins.csv file
def load_data(f):

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    data = []

    with open(full_path, 'r', newline = '') as file:
        r = csv.DictReader(file)

        for row in r:
            data.append(row)

    return data

#Drops rows with invalid or missing data
def clean_and_cast(data):
    null_values = {'', 'na', 'null'}

    cleaned_data = []

    for row in data:
        
        new_row = {}

        for key, value in row.items():
            cleaned_value = str(value).strip()

            if cleaned_value.lower() in null_values:
                new_row[key] = None
                continue

            try:
                if '.' not in cleaned_value:
                    new_row[key] = int(cleaned_value)

                else:
                    new_row[key] = float(cleaned_value)

            except ValueError:
                new_row[key] = cleaned_value

        cleaned_data.append(new_row)

    return cleaned_data

#Benson's First Calculation: Calculate average body mass for male penguins and female penguins of each species
def avg_mass_by_species_sex(cleaned_data):

    data = {}

    for row in cleaned_data:
        species = row.get('species', '')
        sex = row.get('sex', '')
        key = (species, sex)

        try:
            body_mass = float(row["body_mass_g"])

        except (ValueError, TypeError, KeyError):
            continue

        if key not in data:
            data[key] = []
        
        data[key].append(body_mass)

    benson_result_1 = []

    for (species, sex), masses in data.items():
        avg_mass = sum(masses) / len(masses)

        benson_result_1.append((species, sex, avg_mass))

    return benson_result_1

#Benson's Second Calculation (1): Calculate average flipper length of penguins for each species
def species_flipper_avg(cleaned_data):
    
    data = {}

    for row in cleaned_data:
        species = row.get('species', '')

        try:
            flipper_length = float(row["flipper_length_mm"])

        except (ValueError, TypeError, KeyError):
            continue

        if species not in data:
            data[species] = []
        
        data[species].append(flipper_length)

    benson_result_2 = {}

    for species, lengths in data.items():
        if lengths:
            avg_length = sum(lengths) / len(lengths)
            benson_result_2[species] = avg_length

    return benson_result_2

#Benson's Second Calculation (2): Calculate the percentage of penguins with flipper length greater than the average flipper length for each island and species
def flipper_above_species_avg(cleaned_data, benson_result_2):
    
    total_counts = {}
    above_avg_counts = {}

    for row in cleaned_data:
        species = row.get('species', '')
        island  = row.get('island', '')

        if species not in benson_result_2:
            continue

        try:
            flipper_length = float(row["flipper_length_mm"])

        except (ValueError, TypeError, KeyError):
            continue

        key = (island, species)

        if key not in total_counts:
            total_counts[key] = 0
        
        total_counts[key] += 1

        species_avg_length = benson_result_2[species]

        if flipper_length > species_avg_length:
            if key not in above_avg_counts:
                above_avg_counts[key] = 0
            
            above_avg_counts[key] += 1

    benson_result_3 = []

    for key in total_counts:
        island = key[0]
        species = key[1]
        total = total_counts[key]

        if key in above_avg_counts:
            above_avg = above_avg_counts[key]
        else:
            above_avg = 0

        if total > 0:
            percentage = (above_avg / total) * 100

        else:
            percentage = 0.0

        benson_result_3.append((island, species, percentage))

    return benson_result_3

#Yuki's First Calculation: Calculate average bill length/depth for male and female penguins in each species
def avg_bill_by_species_sex(cleaned_data):

    data = {}

    for row in cleaned_data:
        species = row.get('species', '')
        sex = row.get('sex', '')
        key = (species, sex)

        try:
            bill_length = float(row["bill_length_mm"])
            bill_depth = float(row["bill_depth_mm"])

        except (ValueError, TypeError, KeyError):
            continue

        if key not in data:
            data[key] = {'bill_length': [], 'bill_depth': []}

        data[key]['bill_length'].append(bill_length)
        data[key]['bill_depth'].append(bill_depth)

    yuki_result_1 = []

    for (species, sex), values in data.items():
        avg_length = sum(data[(species, sex)]['bill_length']) / len(data[(species, sex)]['bill_length'])
        avg_depth = sum(data[(species, sex)]['bill_depth']) / len(data[(species, sex)]['bill_depth'])

        yuki_result_1.append((species, sex, avg_length, avg_depth))

    return yuki_result_1

if __name__ == "__main__":
    data = load_data('penguins.csv')
    cleaned_data = clean_and_cast(data)

print(cleaned_data)