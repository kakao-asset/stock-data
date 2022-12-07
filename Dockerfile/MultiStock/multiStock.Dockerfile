FROM python:3.9.0-slim

COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY MultiStockRetrySchedule.py .
ENV TZ Asia/Seoul

# crontab
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    cron \
    vim

# Copy cron file to the cron.d directory on container
COPY cron /etc/cron.d/cron
# Give execution access
RUN chmod 0755 /etc/cron.d/cron
# Run cron job on cron file
RUN crontab /etc/cron.d/cron
# Create the log file
RUN touch /var/log/cron.log

CMD ["python", "MultiStockRetrySchedule.py"]
