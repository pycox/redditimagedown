import csv

metadata_csv_path = "image_metadata.csv"

try:
    with open(metadata_csv_path, newline="", encoding="utf-8-sig") as hist_file:
        hist_reader = csv.reader(hist_file)
        print(len(hist_reader))
except:
    print(0)
