import os
import gc
import polars as pl
import faiss
import torch
import numpy as np
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import argparse

# 設定 argparse 參數
parser = argparse.ArgumentParser(description="Generate embeddings from PubMed CSVs and create a FAISS index.")
parser.add_argument("--csv_path", type=str, default="../data/pubmed_baseline/data.csv", help="Path to the CSV file")
parser.add_argument("--output_dir", type=str, default=".", help="Directory to save FAISS index and metadata (default: current directory)")
parser.add_argument("--batch_size", type=int, default=3000, help="Batch size for processing (default: 3000)")
parser.add_argument("--multi_gpu", action="store_true", help="Use multiple GPUs (default: False)")
args = parser.parse_args()

# Load dataset
def load_dataset(csv_path):
    df = pl.read_csv(csv_path)
    if "Year" in df.columns:
        df = df.with_columns(df["Year"].fill_null(0).cast(int))
    return df

# Load embedding model
def load_embedding_model(device):
    model_name = "abhinand/MedEmbed-base-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True).to(device).eval()
    model.to(torch.bfloat16)
    return model, tokenizer

# Embed text in batches
def embed_text_in_batches(texts, model, tokenizer, device, batch_size=32, output_file="./output/embeddings.npy"):
    texts = list(texts)
    num_samples = len(texts)
    embedding_dim = 768  # `MedEmbed-base-v0.1` 的輸出維度應該是 768

    # **建立 memory-mapped 檔案 (不佔用 RAM)**
    embeddings = np.memmap(output_file, dtype=np.float32, mode='w+', shape=(num_samples, embedding_dim))

    offset = 0
    for i in tqdm(range(0, num_samples, batch_size), desc="Processing Batches"):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt", max_length=512).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        batch_embeddings = outputs.last_hidden_state[:, 0, :].to(torch.float32).cpu().numpy()
        
        # **直接寫入 memory-mapped 檔案**
        batch_size = batch_embeddings.shape[0]
        embeddings[offset:offset + batch_size] = batch_embeddings
        offset += batch_size

        del inputs, outputs, batch_embeddings
        torch.cuda.empty_cache()
        gc.collect()

    embeddings.flush()  # 確保數據寫入硬碟
    print(f"Embeddings saved to {output_file}")
    return output_file  # 回傳 `.npy` 檔案路徑

# Create FAISS index
def create_faiss_index(embeddings):
    d = embeddings.shape[1] # dimension
    N = embeddings.shape[0] # number of embeddings
    nlist = nlist = min(int(4 * np.sqrt(N)), N)
    print(f"Creating FAISS index with nlist = {nlist}")
    
    quantizer = faiss.IndexFlatL2(d)
    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
    
    index.train(embeddings)
    index.add(embeddings)
    return index


if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load dataset
    df = load_dataset(args.csv_path)
    # df = df.head(300000)
    print(f'Number of rows: {len(df)}')

    # Load model
    model, tokenizer = load_embedding_model(device)
    if args.multi_gpu and torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)

    # Embed text in batches
    texts = df["Title"] + ". " + df["Abstract"]
    embedding_file = embed_text_in_batches(texts, model, tokenizer, device, batch_size=args.batch_size)

    # Create FAISS index
    embeddings = np.memmap(embedding_file, dtype=np.float32, mode='r', shape=(len(texts), 768))
    index = create_faiss_index(embeddings)

    # Save index and metadata
    os.makedirs(args.output_dir, exist_ok=True)
    faiss.write_index(index, f"{args.output_dir}/faiss.index")
    df.write_csv(f"{args.output_dir}/metadata.csv")

    print("Index and metadata saved successfully.")