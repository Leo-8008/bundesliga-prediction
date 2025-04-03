import subprocess
import datetime
import os
from azure.storage.blob import BlobServiceClient

# 1. Scrapy Spider ausführen
print("Starte Scraping...")
subprocess.run(["scrapy", "crawl", "bundesliga_spider"], cwd="scraping")

# 2. Form-Features hinzufügen
print("Berechne Form-Features...")
subprocess.run(["python", "add_form_features.py"])

# 3. Modelltraining
print("Trainiere Modelle...")
subprocess.run(["python", "train_model.py"])

# 4. MongoDB Import
print("Importiere Daten in MongoDB...")
subprocess.run(["python", "import_to_cosmos.py"])

# 5. Upload zu Azure Blob Storage
print("Lade Modelle in Azure Blob Storage hoch...")

AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")  # muss in .env oder GitHub Actions gesetzt sein
STORAGE_ACCOUNT_NAME = "bundesligaml4305190470"
container_name = "models"
version = datetime.datetime.now().strftime("v%Y%m%d_%H%M")

blob_service = BlobServiceClient(
    f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=AZURE_STORAGE_KEY
)

container_client = blob_service.get_container_client(container_name)
try:
    container_client.create_container()
    print(f"Container '{container_name}' erstellt")
except Exception:
    print(f"Container '{container_name}' existiert bereits")

for file in ["model_home.pkl", "model_away.pkl", "feature_names.csv"]:
    blob_path = f"{version}/{file}"
    blob_client = container_client.get_blob_client(blob_path)
    with open(file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        print(f"Hochgeladen: {blob_path}")

print("Pipeline erfolgreich abgeschlossen!")
