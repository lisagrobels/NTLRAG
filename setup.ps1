Write-Host "=== Installing Python dependencies ==="
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Write-Host "=== Setup complete! ==="
Write-Host "⚙️  Note: Please install your preferred EXTRACTOR/VALIDATOR/REFINER component separately. If you choose Ollama LLM, follow the instructions in the README."