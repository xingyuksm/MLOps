# Run local test
STORAGE=$PWD/tmp
mkdir -p $STORAGE

docker build -t xingyuusa/mlops-test:amaro-preprocess ./data-preprocess
docker run --volume $STORAGE:/tmp xingyuusa/mlops-test:amaro-preprocess preprocess.py --url https://raw.githubusercontent.com/xingyuksm/MLOps/main/amaro/data/batch_01_train.csv --output_path /tmp/data.csv --hist_path /tmp/hist.png --embed_plot_path /tmp/embed.png --features_save_path /tmp/features.csv --labels_save_path /tmp/labels.csv

docker build -t xingyuusa/mlops-test:amaro-xgb ./train-xgb
docker run --volume $STORAGE:/tmp xingyuusa/mlops-test:amaro-xgb model.py --features_file_path /tmp/features.csv --labels_file_path /tmp/labels.csv --cv_results_file_path /tmp/xgb_cv_results.csv --model_file_path /tmp/xgb_model --kfp_metrics_path /tmp/kfp_metrics_xgb.json

docker build -t xingyuusa/mlops-test:amaro-rf ./train-rf
docker run --volume $STORAGE:/tmp xingyuusa/mlops-test:amaro-rf model.py --features_file_path /tmp/features.csv --labels_file_path /tmp/labels.csv --cv_results_file_path /tmp/rf_cv_results.csv --model_file_path /tmp/rf_model --kfp_metrics_path /tmp/kfp_metrics_rf.json