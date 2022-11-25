FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY Member_trend.py .
ENV TZ Asia/Seoul

CMD ["python", "Member_trend.py"]
