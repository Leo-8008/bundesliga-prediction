from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

subscription_id = "763385d7-e323-4a29-bb0d-4101d0381259"
resource_group = "bundesliga-rg"
workspace_name = "bundesliga-ml"

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id,
    resource_group,
    workspace_name
)

# Alle Versionen auflisten
models = ml_client.models.list(name="bundesliga-home-model")
for model in models:
    print(f"{model.name} - Version: {model.version} - Pfad: {model.path}")

models = ml_client.models.list(name="bundesliga-away-model")
for model in models:
    print(f"{model.name} - Version: {model.version} - Pfad: {model.path}")