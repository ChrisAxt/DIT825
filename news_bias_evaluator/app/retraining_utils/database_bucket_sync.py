# Shall convert data from cloudSQL into a csv format for the ai platform bucket.
from app.models import LabeledSentence
import pandas as pd
from app.retraining_utils import validator 
from google.cloud import storage

def sync_db_and_bucket(): 
    # Pull data from database
    db_training_data_df, db_evaluation_data_df = get_data_from_db()
    # Validate and clean the data
    training_data_df = validator.prepare_data(db_training_data_df)
    evaluation_data_df = validator.prepare_data(db_evaluation_data_df) 
    # Convert to csv and store to the bucket
    bucket_name = 'example_bucket_v2-aiproject-dit825'
    store_data_to_bucket(training_data_df, bucket_name, 'training_data/media_bias_dataset_cleaned.csv')
    store_data_to_bucket(evaluation_data_df, bucket_name, 'evaluation_data/evaluation_data.csv')


def get_data_from_db():
    db_training_data_df = pd.DataFrame(list(LabeledSentence.objects.all().values()))
    # Remove last 50 entries to train the model on.
    # (ie dont train model on eval data)
    db_training_data_df = db_training_data_df[:-50 or None]
    # Get the last 50 values for evaluation
    db_eval_data_df = pd.DataFrame(list(LabeledSentence.objects.all()[-50:].values()))
    print(db_training_data_df)
    print(db_eval_data_df)
    return db_training_data_df, db_eval_data_df
    

def store_data_to_bucket(data_df, bucket_name, bucket_file):
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(bucket_file)

    blob.upload_from_string(convert_to_csv(data_df), 'text/csv')


def convert_to_csv(db_data_df):
    return db_data_df.to_csv()
