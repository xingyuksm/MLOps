#!/usr/bin/env python3
import pathlib
import requests
import argparse
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s : %(lineno)d] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

def data_ingestion(url, output_path):
    '''The function fetches data by given URL.
    
    '''
    
    p = pathlib.Path(output_path)
    if p.exists():
        logger.warning('Output file already exists.')
        with open(output_path, 'r') as f:
            ret = f.read()
    else:
        p.parent.absolute().mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            r = requests.get(url)
            f.write(r.text)
            ret = r.text

    logger.info(ret[:100])
    return ret

if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', type=str, action='store')
        parser.add_argument('--output_path', type=str, action='store')

        FLAGS = parser.parse_args()
        url = FLAGS.url
        output_path = FLAGS.output_path

        # Call the data_ingestion function
        data_ingestion(url, output_path)

    except Exception as e:
        logger.exception(e)
