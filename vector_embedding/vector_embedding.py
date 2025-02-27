import pandas as pd
import torch
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# 設定裝置
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# 設定模型
model_name = "abhinand/MedEmbed-base-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True).to(device)

# 內積索引 (可以改為 IndexFlatL2)
embedding_dim = 768  
index = faiss.IndexFlatIP(embedding_dim)

# 儲存 metadata
paper_metadata = []

# 產生 embedding 的函數
def generate_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs).last_hidden_state  # 取得最後一層隱藏狀態
    embedding = outputs.mean(dim=1)  # 均值池化
    return embedding.to(torch.float32).cpu().numpy().flatten()

# 遍歷多個檔案
for file_idx in range(1, 1274):  # 確保範圍正確 (從 1 到 1273)
    file_path = f"../data/pubmed_baseline/csv/pubmed25n{str(file_idx).zfill(4)}.csv"
    
    try:
        df = pd.read_csv(file_path)
        print(f"Processing: {file_path} ({len(df)} records)")

        all_embeddings = []
        for _, row in df.iterrows():
            text = f"{row['Title']} {row['Abstract']}"  # 合併標題與摘要
            embedding = generate_embedding(text)  # 轉換為 embedding
            all_embeddings.append(embedding)
            
            paper_metadata.append({
                "PMID": row["PMID"], 
                "Title": row["Title"], 
                "Abstract": row["Abstract"], 
                "Year": row["Year"]
            })

        # 轉換為 FAISS 格式並新增索引
        all_embeddings = np.array(all_embeddings).astype("float32")
        index.add(all_embeddings)
    
    except FileNotFoundError:
        print(f"File not found: {file_path}, skipping...")
        continue  # 若檔案不存在則跳過

# 儲存 FAISS 索引與 metadata
faiss.write_index(index, "pubmed_index.faiss")
np.save("pubmed_metadata.npy", paper_metadata)

print("FAISS index and metadata saved successfully.")