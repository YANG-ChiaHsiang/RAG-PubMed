#!/bin/bash

# 設定起始與結束範圍
START=1
END=400
STEP=100
LOG_DIR="logs"

# 創建 logs 目錄（如果不存在）
mkdir -p $LOG_DIR

# 遍歷範圍
for ((i=$START; i<=$END; i+=$STEP))
do
    # 計算結束索引
    j=$((i + STEP - 1))

    # 確保不超過 END
    if [ $j -gt $END ]; then
        j=$END
    fi

    # 設定 log 檔案名稱
    LOG_FILE="$LOG_DIR/start_end_${i}_${j}.log"

    # 執行 Python 腳本並輸出到 log 檔案 (並行執行)
    echo "Running: python vector_embedding_start_end.py --start $i --end $j --output_dir output/ | tee $LOG_FILE"
    python vector_embedding_start_end.py --start $i --end $j --output_dir output/ | tee $LOG_FILE &  # 加上 '&' 讓它並行執行
done

# 等待所有後台進程完成
wait
echo "All tasks completed!"