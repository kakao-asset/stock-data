FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY MultiStock.py .
ENV TZ Asia/Seoul

CMD ["python", "MultiStock.py"]
