#!/bin/bash

# Set the directory containing .gz files to be extracted
source_dir="./gz"

# Set the target directory for extracted files
target_dir="./xml"

# Ensure target directory exists, create if not
mkdir -p "$target_dir"

# Use parallel and gunzip to extract all .gz files to target directory
find "$source_dir" -name "*.gz" | parallel -j 4 gunzip -c {} \> "$target_dir/{/.}"

echo "All .gz files in $source_dir have been extracted to $target_dir using parallel."
