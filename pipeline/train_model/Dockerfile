FROM python:3.9

ENV WORKING_DIRECTORY=/app

RUN apt-get update && apt-get upgrade -y

RUN pip3 install pandas scikit-learn xgboost

WORKDIR ${WORKING_DIRECTORY}
RUN mkdir -p /temp_storage
ADD *.py ${WORKING_DIRECTORY}/

ENV PATH="${WORKING_DIRECTORY}:${PATH}"
RUN chmod +x ${WORKING_DIRECTORY}/train.py