import json
import os  # An included library with Python install.
from google.api_core.client_options import ClientOptions
from googleapiclient import discovery
import requests
from app.models import ModelEvaluation
from datetime import datetime

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
                # add handling for duplicate of sentence ending chars
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

def getModels():
    
    modelList = []
    response = requests.get(endpoint+'//v1/projects/dit825/models/', headers={'Authorization': 'Bearer '+getToken()}).json()
    
    print(response)
    try:
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
        file = open(cwd+"\modelSettings.json", "r")
        data = json.load(file)
        TOKEN = data['token']
        file.close()
    except:
        print("Failed to access token from json file: modelSettings.json")
    return TOKEN

def saveEvaluation(model_evaluation):
    now = datetime.now()
    
    new_Evaluation = ModelEvaluation(
        version_name = model_evaluation['model'],
        date_evaluated = now.strftime("%d/%m/%Y, %H:%M:%S"), # dd/mm/YY H:M:S format
        true_positive = model_evaluation['true_positive'],
        true_negative = model_evaluation['true_negative'],
        false_positive = model_evaluation['false_positive'],
        false_negative = model_evaluation['false_negative']
    )

    new_Evaluation.save()

def retrieveLatestEvaluation(queriedModel):
    try:
        modelMatchs = ModelEvaluation.objects.get(model = queriedModel)
        latestEntry = {}
        for entry in modelMatchs:
            if latestEntry == {}:
                latestEntry = entry
            elif entry['date_evaluated'] > latestEntry['date_evaluated']:
                latestEntry = entry
        return latestEntry
    except:
        print("No elaluations found for the specified model")


