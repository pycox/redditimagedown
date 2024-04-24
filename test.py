import os
import csv

metadata_csv_path = "test.csv"

if os.path.exists(metadata_csv_path) == False:
    with open(
        metadata_csv_path, mode="w", newline="", encoding="utf-8-sig"
    ) as metadata_file:
        metadata_writer = csv.writer(metadata_file)