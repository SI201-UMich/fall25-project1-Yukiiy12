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

#Yuki's Second Calculation: Calculate the percentage of penguins with bill length/depth above the median for each island and species
def species_bill_ratio_median(cleaned_data):

    species_ratios = {}

    for row in cleaned_data:
        species = row.get('species', '')

        try:
            bill_length = float(row["bill_length_mm"])
            bill_depth = float(row["bill_depth_mm"])

            if bill_depth == 0:
                continue

        except (ValueError, TypeError, KeyError):
            continue

        ratio = bill_length / bill_depth

        if species not in species_ratios:
            species_ratios[species] = []

        species_ratios[species].append(ratio)

    species_medians = {}

    for species, ratios in species_ratios.items():
        if ratios:
            sorted_ratios = sorted(ratios)
            n = len(sorted_ratios)
            mid = n // 2

            if n % 2 == 0:
                median = (sorted_ratios[mid - 1] + sorted_ratios[mid]) / 2
            else:
                median = sorted_ratios[mid]

            species_medians[species] = median

    total_counts = {}
    above_median_counts = {}

    for row in cleaned_data:
        island = row.get('island', '')
        species = row.get('species', '')

        if species not in species_medians:
            continue

        try:
            bill_length = float(row["bill_length_mm"])
            bill_depth = float(row["bill_depth_mm"])

            if bill_depth == 0:
                continue

        except (ValueError, TypeError, KeyError):
            continue

        ratio = bill_length / bill_depth
        
        key = (island, species)

        total_counts[key] = total_counts.get(key, 0) + 1

        if ratio > species_medians[species]:
            above_median_counts[key] = above_median_counts.get(key, 0) + 1

    yuki_result_2 = []

    for key in total_counts:
        island = key[0]
        species = key[1]
        total = total_counts[key]
        above_median = above_median_counts.get(key, 0)

        if total > 0:
            percentage = (above_median / total) * 100
        else:
            percentage = 0.0

        yuki_result_2.append((island, species, percentage))

    return yuki_result_2

#Unit Tests For All Calculations
class TestCalculations(unittest.TestCase):

    def setUp(self):
        self.data = load_data('penguins.csv')
        self.cleaned_data = clean_and_cast(self.data)

    #Benson's First Calculation (The Average Body Mass by Species and Sex)
    
    def test_avg_mass_basic(self): #Normal case: result should not be empty and contain tuples
        result = avg_mass_by_species_sex(self.cleaned_data)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], tuple)

    def test_avg_mass_species_present(self): #Ensure Adelie species is in result
        result = avg_mass_by_species_sex(self.cleaned_data)
        species_list = [r[0] for r in result]
        self.assertIn('Adelie', species_list)

    def test_avg_mass_values_reasonable(self): #Check body mass averages should be positive
        result = avg_mass_by_species_sex(self.cleaned_data)
        for _, _, avg in result:
            self.assertGreater(avg, 0)

    def test_avg_mass_ignore_invalid(self): #Ensure the function can skip rows with invalid body mass
        invalid_row = {'species': 'Adelie', 'sex': 'Male', 'body_mass_g': 'NA'}
        data = self.cleaned_data + [invalid_row]
        result = avg_mass_by_species_sex(data)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)

    #Benson's Second Calculation (The Percentage Above Average Flipper Length)
    
    def test_flipper_above_basic(self): #Normal case: returns list not empty
        avg_dict = species_flipper_avg(self.cleaned_data)
        result = flipper_above_species_avg(self.cleaned_data, avg_dict)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_flipper_above_percent_range(self): #Percentage values should be between 0 and 100
        avg_dict = species_flipper_avg(self.cleaned_data)
        result = flipper_above_species_avg(self.cleaned_data, avg_dict)
        for _, _, pct in result:
            self.assertTrue(0 <= pct <= 100)

    def test_flipper_above_missing_species(self): #Missing species average should be skipped
        fake_avg = {'FakePenguin': 100}
        result = flipper_above_species_avg(self.cleaned_data, fake_avg)
        # Should not contain fake species
        species_list = [s for _, s, _ in result]
        self.assertNotIn('FakePenguin', species_list)

    def test_flipper_above_nonzero_islands(self): #Should include multiple islands
        avg_dict = species_flipper_avg(self.cleaned_data)
        result = flipper_above_species_avg(self.cleaned_data, avg_dict)
        islands = {r[0] for r in result}
        self.assertGreater(len(islands), 1)

    #Yuki's First Calculation (Avg Bill Length/Depth)

    def test_bill_avg_basic(self): #Normal case: returns list of tuples
        result = avg_bill_by_species_sex(self.cleaned_data)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)

    def test_bill_avg_positive(self): #Average length/depth should be positive
        result = avg_bill_by_species_sex(self.cleaned_data)
        for _, _, l, d in result:
            self.assertTrue(l > 0 and d > 0)

    def test_bill_avg_species_included(self): #Ensure Adelie is in species list
        result = avg_bill_by_species_sex(self.cleaned_data)
        species = [r[0] for r in result]
        self.assertIn('Adelie', species)

    def test_bill_avg_handle_missing(self): #Ensure function can skip NA values
        bad_data = self.cleaned_data + [{'species': 'Adelie', 'bill_length_mm': 'NA', 'bill_depth_mm': 'NA'}]
        result = avg_bill_by_species_sex(bad_data)
        self.assertGreaterEqual(len(result), 1)

    #Yuki's Second Calculation (The Percentage of Bill Length/Depth Ratio > Median)

    def test_bill_ratio_basic(self): #Normal case: returns list
        result = species_bill_ratio_median(self.cleaned_data)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_bill_ratio_percent_range(self): #Percentage between 0 and 100
        result = species_bill_ratio_median(self.cleaned_data)
        for _, _, pct in result:
            self.assertTrue(0 <= pct <= 100)

    def test_bill_ratio_ignore_zero_depth(self): #Ensure the function can run when bill_depth = 0
        bad_data = self.cleaned_data + [{'species': 'Adelie', 'bill_length_mm': 40, 'bill_depth_mm': 0}]
        result = species_bill_ratio_median(bad_data)
        self.assertIsInstance(result, list)

    def test_bill_ratio_multiple_species(self): #Ensure the result includes multiple species
        result = species_bill_ratio_median(self.cleaned_data)
        species = {r[1] for r in result}
        self.assertGreater(len(species), 1)
        
