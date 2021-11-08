import json
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s : %(lineno)d] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_metrics(metrics_file):
	with open(metrics, 'r') as f:
		data = json.load(f)
	return data

def argmax(l):
	if not l: return
	res = 0
	for i in range(len(l)):
		if l[i] > l[res]:
			res=i

	return res

def eval_deploy(rf_metrics_file, xgb_metrics_file, 
	rf_model_file, xgb_model_file):
	rf_metrics = load_metrics(rf_metrics_file)
	xgb_metrics = load_metrics(xgb_metrics_file)

	rf_score = float(rf_metrics['metrics'][0]['numberValue'])
	xgb_score = float(xgb_metrics['metrics'][0]['numberValue'])
	scores = [rf_score, xgb_score]
	model_names = ["Random Forest", "XGBoost"]
	models = [rf_model_file, xgb_model_file]

	best_model_idx = argmax(scores)

	logger.info(f"The {model_names[best_model_idx]} has a better eval score {scores[best_model_idx]}.")

	# Copy best model to model registery
	best_model = models[best_model_idx]

	logger.info(f"Model deployed to model registery at gs://example.com.")

if __name__ == "__main__":
    try:
        # The component must be stateless
        # All inputs are not hard coded but passed in as params
        parser = argparse.ArgumentParser()
        parser.add_argument('--rf_metrics_file', type=str, action='store')
        parser.add_argument('--xgb_metrics_file', type=str, action='store')
        parser.add_argument('--rf_model_file', type=str, action='store')
        parser.add_argument('--xgb_model_file', type=str, action='store')

        FLAGS = parser.parse_args()

        eval_deploy(FLAGS.rf_metrics_file, 
        	FLAGS.xgb_metrics_file, 
        	FLAGS.rf_model_file, 
        	FLAGS.xgb_model_file
        	)

    except Exception as e:
        logger.exception(e)