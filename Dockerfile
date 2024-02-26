# import de python
FROM python:3.9-slim

WORKDIR /app

# COPY . /churn_finance_g2

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./app/app.py" ]

