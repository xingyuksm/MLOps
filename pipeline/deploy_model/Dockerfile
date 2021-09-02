FROM python:3.9

RUN pip install fastapi uvicorn numpy scikit-learn xgboost

RUN mkdir -p /app
RUN mkdir -p /temp_storage

ADD *.py /app

EXPOSE 9090