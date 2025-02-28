# RAG-PubMed

## 1. Data Preprocessing

### Steps:

1. Navigate to the `data/pubmed_baseline` directory:

    ```bash
    cd data/pubmed_baseline
    ```

2. Retrieve XML.gz files via FTP and run the `PubMed_get.sh` script in the background using `nohup`:
    [NCBI FTP](https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/)

    ```bash
    nohup ./PubMed_get.sh > PubMed_get_output.log 2>&1 &
    ```

    - This command executes the script, redirects the output to `PubMed_get_output.log`, and runs it in the background.

3. Unzip the downloaded `.gz` files by running the `PubMed_unzip.sh` command:

    ```bash
    nohup ./PubMed_unzip.sh > PubMed_unzip_output.log 2>&1 &
    ```

    - This command unzips all files with the `.gz` extension.

4. Convert the unzipped XML files to CSV format using the following command:

    ```bash
    nohup python PubMed_Convert_xml2csv.py > PubMed_Convert_output.log 2>&1 &
    ```

    - This command converts the unzipped XML files to CSV format.

5. Merge all CSV files into one file by running the `PubMed_merge_csv.py` script:

    ```bash
    nohup python PubMed_merge_csv.py --csv_folder './csv' --output_file './merged_output.csv' > PubMed_merge_output.log 2>&1 &
    ```

    - This command merges all CSV files into one file and logs the output to `PubMed_merge_output.log`.

6. Filter articles by year using `PutMed_after_Year.py`. Example:

    ```bash
    nohup python PutMed_after_Year.py --merge_csv_file './merged_output.csv' --after_year 2020 --output_csv_file 'merged_2020.csv' > PubMed_after_Year.log 2>&1 &
    ```

    - This command filters articles published after the specified year in the merged CSV file and logs the output to `PubMed_after_Year.log`.

## 2. Store Embedding Vectors in Vector Database (faiss)

### Using 0, 1 GPU

1. Set visible GPUs:

    ```bash
    export CUDA_VISIBLE_DEVICES=0,1
    ```

2. Store embedding vectors in the vector database:

    ```bash
    chmod +x run_embedding_to_vector.sh 
    nohup ./run_embedding_to_vector.sh > output/2020/embedding_output.log 2>&1 &
    ```

## Additional Notes

- Ensure the `PubMed_get.sh` script is executable (`chmod +x PubMed_get.sh`).
- The unzipping process may take a considerable amount of time depending on the size and number of `.gz` files.
- Consider using parallel processing tools like `parallel` to speed up the unzipping process for large datasets.
- Add further steps to parse the unzipped XML files and process the data according to your specific use case.
- Add additional error handling to the bash scripts.
- Add steps to clean up the unzipped `.gz` files if necessary.
- If you encounter FTP connection issues, check your network settings and the status of the NCBI FTP server.
- It is advisable to include information on how to install dependencies required to run the scripts.
- If running this in a cloud environment, you may need to add steps to copy files to cloud storage.
- Consider using a virtual environment to manage dependencies for this project.
