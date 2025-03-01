# RAG-PubMed

本專案旨在使用 PubMed 資料庫創建一個論文推薦系統。該系統採用了 RAG (Retrieval-Augmented Generation) 技術，並使用 MedEmbed 作為醫學和臨床信息檢索的專用嵌入模型。此外，系統使用本地化的 faiss 作為向量數據庫。PubMed 資料庫包含超過 2000 萬篇論文數據，並使用論文的標題和摘要作為查詢對象。

![Architecture](https://github.com/YANG-ChiaHsiang/RAG-PubMed/blob/main/RAG.png)

## 使用 Conda 環境運行

1. 創建 Conda 環境
    ```bash
    conda create -n rag python=3.9
    conda activate rag
    ```
2. 安裝套件
    ```bash
    pip install transformers torch einops faiss-gpu polars python-dotenv
    pip install 'numpy<2'
    ```

## 實作步驟

### 1. 數據預處理

1. 在專案目錄下創建 `.env` 文件：
    ```
    OPENAI_API_KEY=your_openai_api_key
    MAIL_ACCOUNT=your_email@example.com
    ```
    將 `your_openai_api_key` 替換為您的實際 OpenAI API 密鑰，並將 `your_email@example.com` 替換為您的電子郵件帳戶。

2. 進入 `data/pubmed_baseline` 目錄：
    ```bash
    cd data/pubmed_baseline
    ```

3. 通過 FTP 獲取 XML.gz 文件，並使用 `nohup` 在後台運行 `PubMed_get.sh` 腳本：
    [NCBI FTP](https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/)
    ```bash
    nohup ./PubMed_get.sh > PubMed_get_output.log 2>&1 &
    ```
    - 此命令執行腳本，將輸出重定向到 `PubMed_get_output.log`，並在後台運行。

4. 通過運行 `PubMed_unzip.sh` 命令解壓下載的 `.gz` 文件：
    ```bash
    nohup ./PubMed_unzip.sh > PubMed_unzip_output.log 2>&1 &
    ```
    - 此命令解壓所有 `.gz` 擴展名的文件。

5. 使用以下命令將解壓的 XML 文件轉換為 CSV 格式：
    ```bash
    nohup python PubMed_Convert_xml2csv.py > PubMed_Convert_output.log 2>&1 &
    ```
    - 此命令將解壓的 XML 文件轉換為 CSV 格式。

6. 通過運行 `PubMed_merge_csv.py` 腳本將所有 CSV 文件合併為一個文件：
    ```bash
    nohup python PubMed_merge_csv.py --csv_folder './csv' --output_file './merged_output.csv' > PubMed_merge_output.log 2>&1 &
    ```
    - 此命令將所有 CSV 文件合併為一個文件，並將輸出記錄到 `PubMed_merge_output.log`。

7. 使用 `PutMed_after_Year.py` 按年份篩選文章。示例：
    ```bash
    nohup python PutMed_after_Year.py --merge_csv_file './merged_output.csv' --after_year 2020 --output_csv_file 'merged_2020.csv' > PubMed_after_Year.log 2>&1 &
    ```
    - 此命令篩選合併的 CSV 文件中指定年份之後發表的文章，並將輸出記錄到 `PubMed_after_Year.log`。

### 2. 將嵌入向量存儲在向量數據庫（faiss）中

#### 使用 0, 1 GPU

1. 設置可見的 GPU：
    ```bash
    export CUDA_VISIBLE_DEVICES=0,1
    ```

2. 將嵌入向量存儲在向量數據庫中：
    ```bash
    chmod +x run_embedding_to_vector.sh 
    nohup ./run_embedding_to_vector.sh > output/2020/embedding_output.log 2>&1 &
    ```
