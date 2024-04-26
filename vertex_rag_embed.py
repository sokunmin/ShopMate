import json
import os
import dotenv
import uuid
import vertexai
from os.path import dirname
from google.cloud import storage
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_google_vertexai import VertexAIEmbeddings
from chains.loader import NewCSVLoader

dotenv.load_dotenv()

script_dir = dirname(dirname(os.path.abspath(__file__)))
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = "us-west1"
GCS_BUCKET_NAME = os.getenv("GOOGLE_BUCKET_NAME")
MODEL_NAME = "textembedding-gecko-multilingual"


def authenticate_implicit_with_adc(project_id):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


def upload_file_to_gcs(project_id, bucket_name, source_file_path, destination_blob_name):
    """A function to upload a local file to Google Cloud Storage"""

    # Google Cloud Storage initialization
    storage_client = storage.Client(project=project_id)

    # Retrieve the specified bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a new blob
    blob = bucket.blob(destination_blob_name)

    # Upload local file
    blob.upload_from_filename(source_file_path)

    print(
        f"File {source_file_path} uploaded to {bucket_name}/{destination_blob_name}"
    )


authenticate_implicit_with_adc(PROJECT_ID)
vertexai.init(
    project=os.getenv("GOOGLE_PROJECT_ID"),
    location="us-west1",
    staging_bucket=f"gs://{os.getenv('GOOGLE_BUCKET_NAME')}",
)

files = ["coupons.csv", "credit_cards.csv", "products.csv"]
embeddings = VertexAIEmbeddings(model_name=MODEL_NAME)

for f in files:
    name = f.split(".")[0]
    loader = NewCSVLoader(
        file_path=os.path.join(script_dir, "data", f),
        csv_args={"delimiter": ","},
        encoding="utf-8"
    )
    docs = loader.load()

    vectors = embeddings.embed_documents([d.page_content for d in docs])

    vector_json = []
    for v in vectors:
        vector_json.append({
            "id": str(uuid.uuid4()),
            "embedding": v
        })

    json_file_name = f"index_{name}_vectors.json"
    file_path = f"{script_dir}/data/{json_file_name}"
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(vector_json, f)

    upload_file_to_gcs(PROJECT_ID, GCS_BUCKET_NAME, file_path, json_file_name)
