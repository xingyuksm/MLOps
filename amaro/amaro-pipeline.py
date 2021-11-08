import kfp
from kfp import components
from kfp import dsl

amarobot_preprocess_op = components.load_component_from_file('./data-preprocess/component.yaml')
amarobot_xgb_op = components.load_component_from_file('./train-xgb/component.yaml')
amarobot_rf_op = components.load_component_from_file('./train-rf/component.yaml')

@dsl.pipeline(
	name='AMAROBot Pipeline',
	description='Train a classifier for identifying litigation texts'
)
def amarobot_pipeline():
	# Link to data set
	data_url = 'https://raw.githubusercontent.com/xingyuksm/MLOps/main/amaro/data/batch_01_train.csv'

	# Ingest and preprocess data
	data_preprocessor = amarobot_preprocess_op(
		url=data_url)
	data_preprocessor.container.set_image_pull_policy("Always")

	# Train and compare models
	xgb_model = amarobot_xgb_op(
		features=data_preprocessor.outputs['features'],
		labels=data_preprocessor.outputs['labels']
		)

	xgb_model.container.set_image_pull_policy("Always")

	rf_model = amarobot_rf_op(
		features=data_preprocessor.outputs['features'],
		labels=data_preprocessor.outputs['labels']
		)

	rf_model.container.set_image_pull_policy("Always")

kfp.compiler.Compiler().compile(pipeline_func=amarobot_pipeline, package_path='amarobot-pl.yaml')