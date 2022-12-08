from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .utils import extractSentences, sendRequest


def main(request):
    return render(request, 'client/main.html')

def onSubmit(request):
    text_input = request.GET['input-text'] # retrieve the text input from form 
    sentenceList = extractSentences(text_input)
    if(len(sentenceList) > 0):
        predictionList = sendRequest(sentenceList)

    if (len(sentenceList) > 0 & len(sentenceList) == len(predictionList)):
        result = {sentenceList, predictionList}

    # creates a context (dictionary mapping variables to HTML variables)
    context = {
        'result': result
    }

    return render(request, 'client/results.html', context)


