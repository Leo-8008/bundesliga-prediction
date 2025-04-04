import argparse
from azure.storage.blob import BlobServiceClient
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument("--container", required=True, help="models")
parser.add_argument("--version", required=True, help="latest")
args = parser.parse_args()

AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
STORAGE_ACCOUNT_NAME = "bundesligaml4305190470" 

blob_service = BlobServiceClient(
    f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=AZURE_STORAGE_KEY
)

container_client = blob_service.get_container_client(args.container)
try:
    container_client.create_container()
    print(f"Container '{args.container}' erstellt")
except Exception:
    print(f"Container '{args.container}' existiert bereits")

for model_file in ["model_home.pkl", "model_away.pkl", "feature_names.csv"]:
    blob_name = f"{args.version}/{model_file}"
    blob_client = container_client.get_blob_client(blob_name)

    with open(model_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        print(f"Hochgeladen: {blob_name}")

print("Upload abgeschlossen.")
