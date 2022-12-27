from googleapiclient import discovery
from app.utils import getCurrentDateTime
from google.api_core.client_options import ClientOptions
import os


def getStatus(job_name):
    project_name = 'dit825'
    project_id = 'projects/{}'.format(project_name)
    cloudml = discovery.build('ml', 'v1')
    request = cloudml.projects().jobs().get(name='projects/dit825/jobs/'+job_name)
    # Execute and retreive the response from the training request 
    print('making request...')
    response = request.execute()
    return response