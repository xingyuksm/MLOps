FROM python:3.9

RUN pip install fastapi uvicorn numpy scikit-learn xgboost

RUN mkdir -p /app
RUN mkdir -p /temp_storage

ENV MODEL_FILE_PATH=/temp_storage/model.pkl
ENV LABEL_ENCODER_PATH=/temp_storage/le

COPY /model/model.pkl /temp_storage/
COPY /model/le  /temp_storage/

ADD *.py /app

EXPOSE 9090

CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "9090"]