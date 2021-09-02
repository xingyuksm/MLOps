# Create a folder as storage
STORAGE=$PWD/temp_storage
mkdir -p $STORAGE

# Run Step 1: Data ingestion
docker run --volume $STORAGE:/temp_storage --rm mlops-data-ingestion/latest data_ingestion.py \
--url="https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv" \
--output_path="/temp_storage/ingested_data.csv"

# Run Step 2: Data preprocess
docker run --volume $STORAGE:/temp_storage --rm mlops-data-preprocess/latest data_preprocess.py \
--data_path="/temp_storage/ingested_data.csv" \
--label_col="variety" \
--output_path="/temp_storage"

# Run Step 3: Train model
docker run --volume $STORAGE:/temp_storage --rm mlops-train-model/latest train.py \
--X_train_path="/temp_storage/X_train.csv" \
--X_test_path="/temp_storage/X_test.csv" \
--y_train_path="/temp_storage/y_train.csv" \
--y_test_path="/temp_storage/y_test.csv" \
--n_estimator=2 \
--output_path="/temp_storage"

# Run Step 4: Deploy model
docker run \
--volume $STORAGE:/temp_storage -e MODEL_FILE_PATH="/temp_storage/xgb.pkl" \
-e LABEL_ENCODER_PATH="/temp_storage/le.pkl" \
-p 9090:9090 \
--rm mlops-deploy-model/latest \
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 9090