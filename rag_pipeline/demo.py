# import libraries (most libraries are imported in the dedicated .py files in rag_pipeline folder)
from pipeline_functions import run_narrative_extraction
from pipeline_functions import config
from utils import load_json_documents
from settings import ollama_version
from settings import output_dir
from settings import news_docs
from settings import st_docs

import json
import pandas as pd
import subprocess
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

# pull Ollama; ADJUST LLM HERE
subprocess.run(["ollama", "pull", ollama_version], check=True)

# add paths
REPO_PATH = Path("/content/NTLRAG")
CSV_PATH = Path("data/testdata_seedtopics.csv")  # csv file with document text and topic number
KEYW_PATH = Path("data/testdata_topic_keywords.json")  # json file with topic keywords
NEWS_PATH = Path("data/testdata_news.json")  # json file with news data
OUTPUT_DIR = output_dir # output directory for the narratives, adjust to yours
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) #create new folder if necessary

# load topic model output file
df = pd.read_csv(CSV_PATH)

# load topic keywords
with open(KEYW_PATH, "r") as f:
    topic_keywords = json.load(f)

# ADJUST EMBEDDING MODEL HERE
embedding_model = OllamaEmbeddings(
    model=ollama_version,
)

# ADJUST RETRIEVER HERE
chroma = Chroma(
    embedding_function=embedding_model
)

docs = load_json_documents(NEWS_PATH, content_key="description")

# add news documents to chroma vector storage; ADJUST RETRIEVER HERE
chroma.add_documents(docs)

# build chroma retriever; ADJUST RETRIEVER HERE
chroma_retriever = chroma.as_retriever(search_kwargs={"k": news_docs})

# build bm25 retriever dict; ADJUST RETRIEVER HERE
bm25_retrievers = {}

# make sure topic values are integers or strings, depending on your JSON keys
df['Topic'] = df['Topic'].astype(str)

# loop over each topic to create a BM25 retriever
for topic_id in df['Topic'].unique():
    topic_docs = df[df['Topic'] == topic_id]

    # convert to LangChain Document objects
    documents = [
        Document(
            page_content=row['Document'],
            metadata={"topic": topic_id}
        )
        for _, row in topic_docs.iterrows()
    ]

    # build BM25Retriever for this topic; ADJUST RETRIEVER HERE
    retriever = BM25Retriever.from_documents(documents)
    retriever.k = st_docs

    # add to dictionary; ADJUST RETRIEVER HERE
    bm25_retrievers[topic_id] = retriever


# run narrative extraction
all_approved_narratives, topic_results = run_narrative_extraction(
    topic_keywords=topic_keywords,
    bm25_retrievers=bm25_retrievers,
    chroma_retriever=chroma_retriever,
    output_dir=OUTPUT_DIR,
    config=config
)

# the print provides NTLRAG results including chain-of-thought answers by the LLM for the sample dataset
print(f"Total approved narratives: {len(all_approved_narratives)}")


