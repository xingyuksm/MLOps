#!/usr/bin/env python3
import pathlib
import argparse
import pickle
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s : %(lineno)d] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

def data_preprocess(data_path, label_col, output_path):
    '''Load newly ingested data and generate training and testing sets
    
    '''
    p = pathlib.Path(data_path)
    if p.exists() != True:
        print(f'Cannot locate data at {data_path}')
        return
    
    df = pd.read_csv(p)
    
    y = df.pop(label_col)
    
    # Encode labels
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = le.transform(y)
    y = pd.DataFrame(y, columns=[label_col])
    
    X = df
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, stratify=y)
    
    p = pathlib.Path(output_path)
    
    if not p.exists(): p.mkdir(exist_ok=True)
    X_train.to_csv(p / 'X_train.csv', index=False)
    y_train.to_csv(p / 'y_train.csv', index=False)
    X_test.to_csv(p / 'X_test.csv', index=False)
    y_test.to_csv(p / 'y_test.csv', index=False)

    pickle.dump(le, open(p / 'le.pkl', 'wb'))
    
    return X_train, y_train, X_test, y_test

if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--data_path', type=str, action='store')
        parser.add_argument('--label_col', type=str, action='store')
        parser.add_argument('--output_path', type=str, action='store')

        FLAGS = parser.parse_args()
        data_path = FLAGS.data_path
        label_col = FLAGS.label_col
        output_path = FLAGS.output_path

        # Call the data_preprocess function
        data_preprocess(data_path, label_col, output_path)

    except Exception as e:
        logger.exception(e)