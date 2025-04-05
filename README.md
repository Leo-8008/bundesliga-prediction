# bundesliga-prediction
Projekt 1 zur Vorhersage von Spielen in der Bundesliga-Meisters.
In diesem Projekt wird ein vollständiger Machine Learning Workflow zur Vorhersage von Bundesliga-Spielergebnissen umgesetzt – inklusive Scraping, Modelltraining, Deployment in Azure und ModelOps-Automatisierung. Die Vorhersage basiert auf historischen Spieldaten, Tabellenplatz, Formkurve und weiteren Features.

Datenherkunft
	• Format: HTML (Web-Scraping mit Scrapy)
	• Beschreibung: Extraktion von Bundesliga-Spielergebnissen, Datum, Tore, Tabellenplatz, Team-Form (letzte 3 Heim-/Auswärtsspiele).
	• Features:
		○ Heim-/Auswärtsteam 
		○ Heim-/Auswärtstore
		○ Tabellenplatz
		○ Teamform


Datenherkunft – URL
https://www.transfermarkt.de/bundesliga/spieltag/wettbewerb/L1

ML-Algorithmus
Linear Regression (scikit-learn)
Zwei Modelle:
	• model_home.pkl: Vorhersage Heimtore
	• model_away.pkl: Vorhersage Auswärtstore

GitHub Repository
https://github.com/Leo-8008/bundesliga-prediction

Dokumentation

Data Scraping
	• Umsetzung mit Scrapy
	• Speicherung der Ergebnisse in bundesliga_results.json
	• Automatischer Export in MongoDB (Azure Cosmos DB mit MongoDB GitHub Secret für Connection String)
	• Features: Heimteam, Auswärtsteam, Tore, Datum, Tabellenplatz, Form
 
 Automatisierung: GitHub Action run_all.yml crawlt alle Spieltage von 2019–2024

Training
	• train_model.py: trainiert zwei Regressionsmodelle (Heim- und Auswärtstore)
	• One-Hot-Encoding + numerische Features
	• Speicherung der Modelle + feature_names.csv
	• Upload in Azure Blob Storage mit Versionierung

 Automatisierung: Teil von run_all.py Workflow

ModelOps Automation
	• GitHub Actions:
		○ upload_model.yml: Upload der Modelle in Azure Blob Storage
		○ run_all.yml: Automatisiert gesamten Pipeline: Scraping → MongoDB → Training → Upload
	• Model-Versionierung in Blob Storage

Deployment
	• Flask App mit UI zur Auswahl von Heim-/Auswärtsteam
	• Ergebnisanzeige (z. B. „BVB vs. FCB – Tipp: 2:1“)
	• Styling mit Bootstrap
	• Containerisierung mit Docker (Dockerfile, .dockerignore)
	• Deployment via Azure Web App for Containers

App erreichbar unter: https://bundesliga-webapp.azurewebsites.net

