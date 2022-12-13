from google.api_core.client_options import ClientOptions
from googleapiclient import discovery

def extractSentences(text_input):

    sentenceList = []
    firstIndex = 0
    text_input = text_input.strip()

    if (text_input != ""):
        for i in range(0, len(text_input)):
            if (text_input[i] == "." or text_input[i] == "?" or text_input[i] == "!"):
                sentence = text_input[firstIndex:i+1]
                sentenceList.append(sentence.strip())
                firstIndex = i+1
            else:
                sentenceList.append(text_input)
                
    return sentenceList
        
def sendRequest(sentenceList):

    endpoint = 'https://europe-west4-ml.googleapis.com'
    client_options = ClientOptions(api_endpoint = endpoint)
    ml = discovery.build('ml', 'v1', client_options=client_options)

    request_body = {'instances' : sentenceList}
    prediction_request = ml.projects().predict(
        name='projects/dit825/models/dit825_model_v1', body = request_body)
    
    response = prediction_request.execute()
    print("Predictions: ", response['predictions'])
    return response['predictions'] 
