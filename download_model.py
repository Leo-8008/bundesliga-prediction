import argparse
from azure.storage.blob import BlobServiceClient
from pathlib import Path
import os
from azure.storage.blob import BlobServiceClient

# Argumente für Container und Version
parser = argparse.ArgumentParser()
parser.add_argument("--container", type=str, required=True, help="Name des Blob Containers (z. B. 'models')")
parser.add_argument("--version", type=str, required=True, help="Modellversion (z. B. 'v1')")
args = parser.parse_args()

# Azure Blob Storage Connection String
AZURE_CONNECTION_STRING = os.environ["AZURE_STORAGE_KEY"]
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(args.container)

# Dateien, die heruntergeladen werden sollen
files_to_download = {
    f"home_{args.version}.pkl": "model_home.pkl",
    f"away_{args.version}.pkl": "model_away.pkl",
    f"features_{args.version}.csv": "feature_names.csv"
}

# Download durchführen
for blob_name, local_file in files_to_download.items():
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(local_file, "wb") as f:
            f.write(blob_client.download_blob().readall())
        print(f"Heruntergeladen: {blob_name} → {local_file}")
    except Exception as e:
        print(f"Fehler beim Herunterladen von {blob_name}: {e}")
