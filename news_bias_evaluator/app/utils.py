import json
import os  # An included library with Python install.
from google.api_core.client_options import ClientOptions
from googleapiclient import discovery
import datetime
import requests
import re
import numpy as np
from .models import ModelEvaluation
from transformers import DistilBertTokenizerFast


cwd = os.getcwd()
endpoint = 'https://europe-west4-ml.googleapis.com'

def extractSentences(text_input):

    sentenceList = []
    firstIndex = 0
    text_input = text_input.strip()

    if (text_input != ""):
        for i in range(0, len(text_input)):
            # Check for sentence ending chars
            if (text_input[i] == "." or text_input[i] == "?" or text_input[i] == "!"):
                #  # Remove all special characters excluding full stops
                # re.sub(r'[^\w\s]', '', text_input[i])
                # # Remove all extra spaces
                # re.sub('  ', ' ', text_input[i])
                # # add handling for duplicate of sentence ending chars
                sentence = text_input[firstIndex:i+1]
                if (len(sentence) > 1):
                    sentenceList.append(sentence.strip())
                firstIndex = i+1
        
        # add handling for the last sentence not ending with the sentence ending char
        if (text_input[len(text_input) -1] != "." or text_input[len(text_input) -1] != "!" or text_input[len(text_input) -1] != "?"):
            if ((i+1 - firstIndex) > 2):
                sentenceList.append(text_input[firstIndex:i+1].strip())
                
    return sentenceList
        
def sendRequest(sentenceList, model_name):
    try:
        client_options = ClientOptions(api_endpoint = endpoint, credentials_file=cwd+"/application_default_credentials.json")
        ml = discovery.build('ml', 'v1', client_options=client_options)

        request_body = {'instances' : sentenceList}
        prediction_request = ml.projects().predict(
            name=model_name, body = request_body)
    

        response = prediction_request.execute()
        return response['predictions']
    except:
        print("Failed to get a response from the selected model!")

# Get the current time with a specific format
def getCurrentDateTime(format):
    current_datetime = datetime.datetime.now()
    current_datetime_formatted = current_datetime.strftime(format)
    return current_datetime_formatted

def getModels():
    
    # generate new token
    key = os.popen('gcloud auth print-access-token').read()
    # remove newline from end of token
    key = key[0:len(key)-2]
    
    modelList = []

    try:
        response = requests.get(endpoint+'//v1/projects/dit825/models/', headers={'Authorization': 'Bearer '+key}).json()
        print(response)
        modelList = getModelVersion(response['models'])
    except:
        print("Failed to connect to Google cloud!")

    return modelList


def getModelVersion(models):

    # generate new token
    key = os.popen('gcloud auth print-access-token').read()
    # remove newline from end of token
    key = key[0:len(key)-2]

    modelVersionList = []
    for model in models:
        modelName = model['name']
        response = requests.get('https://europe-west4-ml.googleapis.com//v1/'+modelName+'/versions', headers={'Authorization': 'Bearer '+key}).json()
        for version in response['versions']:
            modelVersionList.append(version['name'])

    return modelVersionList

def getFromJson(name):
    try:
        file = open(cwd+"/modelSettings.json", "r")
        data = json.load(file)
        if(name == 'prediction_model'):
            result = data['prediction_model']
        elif(name == 'evaluation_model'):
            result = data['evaluation_model']
        elif(name == 'token'):
            result = data['token']
        file.close()
        return result
    except:
        print("Failed to access information from json file: modelSettings.json")

# Gets the tokenized sentences in order to send them to the model for prediction
def getPredictionArrays(sentenceList):
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
    predictionInput = []
    for sentence in sentenceList:
        tokenized = tokenizer(sentence,
        truncation=False,
        padding='max_length',
        max_length=256,
        return_tensors="tf")
        # Create a dictionary from the tensor with the input_ids and attention_mask
        tokenized = {'input_ids': tokenized['input_ids'].numpy().tolist()[0], 'attention_mask': tokenized['attention_mask'].numpy().tolist()[0]}

        predictionInput.append(tokenized)
    return predictionInput


def is_valid_news_link(news_link):
    '''
    Checks that the news_link format is respected
    return True if it is, false if not
    '''
    _re_url = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    if (re.match(_re_url, news_link)):
        return True
    return False 

def is_non_empty_sentence(sentence):
    '''
    checks the validity of the sentence
    return True if it is, false if not
    '''
    _re_sentence_blank = "^\s+$"
    if not sentence or re.match(_re_sentence_blank, sentence):
        return False
    return True

def is_valid_label_bias(label_bias):
    '''
    Checks if the label bias is accepted
    return True if it is, false if not
    '''
    if label_bias.lower() == 'biased' or label_bias.lower() == 'non-biased' or label_bias.lower() == '0' or label_bias.lower() == '1':
        return True
    return False

def convert_label_bias(label_bias):
    '''
    convert the label_bias into string number value
    Should be used after using is_valid_label_bias only
    '''
    if(label_bias.lower() == 'biased'):
        return '1'
    if(label_bias.lower() == 'non-biased'):
        return '0'
    else:
        return label_bias
def softmax(array):
    softmax_output = []
    for i in range(len(array)):
        softmax = list(np.exp(array[i] - np.max(array[i])) / np.exp(array[i] - np.max(array[i])).sum())
        softmax_output.append(softmax)
    return softmax_output

def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')

def saveEvaluation(model_evaluation):

    try:
        new_Evaluation = ModelEvaluation(
            version_name = model_evaluation['name'],
            true_positive = model_evaluation['true_positive'],
            false_positive = model_evaluation['false_positive'],
            false_negative = model_evaluation['false_negative'],
            true_negative = model_evaluation['true_negative']
        )

        new_Evaluation.save()
        print("Evaluation successfully saved")
    except:
        #print(new_Evaluation)
        print("Failed to save the evaluation!")

def retrieveLatestEvaluation(queriedModel):
    try:
        modelMatches = ModelEvaluation.objects.get(model = queriedModel)
        latestEntry = {}
        for entry in modelMatches:
            if latestEntry == {}:
                latestEntry = entry
            elif entry['date_evaluated'] > latestEntry['date_evaluated']:
                latestEntry = entry
        return latestEntry
    except:
        print("No elaluations found for the specified model")
