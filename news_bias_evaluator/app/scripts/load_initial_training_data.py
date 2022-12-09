from app.models import initialEntry
import csv

# Script to extract a cleaned version of the dataset (unnecessary columns and rows removed)
# If necessary we can modify this to extract the data from the original dataset
def run():
    with open('app/assets/media_bias_dataset.csv', errors="ignore") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        # Delete all entries from the database
        initialEntry.objects.all().delete()

        # Itterate over each row in the csv file
        for row in reader:
            print(row)
            
            # Extract the data at the relevent positions
            entry = initialEntry(
                sentence=row[0],
                news_link=row[1],
                outlet=row[2],
                topic=row[3],
                political_type=row[4],
                group_id=row[5],
                num_sent=row[6],
                label_bias=row[7],
                label_opinion=row[8],
                article=row[9],
                bias_words=row[10],)

            # Save each entry to the database
            entry.save()


