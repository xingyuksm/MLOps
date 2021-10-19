# Create a folder as storage
STORAGE=$PWD/temp_storage
mkdir -p $STORAGE

# Run Step 1: Data ingestion
docker run --volume $STORAGE:/temp_storage --rm xingyuusa/mlops-test:data-ingestion data_ingestion.py \
--url="https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv" \
--output_path="/temp_storage/ingested_data.csv"

# Run Step 2: Data preprocess
docker run --volume $STORAGE:/temp_storage --rm xingyuusa/mlops-test:data-preprocess data_preprocess.py \
--data_path="/temp_storage/ingested_data.csv" \
--label_col="variety" \
--x_train_path="/temp_storage/x_train.csv" \
--x_test_path="/temp_storage/X_test.csv" \
--y_train_path="/temp_storage/y_train.csv" \
--y_test_path="/temp_storage/y_test.csv" \
--label_encoder_path="/temp_storage/le.pkl "

# Run Step 3: Train model
docker run --volume $STORAGE:/temp_storage --rm xingyuusa/mlops-test:train_model train.py \
--X_train_path="/temp_storage/X_train.csv" \
--X_test_path="/temp_storage/X_test.csv" \
--y_train_path="/temp_storage/y_train.csv" \
--y_test_path="/temp_storage/y_test.csv" \
--n_estimator=2 \
--model_file_path="/temp_storage/model.pkl" \
--mlpipeline_metrics_path="/temp_storage/metrics.txt"

# Run Step 4: Deploy model
docker run \
--volume $STORAGE:/temp_storage -e MODEL_FILE_PATH="/temp_storage/model.pkl" \
-e LABEL_ENCODER_PATH="/temp_storage/le.pkl" \
-p 9090:9090 \
--rm xingyuusa/mlops-test:deploy_model \
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 9090