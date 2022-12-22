from django.contrib import admin
from app.models import Article, LabeledSentence

# Register your models here.
admin.site.register(Article)
admin.site.register(LabeledSentence)
