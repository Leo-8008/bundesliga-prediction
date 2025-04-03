FROM python:3.10-slim

WORKDIR /app

COPY app/ app/
COPY model_home.pkl model_away.pkl feature_names.csv ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app/app.py"]
