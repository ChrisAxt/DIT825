# How to deploy a model to AI Platform on google cloud

## 1. Save the Model
Model to be saved locally, using the method appropriate for the type of model used. For example, for a keras model, the entire model structure is necessary, so keras uses model.save() or saved_model.save()
```model.save(save_path, save_format='tf')``` or ```saved_model.save(model, save_path)```

Signatures can be created to specify the input and output formats of the model. For example, for a keras model, the input and output formats can be specified as follows:
```signatures = {"serving_default": call, "array_input": module.__call__.get_concrete_function(tf.TensorSpec([None], tf.float32))}```
```tf.saved_model.save(module, save_path, signatures=signatures)```

## 2. AI Platform Model deployment to Google Cloud bucket
First the model will be pushed to the cloud, into a bucket we've created for the purpose.
```gsutil cp -r model/saved_model gs://example_bucket_v2-aiproject-dit825```

## 3. Create a model on AI Platform
Once the model is in the bucket, we can create a model on AI Platform. This can be done in the console, and the model is created with the name of the model, and the path to the model in the bucket. It's useful to specify a unique name for traceability.
```gcloud ai-platform versions create "v1" --model dit825_model_v1 --region europe-west4 --runtime-version 1.15 --python-version 3.7 --framework tensorflow --origin "gs://example_bucket_v2-aiproject-dit825/saved_model"```

## 4. AI Platform Prediction
There exists a python library for AI Platform Prediction, which can be used to make predictions on the model. The library is called google-cloud-aiplatform, and can be installed using pip to test locally. The library can also be used to make predictions on the model, using the following code:
```from google.cloud import aiplatform```
```endpoint = aiplatform.Endpoint('projects/123456789/locations/europe-west4/endpoints/123456789')```
```endpoint.predict(instances=[{"input": "Hello world"}])```
```pip install google-cloud-aiplatform```

AI Pllatform Prediction has a REST API that can be used to make predictions on the model. The library has a method for this, called predict, which takes the model name, the version of the model, and the data to be predicted on. The data is sent as a dictionary, where the key is the name of the input layer of the model, and the value is the data to be predicted on. The data is sent as a list of lists, where each list is a sample to be predicted on. The output is a dictionary, where the key is the name of the output layer of the model, and the value is the prediction for the sample.
```from google.cloud import aiplatform```
