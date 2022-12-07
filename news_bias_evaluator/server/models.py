from django.db import models

# Model for enrty
class Entry(models.Model):
    sentence = models.TextField(primary_key=True)
    news_link = models.CharField(max_length=200)
    outlet = models.CharField(max_length=20)
    topic = models.CharField(max_length=20)
    political_type = models.CharField(max_length=10)
    group_id = models.IntegerField()
    num_sent = models.IntegerField()
    label_bias = models.CharField(max_length=10)
    label_opinion = models.CharField(max_length=50)
    article = models.TextField()
    # Bias words added as a textfield as SQlite does not support array's.
    # This will have to be seperated using a regex function if we contiune with SQlite
    bias_words = models.TextField()
    
    # Returned when a particular entry is quaried
    def __str__(self):
        return self.sentence
