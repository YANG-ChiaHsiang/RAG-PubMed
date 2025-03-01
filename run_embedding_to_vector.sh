#!/bin/bash

# Default parameters
CSV_PATH="./data/pubmed_baseline/merget_2020.csv"
OUTPUT_DIR="output/2020"
BATCH_SIZE=7000 # A6000(48G) * 2 = 96G 
MULTI_GPU=true

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --csv_path) CSV_PATH="$2"; shift ;;
        --output_dir) OUTPUT_DIR="$2"; shift ;;
        --batch_size) BATCH_SIZE="$2"; shift ;;
        --multi_gpu) MULTI_GPU=true ;;
        *) echo "Unknown parameter: $1" ;;
    esac
    shift
done

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Activate Python environment if needed (uncomment and modify if using Conda or virtualenv)
# source ~/anaconda3/bin/activate myenv  # If using Conda, uncomment and replace "myenv"

# Ensure the Python script is executable
chmod +x vector_embedding/generate_faiss_embeddings.py

# Execute the Python script
python -u vector_embedding/generate_faiss_embeddings.py \
    --csv_path "$CSV_PATH" \
    --output_dir "$OUTPUT_DIR" \
    --batch_size "$BATCH_SIZE" \
    $( [ "$MULTI_GPU" = true ] && echo "--multi_gpu" )

echo "Execution completed. Results saved in $OUTPUT_DIR"