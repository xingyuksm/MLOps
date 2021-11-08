# Build and push images
docker build -t xingyuusa/mlops-test:amaro-preprocess ./data-preprocess
docker build -t xingyuusa/mlops-test:amaro-xgb ./train-xgb
docker build -t xingyuusa/mlops-test:amaro-rf ./train-rf

docker push xingyuusa/mlops-test:amaro-preprocess
docker push xingyuusa/mlops-test:amaro-xgb
docker push xingyuusa/mlops-test:amaro-rf
