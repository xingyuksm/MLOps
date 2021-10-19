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

def data_preprocess(data_path, label_col, x_train_path, x_test_path, y_train_path, y_test_path, label_encoder_path):
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

    paths = [x_train_path, x_test_path, y_train_path, y_test_path]
    data = [X_train, X_test, y_train, y_test] 

    for i in range(len(paths)):
        
        p = pathlib.Path(paths[i])
        if not p.exists(): 
            p.parent.absolute().mkdir(parents=True, exist_ok=True)
        data[i].to_csv(p, index=False)
    
    p = pathlib.Path(label_encoder_path)
    if not p.exists():
        p.parent.absolute().mkdir(parents=True, exist_ok=True)
    pickle.dump(le, open(p, 'wb'))
    
    return X_train, y_train, X_test, y_test

if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--data_path', type=str, action='store')
        parser.add_argument('--label_col', type=str, action='store')
        parser.add_argument('--x_train_path', type=str, action='store')
        parser.add_argument('--x_test_path', type=str, action='store')
        parser.add_argument('--y_train_path', type=str, action='store')
        parser.add_argument('--y_test_path', type=str, action='store')
        parser.add_argument('--label_encoder_path', type=str, action='store')

        FLAGS = parser.parse_args()

        # Call the data_preprocess function
        data_preprocess(FLAGS.data_path, FLAGS.label_col, 
                        FLAGS.x_train_path, FLAGS.x_test_path, FLAGS.y_train_path, FLAGS.y_test_path,
                        FLAGS.label_encoder_path)

    except Exception as e:
        logger.exception(e)
