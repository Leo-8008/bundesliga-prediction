from azure.storage.blob import BlobServiceClient
import os
import re

STORAGE_ACCOUNT_NAME = "bundesligaml4305190470"
CONTAINER_NAME = "models"
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY") 

blob_service = BlobServiceClient(
    f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=AZURE_STORAGE_KEY
)

container = blob_service.get_container_client(CONTAINER_NAME)

blobs = list(container.list_blobs())

versions = sorted(set(
    re.match(r"v\d+", blob.name).group()
    for blob in blobs if re.match(r"v\d+/", blob.name)
), reverse=True)

if not versions:
    raise ValueError("Keine Modellversionen gefunden!")

latest_version = versions[0]
print(f"Neueste Version: {latest_version}")


for filename in ["model_home.pkl", "model_away.pkl", "feature_names.csv"]:
    blob_path = f"{latest_version}/{filename}"
    blob_client = container.get_blob_client(blob_path)

    with open(filename, "wb") as f:
        f.write(blob_client.download_blob().readall())
        print(f"Heruntergeladen: {filename}")
