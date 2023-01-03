from app.models import Article, LabeledSentence

import csv

# Script to add the pseudo labelled data to the database
def run():
    with open('app/assets/pseudo_labelled.csv', errors="ignore") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        # Iterate over each row in the csv file
        count = 0;
        print("Processing CSV \n")
        for row in reader:
                        
            # Extract the data at the relevent positions
            new_article = Article(
                news_link=row[2],
                outlet=row[3],
               )
            new_article.save()

            new_sentence = LabeledSentence(
                sentence=row[0],
                label_bias=row[5],
                article = new_article,
            )
            new_sentence.save()
            count += 1
        print("Added rows: ", count)
        # Save each entry to the database
            



