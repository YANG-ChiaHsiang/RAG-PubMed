import argparse
import polars as pl


parser = argparse.ArgumentParser()
args = parser.parse_args()
parser.add_argument("--merge_csv_file", type=str, help="Path to the CSV file to merge.")
parser.add_argument("--after_year", type=int, help="Year to filter after.")
parser.add_argument("--output_csv_file", type=str, help="Path to the output CSV file.")
args = parser.parse_args()

if __name__ == "__main__":
    df = pl.read_csv(args.merge_csv_file)
    filtered_df = df.filter(df["Year"] > args.after_year)

    columns_to_check = ["PMID", "Title", "Abstract", "Authors", "Year", "Journal"]
    filtered_df = filtered_df.drop_nulls(subset=columns_to_check)
    filtered_df.write_csv(args.output_csv_file)
    print(f"Filtered data saved to {args.output_csv_file}.")


