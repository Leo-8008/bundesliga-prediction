from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from pathlib import Path

# Azure-Konfiguration
subscription_id = "763385d7-e323-4a29-bb0d-4101d0381259"
resource_group = "bundesliga-rg"
workspace_name = "bundesliga-ml"

# Authentifizieren & Client erstellen
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id,
    resource_group,
    workspace_name
)

# Modellregistrierung: Heimtore
model_home = Model(
    path=Path("model_home.pkl"),
    name="bundesliga-home-model",
    description="Regressionsmodell Heimtore",
    type="custom_model"
)
registered_home = ml_client.models.create_or_update(model_home)
print(f"Heimtor-Modell registriert: {registered_home.name} v{registered_home.version}")

# Modellregistrierung: Auswärtstore
model_away = Model(
    path=Path("model_away.pkl"),
    name="bundesliga-away-model",
    description="Regressionsmodell Auswärtstore",
    type="custom_model"
)
registered_away = ml_client.models.create_or_update(model_away)
print(f"Auswärtstor-Modell registriert: {registered_away.name} v{registered_away.version}")
