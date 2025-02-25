#!/bin/bash

# 設定要解壓縮的目錄
source_dir="./gz"

# 設定解壓縮後的目標目錄
target_dir="./xml"

# 確保目標目錄存在，如果不存在就創建
mkdir -p "$target_dir"

# 使用 parallel 和 gunzip 解壓縮所有 .gz 檔案到目標目錄
find "$source_dir" -name "*.gz" | parallel -j 4 gunzip -c {} \> "$target_dir/{/.}"

echo "All .gz files in $source_dir have been extracted to $target_dir using parallel."