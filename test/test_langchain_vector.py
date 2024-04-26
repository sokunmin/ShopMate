import os
import sys
import pathlib
import textwrap
import json
import warnings
import pandas as pd
import subprocess
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import google.generativeai as genai
from google.cloud import aiplatform, storage
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores.matching_engine import MatchingEngine
from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vertexai.preview.generative_models import GenerativeModel
from langchain.vectorstores.matching_engine import MatchingEngine

# filter warnings for unused libs
warnings.filterwarnings('ignore')

# key_name = !gcloud services api-keys list --filter="gemini-api-key" --format="value(name)"
# key_name = key_name[0]

# api_key = !gcloud services api-keys get-key-string $key_name --location="us-central1" --format="value(keyString)"
# api_key = api_key[0]


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Define project information
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
REGION = "us-west1"

# Set environment vars
BUCKET = f"gs://{PROJECT_ID}/embeddings"
DIMENSIONS = 768
DISPLAY_NAME = 'vertex_docs_qa'
ENDPOINT = f"{REGION}-aiplatform.googleapis.com"
TEXT_GENERATION_MODEL = 'gemini-pro'
SITEMAP = 'https://docs.anthropic.com/sitemap.xml'

print(f"Your project ID is: {PROJECT_ID}")

aiplatform.init(project=PROJECT_ID, location=REGION)


# Create Documents from Vertex AI Cloud Documentation Site¶
# Load and parse sitemap.xml
# Parse the xml of sitemap and get URLs of doc site

def parse_sitemap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    urls = [element.text for element in soup.find_all("loc")]
    return urls


sites = parse_sitemap(SITEMAP)
# Use this to filter out docs that don't have a corresponding reference page
sites_filtered = [url for url in sites if 'readme.io' not in url]
print(len(sites_filtered))

# Load documentation pages using the LangChain UnstructuredURLLoader
# This step will take a few minutes to complete
# you will see download messages below the cell after execution
loader = UnstructuredURLLoader(urls=sites_filtered)
documents = loader.load()

result = documents[10].page_content + "\n\nSource: " + documents[10].metadata["source"]
print(result)
print(len(documents))

# Create Document chunks
# recursively loop through the text and create document chunks for embedding

text_splitter = RecursiveCharacterTextSplitter(
    # separator = "\n",
    chunk_size=2000,
    chunk_overlap=100)

document_chunks = text_splitter.split_documents(documents)

print(f"Number documents {len(documents)}")
print(f"Number chunks {len(document_chunks)}")

document_chunks = [f"content: {chunk.page_content}, source: {chunk.metadata['source']}" for chunk in document_chunks]

# Generate embeddings from Document chunks¶

# !rm -rf ./documents
# !mkdir ./documents

# Run this cell to generate the embeddings files you will later upload to Cloud Storage
df = pd.DataFrame(document_chunks, columns =['text'])

index_embeddings = []
model = "models/embedding-001"

for index, doc in tqdm(df.iterrows(), total=len(df), position=0):
    response = genai.embed_content(model=model, content=doc['text'], task_type="retrieval_query")

    doc_id = f"{index}.txt"
    embedding_dict = {
        "id": doc_id,
        "embedding": response["embedding"],
    }
    index_embeddings.append(json.dumps(embedding_dict) + "\n")

    with open(f"documents/{doc_id}", "w") as document:
        document.write(doc['text'])

with open("embeddings.json", "w") as f:
    f.writelines(index_embeddings)


source_file = 'embeddings.json'
destination_blob_name = 'embeddings/embeddings.json' # Adjust if needed

client = storage.Client(project=PROJECT_ID)
bucket = client.bucket(PROJECT_ID)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file)


# Upload the embedding files to Cloud Storage
# This step will take a few minutes to complete
gsutil_command = f"gsutil -q cp -r './documents' gs://{PROJECT_ID}/documents"

