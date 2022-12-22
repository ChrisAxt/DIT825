# Dockerfile adapted from: https://cloud.google.com/ai-platform/training/docs/train-ml-model-custom-containers https://towardsdatascience.com/training-your-ml-model-using-google-ai-platform-and-custom-environment-containers-1531888cac3d

FROM python:3



# Copy requirements.txt 
COPY credentials.json requirements.txt /root/

# Create directories for the app
WORKDIR /root

# Install requirement.txt libraries
RUN pip install -r requirements.txt

# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /root/tools/google-cloud-sdk/.install/.backup

# Path configuration
ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
#RUN echo '[GoogleCompute]\nservice_account = 637648471463-compute@developer.gserviceaccount.com' > /etc/boto.cfg
#RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg
#COPY credentials.json ./root/
#RUN gcloud auth activate-service-account --key-file=./root/credentials.json
#CMD gcloud auth login
# Copies the trainer code 
RUN mkdir /root/trainer
COPY toy_model_trainer.py /root/trainer/toy_model_trainer.py

# NOTE: if move this to django project, authentication may not be needed when deployed!
RUN gcloud auth login --cred-file=/root/credentials.json && \
    gcloud config set project 'dit825'

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "trainer/toy_model_trainer.py"]

# Deploy the trained model. 

# Created this manually:
#gcloud ai-platform models create toy_model --regions us-central1

#RUN gcloud ai-platform versions create --model toy_model --region europe-west4 --runtime-version 1.15 --python-version 3.7 --framework --origin "gs://example_bucket_v2-aiproject-dit825/"
