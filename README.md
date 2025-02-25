# RAG-PubMed

## 1. Retrieving XML.gz Files via FTP

PubMed baseline data is downloaded via FTP from the NCBI server.

### Steps:

1.  Navigate to the `data/pubmed_baseline` directory:

    ```bash
    cd data/pubmed_baseline
    ```

2.  Run the `PubMed_get.sh` script in the background using `nohup` to download the files:

    ```bash
    nohup ./PubMed_get.sh > PubMed_get_output.log 2>&1 &
    ```

    - This command executes the script, redirects output to `PubMed_get_output.log`, and runs it in the background.

## 2. Extracting .gz Files

After downloading the `.gz` files, they need to be extracted.

### Steps:

1.  Navigate to the directory containing the `.gz` files (if not already there):

    ```bash
    cd data/pubmed_baseline
    ```

2.  Run the `PubMed_unzip.sh` command to extract each `.gz` file. You can use a loop to process all files:

    ```bash
    nohup ./PubMed_unzip.sh > PubMed_unzip_output.log 2>&1 &
    ```

    - This loop iterates through all files with the `.gz` extension and extracts them.

3.  Convert XML to CSV file using the following command:

    ```bash
    nohup python PubMed_Convert_xml2csv.py > PubMed_Convert_output.log 2>&1 &
    ```

    - This command converts the extracted XML files to CSV format.

## Additional Notes

- Ensure that the `PubMed_get.sh` script is executable (`chmod +x PubMed_get.sh`).
- The extraction process may take a significant amount of time depending on the size and number of `.gz` files.
- Consider using parallel processing tools like `parallel` to speed up the extraction process for large datasets.
- Add further steps for parsing the extracted XML files and processing the data as needed for your specific use case.
- You can add additional error handling to the bash scripts.
- You can add additional steps to clean up the .gz files after they are extracted.
- If you encounter any issues with the FTP connection, check your network settings and the NCBI FTP server status.
- It's a good practice to add information on how to install any dependencies needed to run the scripts.
- It's a good practice to add information on how to install any dependencies needed to run the scripts.
- If you are running this on a cloud environment you may want to add a step to copy the files to cloud storage.
- If you are running this on a cloud environment you may want to add a step to copy the files to cloud storage.
- Consider using a virtual environment to manage dependencies for this project.
- Consider using a virtual environment to manage dependencies for this project.
