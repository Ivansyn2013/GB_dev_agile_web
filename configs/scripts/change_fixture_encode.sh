#!/bin/bash
START_DIR="../../web/authapp"
SOURCE_ENCODE="UTF-16le"
TARGET_ENCODE="UTF-8"

if [ -d "$START_DIR/fixtures" ]; then
  echo "$START_DIR/fixtures is exists";
else
  cp -r "$START_DIR/fixtures" "$START_DIR/fixtures.back.d"
fi

for file in "$START_DIR"/fixtures/* ; do
  if [ -f "$file" ]; then
    file_name=$(basename "$file")
    echo "$file_name recoding..."
    iconv -f "$SOURCE_ENCODE" -t "$TARGET_ENCODE" -o $file $file
    echo "$file_name recoding succeses"
  fi
done;


