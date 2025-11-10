from pathlib import Path

max_recursions = 500 # set recursion limit for LLM in VALIDATOR
max_refines = 100 # set limit for REFINER; after max_refines is reached, the last version of a narrative will be automatically approved
ollama_version = "llama3.2" # set your preferred ollama model
output_dir = Path("data/results") # add your desired output directory

# settings for RETRIEVER
news_docs = 5 # set number of news documents you want to retrieve with the Chroma retriever
st_docs = 10 # set number of short documents you want to retrieve per topic with the BM_25 retriever