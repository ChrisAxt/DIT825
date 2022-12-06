from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, 'client/index.html')

def results(request):
    
    text_input = request.GET['input-text'] # retrieve the text input

    sentences = {text_input,}
    context = {
        'sentences': sentences
    }
    return render(request, 'client/results.html', context)