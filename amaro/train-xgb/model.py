#!/usr/bin/env python3
import json
import pickle
import pathlib

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import auc, accuracy_score, confusion_matrix, mean_squared_error
import xgboost as xgb
import argparse
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s : %(lineno)d] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

def _check_path(path):
    p = pathlib.Path(path)
    if not p.exists():
        logger.info(f"Path {path} does not exist. Creating...")
        p.parent.absolute().mkdir(parents=True, exist_ok=True)
        return False
    else:
        logger.info(f"Path {path} already exists.")
        return True

def load_data(features_file_path, labels_file_path):
    X = np.loadtxt(features_file_path, delimiter=',')
    y = pd.read_csv(labels_file_path)

    assert X.shape[0] == y['MTurk_label'].shape[0]

    return X, [int(d) for d  in y['MTurk_label'].to_list()]

def train(X, y, 
    cv_results_file_path, 
    model_save_path,
    mlpipeline_metrics_path,
    test_size=0.3):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)

    estimator = xgb.XGBClassifier(
        objective="binary:logistic", 
        eval_metric="logloss",
        use_label_encoder=False,
        random_state=42)
    
    parameters={
        'max_depth': range(2, 5, 1),
        'n_estimators': range(10, 100, 10),
        'learning_rate': [0.1, 0.05, 0.01]
    }   
                                 
    random_search = RandomizedSearchCV(
        estimator=estimator, 
        param_distributions=parameters,
        scoring='accuracy',
        random_state=22,
        return_train_score=True
        )

    search_result = random_search.fit(X_train, y_train)

    cv_results = search_result.cv_results_
    best_params = search_result.best_params_
    best_score = search_result.best_score_
    best_model = search_result.best_estimator_

    cv_results = pd.DataFrame(cv_results)

    _check_path(cv_results_file_path)
    cv_results.to_csv(cv_results_file_path)

    logger.info(f"Model: {estimator}")
    logger.info(f"Best CV score is {best_score}")
    logger.info(f"Best parameters are {best_params}")
    

    # Save model
    _check_path(model_save_path)
    pickle.dump(best_model, open(model_save_path, 'wb'))

    # Save metrics
    _check_path(mlpipeline_metrics_path)
    y_pred = best_model.predict(X_test)
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
    with open(mlpipeline_metrics_path, 'w') as f:
        json.dump(metrics, f)

    logger.info(f"Test score is {accuracy_score(y_test, y_pred)}")


if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--features_file_path', type=str, action='store')
        parser.add_argument('--labels_file_path', type=str, action='store')
        parser.add_argument('--cv_results_file_path', type=str, action='store')
        parser.add_argument('--model_file_path', type=str, action='store')
        parser.add_argument('--kfp_metrics_path', type=str, action='store')

        FLAGS = parser.parse_args()

        X, y = load_data(FLAGS.features_file_path, FLAGS.labels_file_path)
        train(X, y, 
            FLAGS.cv_results_file_path,
            FLAGS.model_file_path,
            FLAGS.kfp_metrics_path)

    except Exception as e:
        logger.exception(e)