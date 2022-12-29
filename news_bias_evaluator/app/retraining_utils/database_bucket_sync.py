# Shall convert data from cloudSQL into a csv format for the ai platform bucket.
from app.models import LabeledSentence

def get_data_from_db(query_params):
    db_data = LabeledSentence.objects.all().values()
    print(db_data)
    return db_data
    # Pull in data from database
    # validate the data

#def convert_to_csv(data):
    # convert data to csv

#def store_data_to_bucket():