from google.cloud import storage
import pandas as pd
import json
from ..templatetags import evaluation

def get_training_evaluation_data():
    # get the training metrics from the latest training job.
    training_evaluation_data_df = pd.read_csv('gs://example_bucket_v2-aiproject-dit825/simple_model/training_metrics/training_metrics.csv')
    # Create a json format containing the training metrics
    training_evaluation_data_json = {
        'model': 'latest trained simple model',
        'true_positive': int(training_evaluation_data_df['true_positive'].values[0]),
        'false_positive': int(training_evaluation_data_df['false_positive'].values[0]),
        'false_negative': int(training_evaluation_data_df['false_negative'].values[0]),
        'true_negative': int(training_evaluation_data_df['true_negative'].values[0])
    }
    # Combine the previous json object with metric calculations
    training_evaluation_data_json = combine_metrics(training_evaluation_data_json)

    return training_evaluation_data_json

# Calculates the different metrics and stores them into
# the initial training eval results json
def combine_metrics(matrix_data_json):
    copy_data = matrix_data_json.copy()
    matrix_data_json['accuracy'] = float(evaluation.getAccuracy(copy_data))
    matrix_data_json['precision'] = float(evaluation.getPrecision(copy_data))
    matrix_data_json['neg_precision'] = float(evaluation.getNegPrecision(copy_data))
    matrix_data_json['recall'] = float(evaluation.getRecall(copy_data))

    return matrix_data_json