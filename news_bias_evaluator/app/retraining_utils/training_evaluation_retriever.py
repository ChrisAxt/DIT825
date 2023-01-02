from google.cloud import storage
import pandas as pd
import json
from ..templatetags import evaluation

def get_training_evaluation_data():
    training_evaluation_data_df = pd.read_csv('gs://example_bucket_v2-aiproject-dit825/simple_model/training_metrics/training_metrics.csv')
    training_evaluation_data_json = {
        'name': 'latest trained simple model',
        'true_positive': training_evaluation_data_df['true_positive'].values[0],
        'false_positive': training_evaluation_data_df['false_positive'].values[0],
        'false_negative': training_evaluation_data_df['false_negative'].values[0],
        'true_negative': training_evaluation_data_df['true_negative'].values[0]
    }
    training_evaluation_data_json = combine_metrics(training_evaluation_data_json)

    print(training_evaluation_data_json)
    return training_evaluation_data_json

# Calculates the different metrics and stores them into
# the initial training eval results json
def combine_metrics(matrix_data_json):
    copy_data = matrix_data_json.copy()
    matrix_data_json['accuracy'] = evaluation.getAccuracy(copy_data)
    matrix_data_json['precision'] = evaluation.getPrecision(copy_data)
    matrix_data_json['neg_precision'] = evaluation.getNegPrecision(copy_data)
    matrix_data_json['recall']: evaluation.getAccuracy(copy_data)

    return matrix_data_json