subprocess.run(['gsutil', '-q', 'cp', '-r', './documents', f'gs://{PROJECT_ID}/documents'])

# Create a Vertex AI Vector Store index
# Create the Vertex AI Vector Search index
# This step will take several minutes to complete
# Wait for this cell to complete before proceeding
index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
      display_name="vertex_docs",
      contents_delta_uri=f"gs://{PROJECT_ID}/embeddings",
      dimensions=768,
      approximate_neighbors_count=150,
      distance_measure_type="DOT_PRODUCT_DISTANCE"
)

index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="vertex_docs",
    description="Embeddings for the Vertex AI documentation site.",
    public_endpoint_enabled=True,
)

# This step will take up to 20 minutes to complete
# You can view the deployment in the Vertex AI console on the "Vector Search" tab
# Wait for this cell to complete before proceeding
index_endpoint = index_endpoint.deploy_index(
    index=index, deployed_index_id="vertex_index_deployment"
)

INDEX_RESOURCE_NAME=index.resource_name
index = aiplatform.MatchingEngineIndex(index_name=INDEX_RESOURCE_NAME)

deployed_index = index.deployed_indexes

# Search Vector Store, add result as context to a query (without using a LangChain Chain)
# In the next cells you will query the model directly using the Vertex AI python SDK
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def search_vector_store(question):
    vector_store = MatchingEngine.from_components(
        index_id=INDEX_RESOURCE_NAME,
        region=REGION,
        embedding=embeddings,
        project_id=PROJECT_ID,
        endpoint_id=deployed_index[0].index_endpoint,
        gcs_bucket_name=f"{PROJECT_ID}")

    relevant_documentation = vector_store.similarity_search(question, k=8)
    context = "\n".join([doc.page_content for doc in relevant_documentation])[:10000]
    return str(context)

def ask_question(question):
    context = search_vector_store(question)

    prompt=f"""
        Follow exactly those 3 steps:
        1. Read the context below and aggregrate this data
        Context : {context}
        2. Answer the question using only this context
        3. Show the source for your answers
        User Question: {question}


        If you don't have any context and are unsure of the answer, reply that you don't know about this topic.
        """

    model = GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return f"Question: \n{question} \n\n Response: \n {response.text}"

print(ask_question("How do I reduce prompt leaks?"))
print(ask_question("What use cases and capabilities does Anthropic support?"))

# Create Retrieval Augmentation Generation application using LangChain

# To answer questions and chain together the prompt, vector search, returned context and model input use a LangChain "Chain"
# In this case you will use the RetrievalQA chain which is commonly used for Question/Answering applications

# initialize model using chat
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.0, convert_system_message_to_human=True)

template = """
    Follow exactly those 3 steps:
    1. Read the context below and aggregate this data
    Context : {context}

    2. Answer the question using only this context
    3. Show the source for your answers
    User Question: {question}

    If you don't have any context and are unsure of the answer, reply that you don't know about this topic.
    """

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

vector_store = MatchingEngine.from_components(
    index_id=INDEX_RESOURCE_NAME,
    region=REGION,
    embedding=embeddings,
    project_id=PROJECT_ID,
    endpoint_id=deployed_index[0].index_endpoint,
    gcs_bucket_name=f"{PROJECT_ID}"
)

retriever = vector_store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 1}
)

# Test the retriever with a simple search performed above
result = retriever.get_relevant_documents("How do I use Anthropic in Vertex AI?")[0].page_content
print(result)

chain_type_kwargs = {"prompt": prompt}
qa = RetrievalQA.from_chain_type(
    llm=model,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs=chain_type_kwargs,
    return_source_documents=True
)


def ask_question(question: str):
    response = qa({"query": question})

    # since k is set to 1 only return the first source retrieved
    source = response['source_documents']

    return f"Response: \n\n {response['result']}"


# Note: You will see a library warning when running this step
result = ask_question("How do I use Anthropic in Vertex AI?")

print(result)