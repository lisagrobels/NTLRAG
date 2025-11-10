#!/bin/bash
set -e

echo "=== Installing Python dependencies ==="
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "=== Setup complete! ==="
echo "⚙️  Note: Please install your preferred EXTRACTOR/VALIDATOR/REFINER component separately. If you choose Ollama LLM, follow the instructions in the README."
