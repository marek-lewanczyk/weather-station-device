#!/bin/bash

# Nazwa pliku wynikowego
OUTPUT_FILE="project.zip"

# Zipowanie całego projektu
zip -r "$OUTPUT_FILE" . -x "*.git*" "__pycache__/*" "*.DS_Store"

# Informacja o zakończeniu
echo "Projekt został spakowany do: $OUTPUT_FILE"