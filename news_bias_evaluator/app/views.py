import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import extractSentences, sendRequest, getModels
from app.retraining_utils import training_handler, training_job_monitor, database_bucket_sync
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from django.http import JsonResponse
import os

from app.templatetags.evaluation import getBatchPrediction, saveEvaluationData

cwd = os.getcwd()  # Get the current working directory (cwd)
from .models import Request, Prediction

dashboard_context = {}

# Views for user side

def main(request):
    return render(request, 'app/main.html')

def onSubmit(request):

    items = {}
    file = open(cwd+"/modelSettings.json", "r")
    data = json.load(file)
    file.close()

    text_input = request.GET['input-text'] # retrieve the text input from form
    model_name = data['name'] 
    print("Model name: " + model_name)
    sentenceList = extractSentences(text_input)

    # Saves the request into the DB
    user_request = Request(request_content = text_input)
    user_request.save()
    
    if(len(sentenceList) > 0):
        predictionList = sendRequest(sentenceList, model_name)

        # Saves the prediction in the DB, using the request
        prediction = Prediction (request = user_request, prediction = predictionList)
        prediction.save()

        # Update the status of the request to processed since we received a prediction (allows to have easy stats on reliability)
        user_request.processed = True
        user_request.save
        
    try:
        if (len(sentenceList) > 0 and len(sentenceList) == len(predictionList)):
            items = {sentenceList[i]: predictionList[i][0] for i in range(len(sentenceList))}
    except:
        messages.error(request, "Failed to get a response from the selected model!")

    # creates a context (dictionary mapping variables to HTML variables)
    context = {
        'resultList': items
    }

    return render(request, 'app/results.html', context)

def onModelChange(selected_model):
    isUpdated = False

    with open(cwd+'/modelSettings.json', errors="ignore") as file:
        data = json.load(file)
        file.close()
        print(data)

    data["name"] = selected_model

    file = open(cwd+'/modelSettings.json', "w")
    json.dump(data, file)
    if (data['name'] == selected_model):
        isUpdated = True
    file.close()

    return isUpdated

# views for admin side
@login_required # decorator redirecting to the login page defined in settings.py if no user is logged in
def dispatch(request):
        return redirect('app:dashboard')

def log(request):
    '''
    Method rendering the login page
    '''
    return render(request, 'app/login.html')

def log_out(request):
    logout(request)
    return redirect('app:main')
 
def access_dashboard(request):
    '''
    method that process a login request.
    If the user is found with the right credentials, it redirects to the dashboard
    in other cases, it returns to the login page and a message to the user is created.
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        # Retrieve all info to be displayed in the dashboard
        
        # list of models. Need to be added in this variable
        model_list= getModels()
        if(len(model_list) == 0):
            messages.error(request, "Failed to connect to google cloud!")

        print(model_list)
        # generates the graph using matplotlib here more info -> https://medium.com/@mdhv.kothari99/matplotlib-into-django-template-5def2e159997
        
        img_uri = 'some_parsed_uri'

        context = {
            'models': model_list,
            'img': img_uri,            
        }
        dashboard_context = context

        return render(request, "app/dashboard.html", context)
    else:
        messages.info(request, 'Incorrect password or username.')
        return redirect('app:login')

@login_required
def process_admin_request(request):
    type_of_request = request.POST.get('action-selection')
    selected_model = request.POST.get('model-options')
    print(type_of_request)
    print(selected_model)

    if(type_of_request == 'evaluate'):
       context = {
            'evaluation' : process_evaluation_request()
       }
       return render(request, 'app/evaluation.html', context)
    elif(type_of_request == 'retrain'):
        # make sure latest simple_model is retrained
        print('entering retrain')
        #try:
        # Sync database and cloud bucket
        database_bucket_sync.sync_db_and_bucket()
        # This execution will initiate the training job, it DOES NOT
        # wait for a successful/failed training job!
        training_response, job_name = training_handler.runTrainingJob()
        print('exited retrain job')            # Pass via a context.
        print(training_response)
        return render(request, 'app/retrain.html', {'job_name': job_name})
        #except Exception as err:  
        #    print('inside error')
        #    print(err)
        #    return redirect('app:main')
    elif(type_of_request == 'use-selected'):
        if(onModelChange(selected_model)):
            messages.success(request, 'Model successfully changed!')
        else:
            messages.error(request, 'Failed to change the model!')

        return render(request, "app/dashboard.html", dashboard_context) 
    else:
        return redirect('app:main')

@sync_to_async
@login_required
@async_to_sync
async def get_training_status(request):
    job_name = request.GET.get('job_name', None) 
    status_response = training_job_monitor.getStatus(job_name)
    print(status_response)
    # insert data from ai platform here.
    return JsonResponse(status_response)
    

def process_evaluation_request():
    data = getBatchPrediction()
    saveEvaluationData(data)
    return data

