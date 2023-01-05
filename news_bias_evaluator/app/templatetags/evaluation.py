from django import template
from app.models import LabeledSentence
from django.http import JsonResponse
import os
import json

from app.utils import sendRequest, getModelVersion, saveEvaluation, getPredictionArrays

register = template.Library()
simpleModel = {'name': 'projects/dit825/models/simple_model'}

@register.simple_tag
def getBatchPrediction(selected_model):
    # Cant slice with - value: ie [-50:]
    # Solution reverses the query set, and then gets the first 50
    # which is the same as the last 50 entries in the non-reversed
    # queryset
    
        dataPoints = LabeledSentence.objects.all().reverse()[:50]
        sentenceList = [data.sentence for data in dataPoints]
        if("bert" in selected_model):
            sentenceList = getPredictionArrays(sentenceList)
        currentModel = selected_model 
        evaluationResults = sendRequest(sentenceList, currentModel)

        results = {}
        results = {dataPoints[i].sentence: { 'true_value' : dataPoints[i].label_bias, 'predicted_value' : evaluationResults[i][0]} for i in range(len(sentenceList))}

        evaluationResults = getEvaluationResults(results, currentModel)
        return evaluationResults
    

@register.simple_tag
def saveEvaluationData(data):
        evaluation = { 'name': getLatestModelVersion(simpleModel), 'true_positive': data['true_positive'], 'false_positive': data['false_positive'], 'false_negative': data['false_negative'], 'true_negative': data['true_negative']}
        #print(evaluation)
        saveEvaluation(evaluation)
   
@register.simple_tag
def getLatestModelVersion(model):
    # Change this to get the latest simple model, not current model
    models = [model]
    modelList = getModelVersion(models)
    latestVersion = ""
    for version in modelList:
        if latestVersion == "":
            latestVersion = version
        else:
            LVtimestamp = latestVersion[latestVersion.find("/versions/simple_model_") + 23:len(latestVersion)]
            Vtimestamp = version[version.find("/versions/simple_model_") + 23: len(version)]
            print(LVtimestamp)
            if(Vtimestamp > LVtimestamp):
                latestVersion = version

    return latestVersion


@register.simple_tag
def getEvaluationResults(results, currentModel):
    TN = 0
    TP = 0
    FP = 0
    FN = 0
    for result in results.items():
        if (result[1]['true_value'] == '1'): 
            if (result[1]['predicted_value'] < 0.5):
                TP += 1
            else: FN += 1
        elif (result[1]['true_value'] == '0'):
            if (result[1]['predicted_value'] >= 0.5):
                TN += 1
            else: FP += 1
    return {'true_positive':TP, 'true_negative':TN, 'false_positive': FP, 'false_negative': FN, 'model': currentModel}

@register.simple_tag
def getAccuracy(evaluation):
    total = evaluation['true_positive'] + evaluation['false_positive'] + evaluation['true_negative'] + evaluation['false_negative']
    accuracy = (evaluation['true_positive'] + evaluation['true_negative']) / total
    return f"{accuracy * 100:.2f}"

@register.simple_tag
def getPrecision(evaluation):
    precision = evaluation['true_positive'] / (evaluation['false_positive'] + evaluation['true_positive'])
    return f"{precision * 100:.2f}"

@register.simple_tag
def getNegPrecision(evaluation):
    precision = evaluation['true_negative'] / (evaluation['true_negative'] + evaluation['false_negative'])
    return f"{precision * 100:.2f}"

@register.simple_tag
def getRecall(evaluation):
    recall = evaluation['true_positive'] / (evaluation['true_positive'] + evaluation['false_negative'])
    return f"{recall * 100:.2f}"

@register.simple_tag
def getF1(evaluation):
    precision = float(getPrecision(evaluation))
    recall = float(getRecall(evaluation))
    f1 = (2 * (precision * recall) / (precision + recall))
    return f"{f1 :.2f}"