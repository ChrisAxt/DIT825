from googleapiclient import discovery
import errors

# Contains calls for retraining the model.
def runTrainingJob():

    # Setup connection details to the API.
    endpoint = 'https://europe-west4-ml.googleapis.com'
    # Get python representation of the AI platform training services
    cloudml = discovery.build('m1', 'v1')

    # Construct the training job request
    request = cloudml().projects().jobs().create(body=job_spec, parent=project_id)
    try:
        # Execute and retreive the response from the training request 
        response = request.execute()
    except errors.HttpError as err:
        # Print out the error
        print(err)
