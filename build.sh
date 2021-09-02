# Build data ingestion image
docker build -t mlops-data-ingestion/latest ./pipeline/data_ingestion

# Build data preprocess image
docker build -t mlops-data-preprocess/latest ./pipeline/data_preprocess

# Build train model image
docker build -t mlops-train-model/latest ./pipeline/train_model

# Build model deploy image
docker build -t mlops-deploy-model/latest ./pipeline/deploy_model

# Show all images
docker image ls