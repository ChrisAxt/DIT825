import subprocess
from app.utils import getCurrentDateTime
import time

def deploy_model():

    # define the date/time in seconds since epoch for the new version name
    date_time = getCurrentDateTime("%s")

    # define new version creation command.
    deploy_command = "gcloud ai-platform versions create simple_model_{} --model=simple_model --region=europe-west4 --runtime-version=1.15 --python-version=3.7 --framework=tensorflow --origin=gs://example_bucket_v2-aiproject-dit825/simple_model".format(date_time)

    # run the command and return the response.
    return subprocess.run(deploy_command, capture_output=True, shell=True), 'simple_model_{}'.format(date_time)