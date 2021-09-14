# Build data ingestion image
# docker build -t mlops-data-ingestion/latest ./pipeline/data_ingestion
docker build -t xingyuusa/mlops-test:data-ingestion ./pipeline/data_ingestion
docker push xingyuusa/mlops-test:data-ingestion

# Build data preprocess image
# docker build -t mlops-data-preprocess/latest ./pipeline/data_preprocess
docker build -t xingyuusa/mlops-test:data-preprocess ./pipeline/data_preprocess
docker push xingyuusa/mlops-test:data-preprocess

# Build train model image
# docker build -t mlops-train-model/latest ./pipeline/train_model
docker build -t xingyuusa/mlops-test:train_model ./pipeline/train_model
docker push xingyuusa/mlops-test:train_model

# Build model deploy image
# docker build -t mlops-deploy-model/latest ./pipeline/deploy_model
docker build -t xingyuusa/mlops-test:deploy_model ./pipeline/deploy_model
docker push xingyuusa/mlops-test:deploy_model

# Show all images
docker image ls