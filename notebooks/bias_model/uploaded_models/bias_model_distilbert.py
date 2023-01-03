#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from transformers import (
    DistilBertTokenizerFast,
    TFDistilBertForSequenceClassification,
)

MAX_SEQUENCE_LENGTH = 256
LEARNING_RATE = 2e-5
BATCH_SIZE = 16
NUM_EPOCHS = 3


# In[4]:


tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

def tokenize(sentences, max_length=MAX_SEQUENCE_LENGTH, padding='max_length'):

    return tokenizer(
        sentences,
        truncation=True,
        padding=padding,
        max_length=max_length,
        return_tensors="tf"
    )


# In[4]:


# Load dataset
df = pd.read_csv('../dataset/media_bias.csv')
df2 = pd.read_csv('../dataset/pseudo_labeled.csv')

# Clean original dataset
df = df[df.Label_bias != 'No agreement']
df = df[df.article != 'NaN']
df = df[df.sentence != 'NaN']

# Clean pseudo labeled dataset
df2 = df2[df2.article != 'NaN']
df2 = df2[df2.sentence != 'NaN']

# Replace label in original dataset with 0, 1
df['Label_bias'] = df['Label_bias'].replace('Biased', 1)
df['Label_bias'] = df['Label_bias'].replace('Non-biased', 0)

# Rename label column in original dataset
df = df.rename(columns={'Label_bias': 'label'})

# Use only sentence and label from df
df = df[['sentence', 'label']]

# Use only sentence and label from df2
df2 = df2[['sentence', 'label']]

# Combine datasets
df = pd.concat([df, df2], ignore_index=True)

print(len(df))

train_data, validation_data, train_label, validation_label = train_test_split(
    df['sentence'].tolist(),
    df['label'].tolist(),
    test_size=.3,
    shuffle=True
)

validation_data, test_data, validation_label, test_label = train_test_split(validation_data, validation_label, test_size=.5, shuffle=True)


# In[5]:


train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(tokenize(train_data)),  # Convert BatchEncoding instance to dictionary
    train_label
)).shuffle(1000).batch(BATCH_SIZE).prefetch(1)
validation_dataset = tf.data.Dataset.from_tensor_slices((
    dict(tokenize(validation_data)),
    validation_label
)).batch(BATCH_SIZE).prefetch(1)


# In[6]:


model = TFDistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=2
)

optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
model.compile(
    optimizer=optimizer,
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
)


# In[7]:


model.fit(
    x=train_dataset,
    validation_data=validation_dataset,
    batch_size=BATCH_SIZE,
    epochs=NUM_EPOCHS,
)


# In[9]:


# test model and plot confusion matrix
model.evaluate(validation_dataset)


# In[10]:


#Get predictions
predictions = model.predict(validation_dataset)
predictions = tf.nn.softmax(predictions[0], axis=1)
predictions = tf.argmax(predictions, axis=1) 


# In[11]:


# plot confusion matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    plt.show()

plot_confusion_matrix(validation_label, predictions)


# In[12]:


# show accuracy
from sklearn.metrics import accuracy_score
print(accuracy_score(validation_label, predictions))


# In[8]:


model.save('./model', save_format='tf')


# In[7]:


inputs = dict(tokenizer(["This is a factual sentence that can be seen in a good light don't you think so, but it seems like they're all unbiased.","YouTube is making clear there will be no “birtherism” on its platform during this year’s U.S. presidential election – a belated response to a type of conspiracy theory more prevalent in the 2012 race.", "The increasingly bitter dispute between American women’s national soccer team and the U.S. Soccer Federation spilled onto the field Wednesday night when players wore their warm-up jerseys inside outin a protest before their 3-1 victory over Japan.","A professor who teaches climate change classes — a subject some would question as a legitimate area of study — said she has seen students who suffer fear, grief, stress, and anxiety about the future."], padding=True, truncation=True, return_tensors="tf"))


# In[14]:


print(inputs)


# In[16]:


# Load the model from the local folder for testing purposes
modelOpen = tf.keras.models.load_model('./model')

import numpy as np
from scipy.special import softmax
#Testing if the loaded model works
newPrediction = modelOpen.predict(inputs)
mutatedToSoftmax = softmax(newPrediction['logits'])
predictionArray = np.argmax(mutatedToSoftmax, axis=1)
print(predictionArray)

