# RAG-PubMed

## 1. 數據預處理

### 步驟：

1. 進入 `data/pubmed_baseline` 目錄：

    ```bash
    cd data/pubmed_baseline
    ```

2. 通過 FTP 獲取 XML.gz 文件，並使用 `nohup` 在後台運行 `PubMed_get.sh` 腳本：
    [NCBI FTP](https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/)

    ```bash
    nohup ./PubMed_get.sh > PubMed_get_output.log 2>&1 &
    ```

    - 此命令執行腳本，將輸出重定向到 `PubMed_get_output.log`，並在後台運行。

3. 通過運行 `PubMed_unzip.sh` 命令解壓下載的 `.gz` 文件：

    ```bash
    nohup ./PubMed_unzip.sh > PubMed_unzip_output.log 2>&1 &
    ```

    - 此命令解壓所有 `.gz` 擴展名的文件。

4. 使用以下命令將解壓的 XML 文件轉換為 CSV 格式：

    ```bash
    nohup python PubMed_Convert_xml2csv.py > PubMed_Convert_output.log 2>&1 &
    ```

    - 此命令將解壓的 XML 文件轉換為 CSV 格式。

5. 通過運行 `PubMed_merge_csv.py` 腳本將所有 CSV 文件合併為一個文件：

    ```bash
    nohup python PubMed_merge_csv.py --csv_folder './csv' --output_file './merged_output.csv' > PubMed_merge_output.log 2>&1 &
    ```

    - 此命令將所有 CSV 文件合併為一個文件，並將輸出記錄到 `PubMed_merge_output.log`。

6. 使用 `PutMed_after_Year.py` 按年份篩選文章。示例：

    ```bash
    nohup python PutMed_after_Year.py --merge_csv_file './merged_output.csv' --after_year 2020 --output_csv_file 'merged_2020.csv' > PubMed_after_Year.log 2>&1 &
    ```

    - 此命令篩選合併的 CSV 文件中指定年份之後發表的文章，並將輸出記錄到 `PubMed_after_Year.log`。

## 2. 將嵌入向量存儲在向量數據庫（faiss）中

### 使用 0, 1 GPU

1. 設置可見的 GPU：

    ```bash
    export CUDA_VISIBLE_DEVICES=0,1
    ```

2. 將嵌入向量存儲在向量數據庫中：

    ```bash
    chmod +x run_embedding_to_vector.sh 
    nohup ./run_embedding_to_vector.sh > output/2020/embedding_output.log 2>&1 &
    ```

## 附加說明

- 確保 `PubMed_get.sh` 腳本是可執行的（`chmod +x PubMed_get.sh`）。
- 根據 `.gz` 文件的大小和數量，解壓過程可能需要相當長的時間。
- 考慮使用 `parallel` 等並行處理工具來加速大數據集的解壓過程。
- 根據您的具體用例，添加進一步解析解壓 XML 文件和處理數據的步驟。
- 可以為 bash 腳本添加額外的錯誤處理。
- 可以添加額外的步驟來清理解壓後的 .gz 文件。
- 如果遇到 FTP 連接問題，請檢查您的網絡設置和 NCBI FTP 服務器狀態。
- 最好添加有關如何安裝運行腳本所需依賴項的信息。
- 如果您在雲環境中運行此操作，您可能需要添加將文件複製到雲存儲的步驟。
- 考慮使用虛擬環境來管理此項目的依賴項。

