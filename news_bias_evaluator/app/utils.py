from google.api_core.client_options import ClientOptions
from googleapiclient import discovery

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
        
def sendRequest(sentenceList):

    endpoint = 'https://europe-west4-ml.googleapis.com'
    client_options = ClientOptions(api_endpoint = endpoint)
    ml = discovery.build('ml', 'v1', client_options=client_options)

    request_body = {'instances' : sentenceList}
    prediction_request = ml.projects().predict(
        name='projects/dit825/models/dit825_model_v1', body = request_body)
    
    response = prediction_request.execute()
    return response['predictions'] 
