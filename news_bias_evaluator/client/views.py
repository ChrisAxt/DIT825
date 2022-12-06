from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, 'client/index.html')

def results(request):
    
    text_input = request.GET['input-text'] # retrieve the text input from form 

    sentences = {text_input,}

    # creates a context (dictionary mapping variables to HTML variables)
    context = {
        'sentences': sentences
    }
    return render(request, 'client/results.html', context)