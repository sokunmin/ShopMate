import os
import vertexai
import dotenv
from google.cloud import aiplatform

dotenv.load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = "us-west1"

vertexai.init(
    project=os.getenv("GOOGLE_PROJECT_ID"),
    location="us-west1",
    staging_bucket=f"gs://{os.getenv('GOOGLE_BUCKET_NAME')}",
)

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Create an endpoint
index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    project=PROJECT_ID,
    location=LOCATION,
    display_name="endpoint-name",
    description="vertexai-search-endpoint",
    public_endpoint_enabled=True,
)

# Deploy an index to the endpoint
index = aiplatform.MatchingEngineIndex(index_name=index_endpoint.name, location=LOCATION)
deployed_index = index_endpoint.deploy_index(
    index=index,
    deployed_index_id="vertexai_deployed_index_name",
    display_name="vertexai-deployed-index-name",
    machine_type="e2-standard-2",
    min_replica_count=1,
    max_replica_count=1,
)