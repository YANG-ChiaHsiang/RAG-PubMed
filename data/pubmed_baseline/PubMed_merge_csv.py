import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Merge multiple CSV files into a single CSV file.")
parser.add_argument("--csv_folder", type=str, default="./csv", help="Path to the folder containing CSV files")
parser.add_argument("--output_file", type=str, default="./merged_output.csv", help="Output filename")
args = parser.parse_args()


def merge_csv_files(csv_folder, output_file):
    first_file = True
    file_count = 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        for file in os.listdir(csv_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(csv_folder, file)
                try:
                    df = pd.read_csv(file_path)
                    df = df.dropna(subset=["Title", "Abstract"])  # Filter out rows where Title or Abstract is NaN
                    file_count += 1
                    
                    df.to_csv(out_file, mode='a', index=False, header=first_file)
                    first_file = False  # Don't write headers for subsequent files
                    print(f"Processed file {file_count}: {file}")
                except Exception as e:
                    print(f"Error occurred while reading {file}: {e}")
    
    print(f"Merged CSV has been saved to {output_file}")

if __name__ == "__main__":
    folder_path = args.csv_folder  # Folder containing CSV files
    output_csv = args.output_file  # Output CSV file
    merge_csv_files(folder_path, output_csv)
