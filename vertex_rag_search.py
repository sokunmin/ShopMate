import os
from os.path import dirname

from google.cloud import aiplatform
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import MatchingEngine

from chains.loader import NewCSVLoader

script_dir = dirname(dirname(os.path.abspath(__file__)))
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = "us-west1"
INDEX_ID = os.getenv("INDEX_ID")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")
GCS_BUCKET_NAME = f"gs://{os.getenv('GOOGLE_BUCKET_NAME')}"
MODEL_NAME = "textembedding-gecko-multilingual"

files = ["coupons.csv", "credit_cards.csv", "products.csv"]

for f in files:
    name = f.split(".")[0]
    loader = NewCSVLoader(
            file_path=os.path.join(script_dir, "data", f),
            csv_args={"delimiter": ","},
            encoding="utf-8"
        )

    documents = loader.load()

    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    vector_store = MatchingEngine.from_components(
        embedding=VertexAIEmbeddings(model_name=MODEL_NAME),
        project_id=PROJECT_ID,
        region=LOCATION,
        gcs_bucket_name=GCS_BUCKET_NAME,
        index_id=INDEX_ID,
        endpoint_id=ENDPOINT_ID,
    )

    vector_store.add_documents(documents)