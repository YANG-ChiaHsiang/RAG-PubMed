import argparse
import os
import pandas as pd
import torch
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import polars as pl


# 設定 argparse 參數
parser = argparse.ArgumentParser(description="Generate embeddings from PubMed CSVs and create a FAISS index.")
parser.add_argument("--start", type=int, default=1, help="Starting index of files to process (default: 1)")
parser.add_argument("--end", type=int, default=1273, help="Ending index of files to process (default: 1273)")
parser.add_argument("--output_dir", type=str, default=".", help="Directory to save FAISS index and metadata (default: current directory)")
parser.add_argument("--batch_size", type=int, default=3000, help="Batch size for processing (default: 16)")
args = parser.parse_args()

# 設定開始與結束索引
start_idx = args.start
end_idx = args.end
output_dir = args.output_dir
BATCH_SIZE = args.batch_size
# 確保 start_idx <= end_idx
if start_idx > end_idx:
    raise ValueError("Start index cannot be greater than end index.")

# 確保輸出目錄存在
os.makedirs(output_dir, exist_ok=True)

# 設定裝置
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"


# 設定模型
model_name = "abhinand/MedEmbed-base-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True).half().to(device)
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model, device_ids=[0, 1])

# 內積索引 (可以改為 IndexFlatL2)
embedding_dim = 768  
index = faiss.IndexFlatIP(embedding_dim)

# 儲存 metadata
paper_metadata = []

# 產生 embedding 的函數
def generate_embeddings_batch(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs).last_hidden_state
    embeddings = outputs.mean(dim=1)
    return embeddings.cpu().numpy()

# 遍歷指定範圍內的檔案
for file_idx in range(start_idx, end_idx + 1):
    file_path = f"../data/pubmed_baseline/csv/pubmed25n{str(file_idx).zfill(4)}.csv"
    
    try:
        df = pl.read_csv(file_path)
        print(f"Processing: {file_path} ({len(df)} records)")

        paper_metadata = []
        all_embeddings = []
        # 準備數據
        texts = []
        for row in df.iter_rows(named=True):
            text = f"{row['Title']} {row['Abstract']}"
            texts.append(text)
            paper_metadata.append({
                "PMID": row["PMID"], 
                "Title": row["Title"], 
                "Abstract": row["Abstract"], 
                "Year": row["Year"]
            })

        # 批次處理
        for i in tqdm(range(0, len(texts), BATCH_SIZE)):
            batch_texts = texts[i:i + BATCH_SIZE]
            batch_embeddings = generate_embeddings_batch(batch_texts)
            all_embeddings.extend(batch_embeddings)

        # 轉換為 FAISS 格式並新增索引
        all_embeddings = np.array(all_embeddings).astype("float32")
        index.add(all_embeddings)
    
    except FileNotFoundError:
        print(f"File not found: {file_path}, skipping...")
        continue  # 若檔案不存在則跳過

# 儲存 FAISS 索引與 metadata，加入 start_idx 與 end_idx 命名
faiss_index_file = os.path.join(output_dir, f"pubmed_index_{start_idx}_{end_idx}.faiss")
metadata_file = os.path.join(output_dir, f"pubmed_metadata_{start_idx}_{end_idx}.npy")

faiss.write_index(index, faiss_index_file)
np.save(metadata_file, paper_metadata)

print(f"FAISS index saved to {faiss_index_file}")
print(f"Metadata saved to {metadata_file}")
