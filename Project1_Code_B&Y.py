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