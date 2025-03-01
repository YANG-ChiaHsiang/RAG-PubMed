#!/bin/bash

# Set the start and end file numbers
START_FILE=1
END_FILE=1274

# Set the number of files to download per batch
BATCH_SIZE=100

# Set the download directory
LOCAL_DIR="./gz"

# Create the directory
mkdir -p "$LOCAL_DIR"

# Set the log file path
LOG_FILE="./download.log"

# Ensure the download directory exists
mkdir -p "$LOCAL_DIR"

# Function: log messages
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG_FILE"
}

# Calculate the total number of batches
TOTAL_BATCHES=$(( (END_FILE - START_FILE + BATCH_SIZE - 1) / BATCH_SIZE ))

# Loop through each batch and execute in parallel
for (( batch=0; batch<TOTAL_BATCHES; batch++ )); do
  # Calculate the start and end file numbers for the current batch
  BATCH_START=$(( START_FILE + batch * BATCH_SIZE ))
  BATCH_END=$(( BATCH_START + BATCH_SIZE - 1 ))

  # Ensure the batch end file number does not exceed the total end file number
  if (( BATCH_END > END_FILE )); then
    BATCH_END=$END_FILE
  fi

  # Display current batch information and log it
  log "Downloading files $BATCH_START to $BATCH_END..."
  echo "Downloading files $BATCH_START to $BATCH_END..."

  # Execute the Python script to download the current batch of files in parallel, and log the output
  (python PubMed_get.py "$BATCH_START" "$BATCH_END" --local_dir "$LOCAL_DIR" | while read line; do log "$line"; echo "$line"; done) &
done

# Wait for all background tasks to complete
wait

log "All batches downloaded successfully."
