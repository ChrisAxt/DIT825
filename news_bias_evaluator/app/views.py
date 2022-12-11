from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def main(request):
    return render(request, 'app/main.html')

def results(request):
    
    text_input = request.GET['input-text'] # retrieve the text input from form 

    sentences = {text_input,}

    # creates a context (dictionary mapping variables to HTML variables)
    context = {
        'sentences': sentences
    }
    return render(request, 'app/results.html', context)