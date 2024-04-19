import csv

# Open the CSV file
with open('sub_list.csv', newline='') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)
    
    f_name = [row[0] for row in csvreader]
    
    print(f_name)