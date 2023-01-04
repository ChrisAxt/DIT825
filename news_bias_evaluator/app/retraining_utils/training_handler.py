from googleapiclient import discovery
from app.utils import getCurrentDateTime
from google.api_core.client_options import ClientOptions
import os

# Contains calls for retraining the model.
def runTrainingJob():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../trainers/toy_model/credentials.json"

        project_name = 'dit825'
        project_id = 'projects/{}'.format(project_name)
        cloudml = discovery.build('ml', 'v1')

        date_time = getCurrentDateTime("%Y%m%d_%H%M%S")
        training_inputs = {
            "region": "us-central1",
            "masterConfig": {
                "imageUri": "gcr.io/dit825/simple_model_trainer_container:latest"
            }
        }
        job_spec = {'jobId': 'simple_model_train_job_'+date_time, 'trainingInput': training_inputs}
        # Construct the training job request
        request = cloudml.projects().jobs().create(body=job_spec, parent=project_id)
        
        # Execute and retreive the response from the training request 
        print('making request...')
        response = request.execute()
        return response, 'simple_model_train_job_'+date_time
