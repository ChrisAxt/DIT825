import subprocess
from app.utils import getCurrentDateTime
import time

def deploy_model():

    date_time = getCurrentDateTime("%s")

    deploy_command = "gcloud ai-platform versions create simple_model_{} --model=simple_model --region=europe-west4 --runtime-version=1.15 --python-version=3.7 --framework=tensorflow --origin=gs://example_bucket_v2-aiproject-dit825/simple_model".format(date_time)

    return subprocess.run(deploy_command, capture_output=True, shell=True)