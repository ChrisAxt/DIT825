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
    Model for an article. 
    It contains some attributes that will be used by the model but that are related to the article and not the sentence. 
    Use foreign key to retreive those attributes.
    '''
    news_link = models.CharField(max_length=200, primary_key=True)
    article = models.TextField()
    outlet = models.CharField(max_length=20)
    topic = models.CharField(max_length=20)
    political_type = models.CharField(max_length=10)
    pub_year = models.IntegerField(null=True)
    add_date = models.DateField(default=current_date)
    
        # Returned when a particular article is queried
    def __str__(self):
        return "Article's URL: ", self.news_link


class LabeledSentence(models.Model):
    '''
    Model for labeled sentences
    To retrieve articles that have not their sentences labeled, we can query the DB
    Is contected vie foreign key to an article. This allows granularity when querying DB based on date, etc.
    We can also retrieve the entire article to give context to the sentence, allowing more advanced training in the futur. 
    '''
    sentence = models.TextField(primary_key=True)
    label_bias = models.CharField(max_length=10)
    label_opinion = models.CharField(max_length=50)
    bias_words = ArrayField(models.CharField(max_length=30, blank=True))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, max_length=200)  #if an article is deleted, the sentence will be deleted as well
    
    # Returned when a particular sentence is queried
    def __str__(self):
        return self.sentence
