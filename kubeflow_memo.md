# Kubeflow Adpatation Memo

Author: Xing Yu
Date: Oct 22, 2021

## Resource Requirements
1. A Kubernetes cluster with [Kubeflow Pipeline](https://www.kubeflow.org/docs/components/pipelines/overview/pipelines-overview/) deployment.  
2. An image registry for storing containerized applications (e.g., Docker hub). The Kubernetes cluster should have access to the image registry.
3. A code repository for storing pipeline files and/or pipeline components.
4. Deployment frameworks such as [Kserve](https://github.com/kubeflow/kfserving) and [Seldon](https://www.seldon.io).

## Prerequisites of using Kubeflow pipelines.

### For System Admin
1. The admin should have knowledge of [Kubernetes](https://kubernetes.io) on the choosen Cloud Environment and feel comfortable to create and deploy [CRD](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
2. The admin should be familiar with setting up and configuring an image registry and an code repository beside the Kubernetes cluster, especially when working in a private environment.

### For Users Who Want to Build Pipeline Components
1. Knowledge of how to containerize applications using [Docker](https://docs.docker.com/get-started/).
2. Knowledge of working with an image registry such as [Docker Hub](https://hub.docker.com).
3. Comfortable with writing [YAML](https://en.wikipedia.org/wiki/YAML) files.
4. Basic understanding of [Kubectl](https://kubernetes.io/docs/tasks/tools/).
5. Skills of using code repositories such as GitHub.

### For Users Who Want to Build Kubeflow Pipelines
1. Comfortable with python programming and using a shell.
2. Learn the basic concepts of pipeline and components.
3. Learn to build a pipeline use python [DSL](https://www.kubeflow.org/docs/components/pipelines/sdk/sdk-overview/).

## Example of Building a Kubeflow Component
Three steps are needed to created a custom pipeline component. First, write the program. Second, containerize the program to an independent application. And third, create a yaml file to provide component specifications.

### Step 1: Create the program

An component should be program to perform a task. When designing a component, it is a good practice to make it stateless and reusable. We are providing an example of ingesting data by an URL below in Python. Note that we are going to containerize the program so it is not necessary to use a specified programming language. This is just for demo.

```python
def data_ingestion(url, output_path):
    '''The function fetches data by given URL.
    
    '''
    
    p = pathlib.Path(output_path)
    if p.exists():
        logger.warning('Output file already exists.')
        with open(output_path, 'r') as f:
            ret = f.read()
    else:
        p.parent.absolute().mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            r = requests.get(url)
            f.write(r.text)
            ret = r.text

    logger.info(ret[:100])
    return ret
```

Instead of implementing this function in a notebook, we save this function as a python script and specify the command line arguments as inputs.

### Step 2: Containerize the Application

We create a Dockerfile to turn this script into a containerized application.

```Dockerfile
FROM python:3.9

ENV WORKING_DIRECTORY=/app

RUN apt-get update && apt-get upgrade -y

RUN pip3 install requests 

WORKDIR ${WORKING_DIRECTORY}
RUN mkdir -p /temp_storage
ADD *.py ${WORKING_DIRECTORY}/

ENV PATH="${WORKING_DIRECTORY}:${PATH}"
RUN chmod +x ${WORKING_DIRECTORY}/data_ingestion.py
```

With this Dockerfile, we can build an image and push it to a container registry.
```bash
docker build -t xingyuusa/mlops-test:data-ingestion ./pipeline/data_ingestion
# this image is pushed to Docker hub, which is just one of the options.
docker push xingyuusa/mlops-test:data-ingestion
```

It is a good practice to test the containerized application locally first for debugging.

### Step 3: Create Component Specifications

Once a application is containerized, we need to create a YAML file to describe the component's meta data, interface, and implementation.

```yaml
name: Data Ingestion
description: Ingest data by input url.

inputs:
- {name: url, type: String, description: 'The URL to ingest the Iris data from'}

outputs:
- {name: data, type: String, description: 'Ingested CSV file'}

implementation:
  container:
    image: xingyuusa/mlops-test:data-ingestion
    command: [
      data_ingestion.py,
      --url, {inputValue: url},
      --output_path, {outputPath: data}
    ]
```

In this example, we create a YAML file that has three parts.

1. In the meta data section, we specify the name of the component and describe it.
2. In the interface section, we specify the inputs and outputs parameters and their types(optional).
3. In the implementation section, we specify the container. Note that the image name is the same as the URI to the image registry.

It is worth noting that, by specifying the inputs and outputs, Kubeflow pipelinne will track the inputs and outputs as [artifacts](https://www.kubeflow.org/docs/components/pipelines/overview/concepts/output-artifact/) in the Kubeflow pipeline UI.

Now we have a component that is ready to be used in any pipelines. Please refer to the official [document](https://www.kubeflow.org/docs/components/pipelines/sdk/component-development/) for more information.
