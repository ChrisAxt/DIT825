from google.cloud import storage
import pandas as pd
import json

def get_training_evaluation_data():
    training_evaluation_data_df = pd.read_csv('gs://example_bucket_v2-aiproject-dit825/simple_model/training_metrics/training_metrics.csv')
    training_evaluation_data_json = {
        'name': 'latest trained simple model',
        'true_positive': training_evaluation_data_df['true_positive'].values[0],
        'false_positive': training_evaluation_data_df['false_positive'].values[0],
        'false_negative': training_evaluation_data_df['false_negative'].values[0],
        'true_negative': training_evaluation_data_df['true_negative'].values[0]
    }

    print(training_evaluation_data_json)
    return training_evaluation_data_json
