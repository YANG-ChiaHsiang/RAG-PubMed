#!/bin/bash

# 設定起始和結束檔案編號
START_FILE=1
END_FILE=1274

# 設定每次下載的檔案數量
BATCH_SIZE=100

# 設定下載目錄
LOCAL_DIR="./gz"

# 創建資料夾
mkdir -p "$LOCAL_DIR"

# 設定日誌檔案路徑
LOG_FILE="./download.log"

# 確保下載目錄存在
mkdir -p "$LOCAL_DIR"

# 函數：記錄日誌訊息
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

# 計算總批次數量
TOTAL_BATCHES=$(( (END_FILE - START_FILE + BATCH_SIZE - 1) / BATCH_SIZE ))

# 迴圈處理每個批次，並行執行
for (( batch=0; batch<TOTAL_BATCHES; batch++ )); do
  # 計算目前批次的起始和結束檔案編號
  BATCH_START=$(( START_FILE + batch * BATCH_SIZE ))
  BATCH_END=$(( BATCH_START + BATCH_SIZE - 1 ))

  # 確保批次結束檔案編號不超過總結束檔案編號
  if (( BATCH_END > END_FILE )); then
    BATCH_END=$END_FILE
  fi

  # 顯示目前批次資訊並記錄日誌
  log "Downloading files $BATCH_START to $BATCH_END..."
  echo "Downloading files $BATCH_START to $BATCH_END..."

  # 並行執行 Python 腳本下載目前批次的文件，並將輸出記錄到日誌
  (python PubMed_get.py "$BATCH_START" "$BATCH_END" --local_dir "$LOCAL_DIR" | while read line; do log "$line"; echo "$line"; done) &
done

# 等待所有背景任務完成
wait

log "All batches downloaded successfully."
echo "All batches downloaded successfully."