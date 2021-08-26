# Resultant MLOps Initiative

Author: Prudhvinath Dittakavi, Xing Yu
Date: Aug 26, 2021

## 0. What is this document for?  
This document tries to figure out how to carry out MLOps at Resultant. By adopting proper MLOps methods, there are several foreseeable benefits.   
* First, the workflows of conducting ML/DL experiments are more repeatable and less platform dependent. 
* Second, ML/DL/DS code can be transformed into components, which can be easily reused to improve efficiency across project. 
* Third, with CI/CD and continuous training provided by MLOps framework, the DevOps process of data science solutions will be faster and less prone to outage.

Note: This document is currently a draft that everything is subject to change.

## 1. How does MLOps work?
This section provides a general description of how MLOps work based on [Kubeflow Pipeline](https://www.kubeflow.org/docs/components/pipelines/overview/pipelines-overview/). 

Typically, there are the following steps when building a data science product.
* Data ingestion and preprocessing.
* Feature engineering and feature selection.
* Training and evaluation of ML/DL model(s).
* Deploying saved model for inference.

While all the steps can be coded in a notebook and run locally or on a server. A more generalizable way to do it would include the following steps:
* Carefully analyze and separate different steps to form a good pipeline.
* Code and containerize each step as a component for the pipeline.
* Make components reusable if possible.
* Define the pipeline using an orchestrator specific way and run the pipeline on a cloud or a hybrid of cloud.

Kubeflow is one of the orchestrator that allows users to create Kubeflow pipelines to execute ML experiments and deploy models on clouds that support Kubernete clusters. 

## 2. What is provided in this repo?
The repository provides the following for facilitating MLOps adoption:
* Code examples of how to create and containerize components.
* Code examples of how to create a Kubeflow pipeline based on multiple components.
* Guidelines of how to create and organize reusable components.
* A demo of how to do feature comparison experiment.
* A demo of how to do model comparison experiment.
* Reusable components from previous projects(TBD, maybe another repo is better).

## 3. TODOs and open questions.
* Add the code examples, demos, and guidelines.
* Finish the documents.
* Is Kubeflow pipeline a good start point? What other similar tools(e.g. Airflow) should we add guidelines for in the future?
* Will the demos/code examples be enough for the DS team members to understand and adopt the standard? How many are comfortable with containerization such as using Docker? The learning of containerization and pipeline specific API is not a trivial task. How to mitigate that?
* Our infrastructure needs include at least a cloud with container registry and Kubernete cluster. Will the cost be a problem?
* The extra work incurred by creating components and pipeline is not trivial. How can that effort be reduced so the standard can be adopted for more project?

