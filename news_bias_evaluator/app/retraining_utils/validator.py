import pandas as pd

# Validate incoming data before storing into cloudSQL.
def prepare_data(db_data_df: pd.DataFrame):
    # Select only wanted columns
    training_data_df = db_data_df[["sentence", "label_bias"]]

    # Rename label_bias to fit what the trainer expects
    training_data_df = training_data_df.rename(columns={'label_bias': 'Label_bias'})
    
    # Remove no agreement labels
    training_data_df = training_data_df[training_data_df.Label_bias != 'No agreement']

    # Remove rows with missing values 
    training_data_df = training_data_df.dropna()

    # Make numeric categorical values
    training_data_df['Label_bias'] = training_data_df['Label_bias'].replace('Biased', 1)
    training_data_df['Label_bias'] = training_data_df['Label_bias'].replace('Non-biased', 0)

    return training_data_df