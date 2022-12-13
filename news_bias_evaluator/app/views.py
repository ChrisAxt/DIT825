from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .utils import extractSentences, sendRequest


def main(request):
    return render(request, 'app/main.html')

def onSubmit(request):
    text_input = request.GET['input-text'] # retrieve the text input from form 
    sentenceList = extractSentences(text_input)
    if(len(sentenceList) > 0):
        predictionList = sendRequest(sentenceList)

    if (len(sentenceList) > 0 and len(sentenceList) == len(predictionList)):
        items = {sentenceList[i]: predictionList[i][0] for i in range(len(sentenceList))}

    # creates a context (dictionary mapping variables to HTML variables)
    context = {
        'resultList': items
    }

    return render(request, 'app/results.html', context)
