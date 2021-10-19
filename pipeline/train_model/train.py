#!/usr/bin/env python3
import json
import pickle
import pathlib
import pandas as pd
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
import xgboost as xgb
import argparse
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s : %(lineno)d] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model(X_train_path, X_test_path, y_train_path, y_test_path, 
                n_estimator,
                model_file_path, mlpipeline_metrics_path):
    '''Train and evaluate the model.
    
    '''
    
    X_train = pd.read_csv(X_train_path)
    X_test = pd.read_csv(X_test_path)
    y_train = pd.read_csv(y_train_path)
    y_test = pd.read_csv(y_test_path)
    
    xgb_model = xgb.XGBClassifier(objective="multi:softprob", 
                                  eval_metric='mlogloss',
                                  random_state=42,
                                  n_estimators=n_estimator,
                                  use_label_encoder=True
                                 )
    xgb_model.fit(X_train, y_train)

    y_pred = xgb_model.predict(X_test)
    
    logger.info('Confusion matrix:')
    logger.info(confusion_matrix(y_test, y_pred))
    logger.info('Accuracy score:')
    logger.info(accuracy_score(y_test, y_pred))
    
    # Save model
    p = pathlib.Path(model_file_path)
    if not p.exists(): p.parent.absolute().mkdir(parents=True, exist_ok=True)
    # pickle.dump(xgb_model, open(p, 'wb'))
    xgb_model.save_model(p)

    # Save metrics
    p = pathlib.Path(mlpipeline_metrics_path)
    metrics = {
        'metrics': [
            {
            'name': 'accuracy_score',
            'numberValue': accuracy_score(y_test, y_pred),
            'format': "PERCENTAGE"
            }
        ]
    }
    if not p.exists(): p.parent.absolute().mkdir(parents=True, exist_ok=True)
    with open(p, 'w') as f:
        json.dump(metrics, f)

if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--X_train_path', type=str, action='store')
        parser.add_argument('--X_test_path', type=str, action='store')
        parser.add_argument('--y_train_path', type=str, action='store')
        parser.add_argument('--y_test_path', type=str, action='store')
        parser.add_argument('--n_estimator', type=int, action='store')
        parser.add_argument('--model_file_path', type=str, action='store')
        parser.add_argument('--mlpipeline_metrics_path', type=str, action='store')

        FLAGS = parser.parse_args()
        X_train_path = FLAGS.X_train_path
        X_test_path = FLAGS.X_test_path
        y_train_path = FLAGS.y_train_path
        y_test_path = FLAGS.y_test_path
        n_estimator = FLAGS.n_estimator
        model_file_path = FLAGS.model_file_path
        mlpipeline_metrics_path = FLAGS.mlpipeline_metrics_path

        # Call the train function
        train_model(X_train_path, X_test_path, y_train_path, y_test_path, 
                n_estimator,
                model_file_path, mlpipeline_metrics_path)

    except Exception as e:
        logger.exception(e)
