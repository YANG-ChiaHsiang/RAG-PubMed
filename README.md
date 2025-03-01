# RAG-PubMed

This project aims to create a paper recommendation system using the PubMed database. The system adopts RAG (Retrieval-Augmented Generation) technology and uses MedEmbed as a specialized embedding model for medical and clinical information retrieval. Additionally, the system uses a localized faiss as the vector database. The PubMed database contains over 20 million paper records, using the titles and abstracts of the papers as query objects.

![Architecture](https://github.com/YANG-ChiaHsiang/RAG-PubMed/blob/main/RAG.png)


## Running with Conda Environment

1. Create a Conda environment
    ```bash
    conda create -n rag python=3.9
    conda activate rag
    ```
2. Install packages
    ```bash
    pip install transformers torch einops faiss-gpu polars python-dotenv
    pip install 'numpy<2'
    ```

## Implementation Steps

### 1. Data Preprocessing

1. Create a `.env` file in the project directory:
    ```
    OPENAI_API_KEY=your_openai_api_key
    MAIL_ACCOUNT=your_email@example.com
    ```
    Replace `your_openai_api_key` with your actual OpenAI API key and `your_email@example.com` with your email account.

2. Navigate to the `data/pubmed_baseline` directory:
    ```bash
    cd data/pubmed_baseline
    ```

3. Obtain XML.gz files via FTP and run the `PubMed_get.sh` script in the background using `nohup`:
    [NCBI FTP](https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/)
    ```bash
    nohup ./PubMed_get.sh > PubMed_get_output.log 2>&1 &
    ```
    - This command executes the script, redirects the output to `PubMed_get_output.log`, and runs it in the background.

4. Unzip the downloaded `.gz` files by running the `PubMed_unzip.sh` command:
    ```bash
    nohup ./PubMed_unzip.sh > PubMed_unzip_output.log 2>&1 &
    ```
    - This command unzips all files with the `.gz` extension.

5. Convert the unzipped XML files to CSV format using the following command:
    ```bash
    nohup python PubMed_Convert_xml2csv.py > PubMed_Convert_output.log 2>&1 &
    ```
    - This command converts the unzipped XML files to CSV format.

6. Merge all CSV files into one file by running the `PubMed_merge_csv.py` script:
    ```bash
    nohup python PubMed_merge_csv.py --csv_folder './csv' --output_file './merged_output.csv' > PubMed_merge_output.log 2>&1 &
    ```
    - This command merges all CSV files into one file and logs the output to `PubMed_merge_output.log`.

7. Filter articles by year using `PutMed_after_Year.py`. Example:
    ```bash
    nohup python PutMed_after_Year.py --merge_csv_file './merged_output.csv' --after_year 2020 --output_csv_file 'merged_2020.csv' > PubMed_after_Year.log 2>&1 &
    ```
    - This command filters articles published after the specified year in the merged CSV file and logs the output to `PubMed_after_Year.log`.

### 2. Store Embedding Vectors in the Vector Database (faiss)

#### Using 0, 1 GPU

1. Set visible GPUs:
    ```bash
    export CUDA_VISIBLE_DEVICES=0,1
    ```

2. Store embedding vectors in the vector database:
    ```bash
    chmod +x run_embedding_to_vector.sh 
    nohup ./run_embedding_to_vector.sh > output/2020/embedding_output.log 2>&1 &
    ```