#Write all results to a CSV file
def write_csv(filename, results_dict):

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        for title, (headers, rows) in results_dict.items():
            writer.writerow([])
            writer.writerow([title])
            writer.writerow(headers)
            writer.writerows(rows)

if __name__ == "__main__":
    data = load_data('penguins.csv')
    cleaned_data = clean_and_cast(data)

    #Run Benson's First Calculation
    benson_result_1 = avg_mass_by_species_sex(cleaned_data)
    #print("\nBenson's First Calculation: Average Body Mass by Species and Sex\n")
    #for species, sex, avg_mass, count in benson_result_1:
        #print(f"Species: {species}, Sex: {sex}, Average Body Mass: {avg_mass:.2f} g, Count: {count}")

    #Run Benson's Second Calculation
    benson_result_2 = species_flipper_avg(cleaned_data)
    #print("\nBenson's Second Calculation: Average Flipper Length by Species\n")
    #for species, avg_length in benson_result_2.items():
        #print(f"Species: {species}, Average Flipper Length: {avg_length:.2f} mm")

    #Run Benson's Third Calculation
    benson_result_3 = flipper_above_species_avg(cleaned_data, benson_result_2)
    #print("\nBenson's Third Calculation: Percentage of Penguins with Flipper Length Above Species Average by Island and Species\n")
    #for island, species, percentage in benson_result_3:
        #print(f"Island: {island}, Species: {species}, Percentage Above Average Flipper Length: {percentage:.2f}%")

    #Run Yuki's First Calculation
    yuki_result_1 = avg_bill_by_species_sex(cleaned_data)
    #print("\nYuki's First Calculation: Average Bill Length/Depth by Species and Sex\n")
    #for species, sex, avg_length, avg_depth, count in yuki_result_1:
        #print(f"Species: {species}, Sex: {sex}, Average Bill Length: {avg_length:.2f} mm, Average Bill Depth: {avg_depth:.2f} mm, Count: {count}")

    #Run Yuki's Second Calculation
    yuki_result_2 = species_bill_ratio_median(cleaned_data)
    #print("\nYuki's Second Calculation: Percentage of Penguins with Bill Length/Depth Ratio Above Species Median by Island and Species\n")
    #for island, species, percentage in yuki_result_2:
        #print(f"Island: {island}, Species: {species}, Percentage Above Median Bill Length/Depth Ratio: {percentage:.2f}%")
    
    #Write all results to a CSV file
    results = {
        "Benson's First Calculation: Average Body Mass by Species and Sex": (
            ["Species", "Sex", "Average Body Mass (g)"],
            benson_result_1
        ),
        "Benson's Second Calculation: The Percentage of Penguins with Flipper Length Above Species Average by Island and Species": (
            ["Island", "Species", "Percentage Above Average Flipper Length (%)"],
            benson_result_3
        ),
        "Yuki's First Calculation: Average Bill Length/Depth by Species and Sex": (
            ["Species", "Sex", "Average Bill Length (mm)", "Average Bill Depth (mm)"],
            yuki_result_1
        ),
        "Yuki's Second Calculation: The Percentage of Penguins with Bill Length/Depth Ratio Above Species Median by Island and Species": (
            ["Island", "Species", "Percentage Above Median Bill Length/Depth Ratio (%)"],
            yuki_result_2
        )
    }

    write_csv('B&Y_penguin_analysis_results.csv', results)