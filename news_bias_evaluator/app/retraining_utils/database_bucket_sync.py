# Shall convert data from cloudSQL into a csv format for the ai platform bucket.
from app.models import LabeledSentence
import pandas as pd
from app.retraining_utils import validator 
from google.cloud import storage

def sync_db_and_bucket(): 
    # Pull data from database
    db_data_df = get_data_from_db()
    # Validate and clean the data
    training_data_df = validator.prepare_training_data(db_data_df)
    # Convert to csv and store to the bucket
    store_data_to_bucket(training_data_df)


def get_data_from_db():
    db_data_df = pd.DataFrame(list(LabeledSentence.objects.all().values()))
    print(db_data_df)
    return db_data_df
    

def store_data_to_bucket(training_data_df):
    
    storage_client = storage.Client()
    bucket = storage_client.bucket('example_bucket_v2-aiproject-dit825')
    blob = bucket.blob('training_data/media_bias_dataset_cleaned.csv')

    blob.upload_from_string(convert_to_csv(training_data_df), 'text/csv')

def convert_to_csv(db_data_df):
    return db_data_df.to_csv()
