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

if __name__ == "__main__":
    data = load_data('penguins.csv')
    cleaned_data = clean_and_cast(data)

print(cleaned_data)