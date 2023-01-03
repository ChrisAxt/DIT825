from app.models import Article, LabeledSentence
from app.utils import *

import csv

# Script to add the pseudo labelled data to the database
def run():
    with open('app/assets/pseudo_labelled.csv', errors="ignore") as file:
        reader = csv.DictReader(file, delimiter=',')

        # Iterate over each row in the csv file
        valid_count = 0;
        invalid_count = 0;
        print("Processing CSV \n")
        for row in reader:

            # Extract the data at the relevent positions
            # TODO: Find a way to check if header is present to be able to use only 1 script to load data

            news_link = row['news_link']
            outlet=row['outlet']
            sentence=row['sentence']
            label_bias=row['label']
            pub_year = row['pub_year']

            # checks if data extracted is valid
            if(is_valid_news_link(news_link) and is_non_empty_sentence(sentence) and is_valid_label_bias(label_bias)):
                
                # creates an article
                new_article = Article(
                    news_link=news_link,
                    outlet=outlet,
                    pub_year=pub_year,
                )
                new_article.save()

                # creates a sentence
                new_sentence = LabeledSentence(
                    sentence=sentence,
                    label_bias=convert_label_bias(label_bias), # converts the label_bias to number format
                    article = new_article,
                )
                new_sentence.save()
                valid_count += 1
                print("Added rows: ", valid_count)
            else:
                invalid_count += 1

        print("Total valid rows: ", valid_count)
        print("Total invalid rows: ", invalid_count)
                  



