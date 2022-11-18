FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY MultiStock-fix.py .

CMD ["python", "MultiStock.py"]