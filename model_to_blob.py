import argparse
from azure.storage.blob import BlobServiceClient
from pathlib import Path
import os
from azure.storage.blob import BlobServiceClient

# Argumente definieren (z. B. für Versionierung)
parser = argparse.ArgumentParser()
parser.add_argument("--container", type=str, required=True, help="Name des Blob Containers (z. B. 'models')")
parser.add_argument("--version", type=str, required=True, help="Modellversion (z. B. 'v1')")
args = parser.parse_args()

# Verbindung mit Azure Blob Storage
AZURE_CONNECTION_STRING = os.environ["AZURE_STORAGE_KEY"]
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(args.container)

# Hochzuladende Dateien
model_files = [
    ("model_home.pkl", f"home_{args.version}.pkl"),
    ("model_away.pkl", f"away_{args.version}.pkl"),
    ("feature_names.csv", f"features_{args.version}.csv")
]

# Upload ausführen
for local_file, blob_name in model_files:
    file_path = Path(local_file)
    if file_path.exists():
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        print(f"Hochgeladen: {local_file} → {args.container}/{blob_name}")
    else:
        print(f"Datei nicht gefunden: {local_file}")
