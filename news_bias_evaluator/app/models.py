from django.db import models
from django.contrib.postgres.fields import ArrayField 
import datetime

# Helper methods to creates choices for years and date values.
def current_date():
    '''
    returns the current date
    '''
    return datetime.date.today()

def current_year():
    '''
    returns the current year
    '''
    return datetime.date.today().year

def possible_years():
    '''
    returns a list of choices for publication years
    Starting date is arbitrary
    Inspired by: https://stackoverflow.com/questions/49051017/year-field-in-django
    '''
    return [(r,r) for r in range(1984, current_year)]


# MODELS

class Article(models.Model):
    '''
    Schema for an article. 
    It contains some attributes that will be used by the model but that are related to the article and not the sentence. 
    Use foreign key to retreive those attributes.
    '''
    news_link = models.TextField(primary_key=True)
    article = models.TextField()
    outlet = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    political_type = models.CharField(max_length=50)
    pub_year = models.IntegerField(null=True)
    add_date = models.DateField(default=current_date)
    
        # Returned when a particular article is queried



class LabeledSentence(models.Model):
    '''
    Schema for labeled sentences
    To retrieve articles that have not their sentences labeled, we can query the DB
    Is contected via foreign key to an article. This allows granularity when querying DB based on date, etc.
    We can also retrieve the entire article to give context to the sentence, allowing more advanced training in the future. 
    '''
    sentence = models.TextField(primary_key=True)
    label_bias = models.CharField(max_length=50)
    label_opinion = models.CharField(max_length=50)
    bias_words = models.TextField(blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  #if an article is deleted, the sentence will be deleted as well
    
    # Returned when a particular sentence is queried


class ModelEvaluation(models.Model):
    '''
    Schema for model evaluation. 
    '''

    version_name = models.CharField(max_length=100, primary_key=True)
    date_evaluated = models.DateField()
    true_positive = models.IntegerField()
    true_negative = models.IntegerField()
    false_positive = models.IntegerField()
    false_negative = models.IntegerField()
