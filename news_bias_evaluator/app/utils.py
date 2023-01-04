import json
import os  # An included library with Python install.
from google.api_core.client_options import ClientOptions
from googleapiclient import discovery
import datetime
import requests
import re
import numpy as np

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
        client_options = ClientOptions(api_endpoint = endpoint)
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
    
    modelList = []

    try:
        response = requests.get(endpoint+'//v1/projects/dit825/models/', headers={'Authorization': 'Bearer '+getToken()}).json()
        print(response)
        modelList = getModelVersion(response['models'])
    except:
        print("Failed to connect to Google cloud!")

    return modelList


def getModelVersion(models):

    modelVersionList = []
    for model in models:
        modelName = model['name']
        response = requests.get('https://europe-west4-ml.googleapis.com//v1/'+modelName+'/versions', headers={'Authorization': 'Bearer '+getToken()}).json()
        for version in response['versions']:
            modelVersionList.append(version['name'])

    return modelVersionList

def getToken():
    try:
        file = open(cwd+"/modelSettings.json", "r")
        data = json.load(file)
        TOKEN = data['token']
        file.close()
        return TOKEN
    except:
        print("Failed to access token from json file: modelSettings.json")

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
