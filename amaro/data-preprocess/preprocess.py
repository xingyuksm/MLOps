#!/usr/bin/env python3
import requests
import pathlib
import argparse
import pickle
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import spacy
import logging

nlp = spacy.load("en_core_web_lg")
pd.set_option('display.max_colwidth', None)

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

def data_ingestion(url, output_path):
    '''The function fetches data by given URL.
    
    '''
    
    p = pathlib.Path(output_path)
    if p.exists():
        logger.warning('Output file already exists.')
        with open(output_path, 'r') as f:
            ret = pd.read_csv(f)
    else:
        _check_path(output_path)
        with open(output_path, 'w') as f:
            r = requests.get(url)
            f.write(r.text)
            ret = pd.read_csv(p)

    logger.info("Data head:")
    logger.info(ret.head())
    return ret

def data_exploration(df):

    def _process_text(row):
        text = row['Input.ngram']
        doc = nlp(text)
        return doc

    def _count_tokens(row):
        return len(row['doc'])

    def _encode(row):
        return row['doc'].vector

    df['doc'] = df.apply(_process_text, axis=1)
    df['n_tokens'] = df.apply(_count_tokens, axis=1)
    df['embed'] = df.apply(_encode, axis=1)

    return df

def stats_gen(df):

    ret = {
        'n_example': df.shape[0],
        'n_true': df[df['MTurk_label']==True].shape[0],
        'n_false': df[df['MTurk_label']==False].shape[0],
        'max_length': max(df['n_tokens']),
        'min_length': min(df['n_tokens']),
        'avg_length': sum(df['n_tokens'].to_list())/df.shape[0]
    }
    logger.info("Data statitics:")
    logger.info(ret)
    return ret

def n_token_hist(df, save_path):

    _check_path(save_path)

    fig = plt.figure(1, figsize=(10,10))
    ax = plt.subplot()
    ax.hist(df['n_tokens'], bins=50)
    ax.set_xlabel('# of tokens')
    ax.set_ylabel('# of texts')
    fig.savefig(save_path, dpi=300)

def embed_plot(df, save_path, n_components=3):

    _check_path(save_path)

    fig = plt.figure(1, figsize=(10, 10))
    ax = plt.subplot()

    data = np.array(df['embed'].to_list())
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(data)

    labels = df['MTurk_label'].to_list()
    markers = []
    colors = []
    for l in labels:
        if l == True:
            markers.append('o')
            colors.append('red')
        else:
            markers.append('^')
            colors.append('green')

    # df_ = pd.DataFrame(data=components, columns = ['pc' + str(i) for i in range(n_components)])

    fig = plt.figure(1, figsize=(10,10))
    ax = fig.add_subplot(projection='3d')
    for i in range(df.shape[0]):
        ax.scatter(components[i, 0], components[i, 1], components[i,2], marker=markers[i], color=colors[i])
    ax.set_xlabel('PC #1')
    ax.set_ylabel('PC #2')
    ax.set_zlabel('PC #3')
    legend_elements = [
        Line2D([0], [0], marker='o', color='red', label="Litigation_True"),
        Line2D([0], [0], marker='^', color='green', label="Litigation_Negative")
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    fig.savefig(save_path, dpi=300)

def save_data(df, X_save_path, y_save_path):
    _check_path(X_save_path)
    _check_path(y_save_path)
    X = df['embed'].to_list()
    y = df['MTurk_label']
    #X.to_json(X_save_path)
    np.savetxt(X_save_path, np.array(X), delimiter=',')
    y.to_csv(y_save_path)

if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', type=str, action='store')
        parser.add_argument('--output_path', type=str, action='store')
        parser.add_argument('--hist_path', type=str, action='store')
        parser.add_argument('--embed_plot_path', type=str, action='store')
        parser.add_argument('--features_save_path', type=str, action='store')
        parser.add_argument('--labels_save_path', type=str, action='store')

        FLAGS = parser.parse_args()

        # Call the data_ingestion function
        logger.info("Ingesting data:")
        df = data_ingestion(FLAGS.url, FLAGS.output_path)
        df = data_exploration(df)
        stats = stats_gen(df)
        n_token_hist(df, FLAGS.hist_path)
        embed_plot(df, FLAGS.embed_plot_path, n_components=3)
        save_data(df, FLAGS.features_save_path, FLAGS.labels_save_path)

    except Exception as e:
        logger.exception(e)