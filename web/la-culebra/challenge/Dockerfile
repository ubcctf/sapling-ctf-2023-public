FROM python:3.9-alpine

WORKDIR /app/culebra

ENV FLASK_APP=app.py

ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_RUN_PORT=9090

# Uncomment to run in dev mode
#ENV FLASK_ENV=development

COPY flag.txt flag.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 9090
COPY . .
CMD ["flask", "run"]