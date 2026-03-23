# Install the Vertex AI SDK
! pip3 install --upgrade --quiet google-cloud-aiplatform

from google.cloud import aiplatform
from datetime import datetime
from google.cloud import storage
from google.cloud import bigquery


project_id = "cloud-deployment-agent"  # @param {type:"string"}
region = "us-central1"  # @param {type: "string"}

bucket_name = "agent-bucket"  # @param {type:"string"}
bucket_uri = f"gs://{bucket_name}"


timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

if bucket_name == "" or bucket_name is None or bucket_name == "agent-bucket":
    bucket_name = project_id + "aip-" + timestamp
    bucket_uri = "gs://" + bucket_name
! echo $bucket_uri


client = storage.Client(project=project_id)

# Create a bucket
bucket = client.create_bucket(bucket_name, location=region)
print("Bucket {} created.".format(bucket.name))


# Initialize the Vertex AI SDK
aiplatform.init(project=project_id, location=region, staging_bucket=bucket_uri)


# Set up BigQuery client
bq_client = bigquery.Client(project=project_id)
