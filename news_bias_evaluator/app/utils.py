from google.api_core.client_options import ClientOptions
from googleapiclient import discovery
import requests

endpoint = 'https://europe-west4-ml.googleapis.com'
TOKEN = 'ya29.a0AX9GBdU4l4g_PQi345s6_6gDV_2o2uOnd5f96PWueAkaKrZJv61DaDxbtCl9K-NBtr-F0IcjmZphoHSNq9b6pIrvhVFMLI9sgHo2HhrMS5g9fEe5lCHYiKpMoZVwGj9L-scjBjGsWD5uzm9VAkqqVicm79w00RhqfhrQEgaCgYKASkSAQASFQHUCsbC5-IAnovy3wMlFUuSe34ENw0173'

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

    client_options = ClientOptions(api_endpoint = endpoint)
    ml = discovery.build('ml', 'v1', client_options=client_options)

    request_body = {'instances' : sentenceList}
    prediction_request = ml.projects().predict(
        name=model_name, body = request_body)
    
    response = prediction_request.execute()
    return response['predictions'] 

def getModels():
    
    response = requests.get('https://europe-west4-ml.googleapis.com//v1/projects/dit825/models/', headers={'Authorization': 'Bearer '+TOKEN}).json()
    print(response)
    return getModelVersion(response['models'])


def getModelVersion(models):

    modelVersionList = []
    for model in models:
        modelName = model['name']
        response = requests.get('https://europe-west4-ml.googleapis.com//v1/'+modelName+'/versions', headers={'Authorization': 'Bearer '+TOKEN}).json()
        for version in response['versions']:
            modelVersionList.append(version['name'])

    return modelVersionList

