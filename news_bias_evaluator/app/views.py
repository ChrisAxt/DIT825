from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import extractSentences, sendRequest


# Views for user side

def main(request):
    return render(request, 'app/main.html')

def onSubmit(request):
    text_input = request.GET['input-text'] # retrieve the text input from form
    model_name = request.GET['slected_model'] 
    sentenceList = extractSentences(text_input)
    if(len(sentenceList) > 0):
        predictionList = sendRequest(sentenceList, model_name)

    if (len(sentenceList) > 0 and len(sentenceList) == len(predictionList)):
        items = {sentenceList[i]: predictionList[i][0] for i in range(len(sentenceList))}

    # creates a context (dictionary mapping variables to HTML variables)
    context = {
        'resultList': items
    }

    return render(request, 'app/results.html', context)



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
        model_list= [
                {'name': 'model1'},
                {'name': 'model2'}
        ]

        # generates the graph using matplotlib here more info -> https://medium.com/@mdhv.kothari99/matplotlib-into-django-template-5def2e159997
        
        img_uri = 'some_parsed_uri'

        context = {
            'models': model_list,
            'img': img_uri,            
        }

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
       return render(request, 'app/evaluation.html')
    elif(type_of_request == 'retrain'):
        return render(request, 'app/retrain.html')
    else:
        return redirect('app:main')
    
