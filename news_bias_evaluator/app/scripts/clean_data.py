import os
import pandas as pd

def clean_data():
    # Read in the data
    df = pd.read_csv('../assets/media_bias_dataset.csv')

    # Drop the columns we don't need
    df = df.drop(columns=['group_id', 'num_sent'])

    # Rename the columns
    df = df.rename(columns={'Label_bias': 'label'})
    
    # Remove non-unique sentences
    df = df.drop_duplicates(subset=['sentence'])

    # Remove 'No agreement' rows from label
    df = df[df.label != 'No agreement']
    
    # Save the cleaned data
    print("Saving cleaned data")
    print("Datapoints saved: ", len(df))
    df.to_csv(os.path.join('../assets/media_bias_dataset_cleaned.csv'), index=False)

    pseudo_df = pd.read_csv('../assets/pseudo_labelled.csv')
    
    # Remove non-unique sentences
    pseudo_df = pseudo_df.drop_duplicates(subset=['sentence'])

    # Remove a tags from sentences
    pseudo_df['sentence'] = pseudo_df['sentence'].str.replace('<a.*?>', '')

    # Save the cleaned data
    print("Saving cleaned pseudo-labelled data")
    df.to_csv(os.path.join('../assets/pseudo_labelled_data_cleaned.csv'), index=False)
    print("Datapoints saved: ", len(pseudo_df))

if __name__ == '__main__':
    clean_data()
