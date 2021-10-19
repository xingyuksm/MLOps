import kfp
from kfp import components
from kfp import dsl

data_ingestion_op = components.load_component_from_file('./pipeline/data_ingestion/component.yaml')
data_preprocess_op = components.load_component_from_file('./pipeline/data_preprocess/component.yaml')
train_eval_op = components.load_component_from_file('./pipeline/train_model/component.yaml')

@dsl.pipeline(
    name='Iris pipeline',
    description='An example pipeline of training a classification model on the Iris dataset'
)
def iris_pipeline():
    url = 'https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv'
    
    ingested_data = data_ingestion_op(url=url)
    ingested_data.container.set_image_pull_policy("Always")
    ingested_data.execution_options.caching_strategy.max_cache_staleness = "P0D"
    processed_data = data_preprocess_op(ingested_data=ingested_data.outputs['data'],
                                        label_colname='variety'
                                        )
    train_eval = train_eval_op(x_train=processed_data.outputs['x_train'],
                                x_test=processed_data.outputs['x_test'],
                                y_train=processed_data.outputs['y_train'],
                                y_test=processed_data.outputs['y_test'],
                                number_of_estimators=2
                                )

kfp.compiler.Compiler().compile(pipeline_func=iris_pipeline, package_path='pipeline.yaml')
