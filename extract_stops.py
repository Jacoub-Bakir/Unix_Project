import csv

def extract_ids(csv_file, output_dir):
    # Dictionary to store unique IDs for each arrtype
    id_dict = {'tram': set(), 'metro': set(), 'bus': set(), 'rail': set()}

    # Open the CSV file and extract stop IDs and stop area IDs based on arrtype
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            # Extract arrid and arrtype
            arrid = row['arrid']
            arrtype = row['arrtype']

            # Add arrid to the corresponding list in id_dict based on arrtype
            if arrtype == 'metro':
                id_dict['metro'].add(arrid)
            elif arrtype == 'bus':
                zdaid = row['zdaid']
                arrfarezone = row['arrfarezone']
                if zdaid and arrfarezone == '1': 
                    id_dict['bus'].add(zdaid)
            elif arrtype == 'tram':
                zdaid = row['zdaid']
                if zdaid:  # Check if zdaid is not empty
                    id_dict['tram'].add(zdaid)
            elif arrtype == 'rail':
                zdaid = row['zdaid']
                if zdaid:  # Check if zdaid is not empty
                    id_dict['rail'].add(zdaid)

    # Save extracted IDs to separate text files based on arrtype
    for arrtype, ids in id_dict.items():
        txt_file = f"{output_dir}/{arrtype}_ids.txt"
        with open(txt_file, 'w') as outfile:
            for id in ids:
                outfile.write(f"{id}\n")
        print(f"{arrtype.capitalize()} IDs saved to {txt_file}")

if __name__ == "__main__":
    csv_file = "/Users/mac/Desktop/ParisCité_M1/Adm_Linux/project/updates/stops.csv" 
    output_dir = "/Users/mac/Desktop/ParisCité_M1/Adm_Linux/project/updates" 

    extract_ids(csv_file, output_dir)
