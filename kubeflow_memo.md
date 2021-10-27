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
