FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY StockListAPI.py .

CMD ["python", "StockListAPI.py"]