FROM python:3.9

ENV WORKING_DIRECTORY=/app

RUN apt-get update && apt-get upgrade -y

RUN pip3 install requests pandas scikit-learn spacy matplotlib
RUN python -m spacy download en_core_web_lg

WORKDIR ${WORKING_DIRECTORY}
ADD *.py ${WORKING_DIRECTORY}/

ENV PATH="${WORKING_DIRECTORY}:${PATH}"
RUN chmod +x ${WORKING_DIRECTORY}/*.py