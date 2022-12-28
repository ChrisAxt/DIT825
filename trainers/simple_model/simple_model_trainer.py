# NOTE: This is a copy of the model.ipynb in the uploaded_models
# directory that Vernita made. This file contains
# minor adjustements required for the ai platform training job. 
#!/usr/bin/env python
# coding: utf-8

import os
import tempfile
# For N-dimensional array manipulation
import numpy as np
# Plotting library
import matplotlib.pyplot as plt
# For data analysis and data structures in DataFrames
import pandas as pd
# For data visualization
import seaborn as sns

# For machine learning algorithms and evaluation metrics
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import metrics

#import tensorflow
import tensorflow as tf
from tensorflow import keras
from keras import layers
# import TextVectorization from keras
from keras.layers import TextVectorization
from google.cloud import storage
import glob




# Load dataset
df = pd.read_csv('gs://example_bucket_v2-aiproject-dit825/training_data/media_bias_dataset_cleaned.csv')

# Clean dataset
df = df[df.Label_bias != 'No agreement']
#df = df[df.article != 'NaN']
df = df[df.sentence != 'NaN']

# Replace label with 0, 1
df['Label_bias'] = df['Label_bias'].replace('Biased', 1)
df['Label_bias'] = df['Label_bias'].replace('Non-biased', 0)

# Only use sentence column and bias column
df = df[['sentence', 'Label_bias']]
df = df.rename(columns={'sentence': 'text', 'Label_bias': 'label'})

# Split data into X and y
X = df['text']
y = df['label']

# Remove numbers from all strings in X
X = X.str.replace('\d+', '', regex=True)

# Remove punctuation from all strings in X
X = X.str.replace('[^\w\s]','',regex=True)




# Split data into train, validation and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Print shape of train, validation and test
print("X_train shape: ", X_train.shape)
# print("X_val shape: ", X_val.shape)
print("X_test shape: ", X_test.shape)


# Flatten X_train for training and X_test for testing
X_train = np.array(X_train).flatten()
X_test = np.array(X_test).flatten()
    
# X_train = X_train.to_numpy()
# X_train = np.array(X_train).flatten()
# print x shape
print("X_train shape: ", X_train.shape)
# print test shape
print("X_test shape: ", X_test.shape)




print(X_train.shape[0])
# Create DNN using tensorflow
vectorize_layer = TextVectorization(max_tokens=512, output_mode='int', output_sequence_length=128)
vectorize_layer.adapt(X_train)
model = keras.Sequential([
    vectorize_layer,
    layers.Embedding(input_dim=X_train.shape[0] , output_dim=128, mask_zero=True),
    layers.Bidirectional(layers.LSTM(128, return_sequences=True)),
    layers.Flatten(),
    layers.Dropout(0.4),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Train model
history = model.fit(X_train, y_train, epochs=4, batch_size=16, validation_data=(X_val, y_val))




# model.save('model/saved_model')
# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print("Loss: ", loss)
print("Accuracy: ", accuracy)

#prediction = model.predict(["YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.", "The increasingly bitter dispute between American women’s national soccer team and the U.S. Soccer Federation spilled onto the field Wednesday night when players wore their warm-up jerseys inside outin a protest before their 3-1 victory over Japan."])
#print(prediction, "1 is bias, 0 is non-bias")

save_path = "./simple_model/"

'''
Save metrics to a folder!
This will be overwritten with every training job.
'''

# Make directory for training metrics
os.mkdir(save_path+'training_metrics/')

# Creating a dataframe for the training metrics.
# Makes saving to cloudSQL db easier.
data = {'training_accuracy': accuracy, 'loss': loss}
metricsDf = pd.DataFrame(data=data)
metricsDf.to_csv('./simple_model/training_metrics/')

'''
end of saving metrics section
'''

#parent_dir = os.path.split(os.getcwd())[0] + "\\" + os.path.split(os.getcwd())[1]
# tf.saved_model.save(model, save_path) - DOESN'T SAVE THE LAYERS

model.save(save_path, save_format='tf') # ERROR states layers aren't saved, but keras_metadata.pb is saved

### HELPER ###
#REFERENCE: https://stackoverflow.com/questions/56759262/upload-a-folder-to-google-cloud-storage-with-python
def copy_local_directory_to_gcs(local_path, bucket, gcs_path):
    assert os.path.isdir(local_path)
    for local_file in glob.glob(local_path + '/**'):
        if not os.path.isfile(local_file):
            copy_local_directory_to_gcs(local_file, bucket, gcs_path + os.path.basename(local_file))
        else:
            remote_path = os.path.join(gcs_path, local_file[1 + len(local_path) :])
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)
### HELPER ###

storage_client = storage.Client()
bucket = storage_client.bucket('example_bucket_v2-aiproject-dit825')

# Copy each file to cloud storage directory
copy_local_directory_to_gcs('./simple_model', bucket, 'simple_model/')


# def _serving_input_receiver_fn():
#     serialized_tf_example = tf.placeholder(dtype=tf.string, shape=None, 
#                                            name='input_example_tensor')
#     # key (e.g. 'examples') should be same with the inputKey when you 
#     # buid the request for prediction
#     receiver_tensors = {'examples': serialized_tf_example}
#     inputs = {'text': tf.placeholder(tf.string, [None])}
#     return tf.estimator.export.ServingInputReceiver(inputs, receiver_tensors)



'''
from google.cloud import aiplatform
from google.cloud import storage
import os
project_id = 'dit825'
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
storage_client = storage.Client(project=project_id)
buckets = storage_client.list_buckets()
print("Buckets:")
for bucket in buckets:
    print(bucket.name) 
print("Listed all storage buckets.")
# List all models in the project from aiplatform
aiplatform.init(project=project_id, location='europe-west4')
models = aiplatform.Model.list()
print("Models:")
for model in models:
    print(model)
print("Listed all models.")
'''
#from sklearn.linear_model import LogisticRegression
#from sklearn.feature_extraction.text import CountVectorizer

#vectorizer = CountVectorizer()
#vectorizer.fit(X_train)

#train = vectorizer.transform(X_train)
#test  = vectorizer.transform(X_test)

#classifier = LogisticRegression()
#classifier.fit(train, y_train)
#score = classifier.score(test, y_test)




#print("Accuracy:", score)