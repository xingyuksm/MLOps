import kfp
from kfp import dsl

def data_ingestion_op(url):
	'''Call data ingestion component to 
	ingestion data

	'''

	return dsl.ContainerOp(
		name='Ingest Data from URL',
		image='',
		arguments=[
			'--url', url,
			'--output_path', "/temp_storage/ingested_data.csv"
		],
		file_outputs={
			'ingested_file': "/temp_storage/ingested_data.csv"
		}
	)

def data_preprocess_op(ingested_file):
	'''Preprocess ingested data

	'''

	return dsl.ContainerOp(
		name='Data Preprocess',
		image='',
		arguments=[
			'--data_path', ingested_file,
			'--label_col', 'variety',
			'--output_path', '/temp_storage'
		],
		file_outputs={
			'X_train': "/temp_storage/X_train.csv",
			'X_test' : "/temp_storage/X_test.csv",
			'y_train': "/temp_storage/y_train.csv",
			'y_test' : "/temp_storage/y_test.csv"
		}
	)

def train_eval_op(X_train, X_test, y_train, y_test):

	return dsl.ContainerOp(
		name='Train and Evaluation',
		image='',
		arguments=[
			'--X_train_path', X_train,
			'--X_test_path', X_test,
			'--y_train_path', y_train,
			'--y_test_path', y_test,
			'--n_estimator', 2,
			'--output_path', '/temp_storage'
		],
		file_outputs={
			'model_file': '/temp_storage/xgb.pkl',
			'label_encoder_file': '/temp_storage/le.pkl'
		}
	)
