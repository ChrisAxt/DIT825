from app.models import Article, LabeledSentence
from app.utils import is_valid_news_link, is_valid_label_bias, is_non_empty_sentence
import pandas as pd
import csv

# Script to extract a cleaned version of the dataset (unnecessary columns and rows removed)
# If necessary we can modify this to extract the data from the original dataset
def run():
    with open('app/assets/media_bias_dataset.csv', errors="ignore") as file:
        reader = csv.DictReader(file, delimiter=',')

        # Delete all entries from the database
        print("Deleting all items in database \n")
        Article.objects.all().delete()
        print("Done")
        # Itterate over each row in the csv file
        valid_count = 0;
        invalid_count = 0;
        print("Processing CSV \n")
        for row in reader:
            
            # Extract the data at the relevent positions
            # TODO: Find a way to check if header is present to be able to use only 1 script to load data
            news_link = row['news_link']
            outlet=row['outlet']
            topic=row['topic']
            political_type=row['type']
            article=row['article']
            sentence=row['sentence']
            bias_words=row['biased_words']
            label_bias=row['Label_bias']
            label_opinion=row['Label_opinion']

            if is_non_empty_sentence(sentence) and is_valid_label_bias(label_bias) and is_valid_news_link(news_link):
                new_article = Article(
                    news_link = news_link,
                    outlet = outlet,
                    topic = topic,
                    political_type = political_type,
                    article = article,
                    # -> dummy date to differenciate initial dataset from other ones. If commented out, -> default value
                    # add_date = '2022-11-01' 
                )
                new_article.save()

                new_sentence = LabeledSentence(
                    sentence=sentence,
                    bias_words=bias_words,
                    label_bias=label_bias,
                    label_opinion=label_opinion,
                    article = new_article,
                )
                new_sentence.save()
                valid_count += 1
                print("Added rows: ", valid_count)
            else: 
                invalid_count += 1
        print("Total valid rows: ", valid_count)
        print("Total invalid rows: ", invalid_count)    



