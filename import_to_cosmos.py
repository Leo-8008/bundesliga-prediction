import json
from pymongo import MongoClient

# Deinen Connection String hier einfügen (mit Passwort!)
CONNECTION_STRING = "mongodb+srv://mdmleodb:Test1234!@bundesliga-db.mongocluster.cosmos.azure.com/?tls=true&retrywrites=false&maxIdleTimeMS=120000&authMechanism=SCRAM-SHA-256"

# Verbindung aufbauen
client = MongoClient(CONNECTION_STRING)

# Datenbank und Collection anlegen
db = client["bundesliga"]
collection = db["results"]

# Lokale JSON-Datei laden
with open("bundesliga_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Daten einfügen (mehrfache Arrays -> flatten falls nötig)
if isinstance(data, list):
    collection.insert_many(data)
elif isinstance(data, dict):
    collection.insert_one(data)
else:
    print("Unerwartetes Datenformat")

print("Daten erfolgreich nach Cosmos DB importiert!")
