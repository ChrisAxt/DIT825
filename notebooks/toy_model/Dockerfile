FROM alpine:3.6

RUN apk add --update \
python \
curl \
which \
bash

RUN curl -sSL https://sdk.cloud.google.com | bash

ENV PATH $PATH:/root/google-cloud-sdk/bin

WORKDIR /ai_model

ADD . /ai_model

COPY credentials.json prediction.txt  ./ai_model/

# ENV GOOGLE_APPLICATION_CREDENTIALS /ai_model/credentials.json

## Log in to google-cloud and set project
RUN gcloud auth login --cred-file=/ai_model/credentials.json && \
    gcloud config set project 'dit825'

## Add model to the google cloud bucket
# RUN gsutil cp -r /ai_model/model/1 gs://example_bucket_v2-aiproject-dit825

## Add model from bucket to aiplatform
# RUN gcloud ai-platform versions create "v2" --model dit825_model_v1 --region europe-west4 --runtime-version 1.15 --python-version 3.7 --framework tensorflow --origin "gs://example_bucket_v2-aiproject-dit825/1"

## Run prediction to check whether model is successfully uploaded
RUN gcloud ai-platform predict --model=dit825_model_v1 --version=v1 --region=europe-west4 --text-instances=/ai_model/prediction.txt