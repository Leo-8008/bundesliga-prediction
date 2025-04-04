import json
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://mdmleodb:Test1234!@bundesliga-db.mongocluster.cosmos.azure.com/?tls=true&retrywrites=false&maxIdleTimeMS=120000&authMechanism=SCRAM-SHA-256"

client = MongoClient(CONNECTION_STRING)

db = client["bundesliga"]
collection = db["results"]

collection.delete_many({})  

with open("bundesliga_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(data[0].keys())

if isinstance(data, list):
    collection.insert_many(data)
elif isinstance(data, dict):
    collection.insert_one(data)
else:
    print("Unerwartetes Datenformat")

print("Daten erfolgreich aktualisiert und in Cosmos DB gespeichert!")
