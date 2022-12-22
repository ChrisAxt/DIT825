from app.models import Article, LabeledSentence


import csv

# Script to extract a cleaned version of the dataset (unnecessary columns and rows removed)
# If necessary we can modify this to extract the data from the original dataset
def run():
    with open('app/assets/media_bias_dataset.csv', errors="ignore") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        # Delete all entries from the database
        print("Deleting all items in database \n")
        Article.objects.all().delete()
        print("Done")
        # Itterate over each row in the csv file
        count = 0;
        print("Processing CSV \n")
        for row in reader:
                        
            # Extract the data at the relevent positions
            new_article = Article(
                news_link=row[1],
                outlet=row[2],
                topic=row[3],
                political_type=row[4],
                article=row[9],
               )
            """ print("article: \n", new_article) """
            new_article.save()

            new_sentence = LabeledSentence(
                sentence=row[0],
                bias_words=row[10],
                label_bias=row[7],
                label_opinion=row[8],
                article = new_article,
            )
            new_sentence.save()
            count += 1
            print("Added rows: ", count)
            # Save each entry to the database
            



