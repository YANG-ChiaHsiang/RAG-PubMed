import os
import argparse
from ftplib import FTP

def download_pubmed_files(start_file, end_file, local_dir="./data/pubmed_baseline"):
    """Downloads PubMed baseline files from FTP."""

    # FTP server details
    FTP_HOST = "ftp.ncbi.nlm.nih.gov"
    FTP_DIR = "/pubmed/baseline"

    try:
        # Connect to FTP
        ftp = FTP(FTP_HOST)
        ftp.login(user="anonymous", passwd="yang900412@gmail.com")  # Use your email as the password
        ftp.cwd(FTP_DIR)

        os.makedirs(local_dir, exist_ok=True)

        # Download files in loop
        for i in range(start_file, end_file + 1):
            filename = f"pubmed25n{i:04d}.xml.gz"
            local_filepath = os.path.join(local_dir, filename)

            print(f"Downloading {filename}...")

            try:
                with open(local_filepath, 'wb') as f:
                    ftp.retrbinary(f"RETR {filename}", f.write)
            except Exception as e:
                print(f"Error downloading {filename}: {e}")

        print("Download process completed.")

        # Close FTP connection
        ftp.quit()

    except Exception as e:
        print(f"FTP connection or other error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download PubMed baseline files.")
    parser.add_argument("start_file", type=int, help="Start file number.")
    parser.add_argument("end_file", type=int, help="End file number.")
    parser.add_argument("--local_dir", type=str, default="./data/pubmed_baseline", help="Local directory to save files.")

    args = parser.parse_args()

    download_pubmed_files(args.start_file, args.end_file, args.local_dir)