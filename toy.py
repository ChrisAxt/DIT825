# For N-dimensional array manipulation
import numpy as np

# Plotting library
import matplotlib.pyplot as plt

# For data analysis and data structures in DataFrames
import pandas as pd

# For data visualization
import seaborn as sns

# For machine learning algorithms and evaluation metrics
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Load dataset
df = pd.read_csv("media_bias.csv")

# Print head to see whether load was successful
print(df.head)

# Remove rows where 'Label_bias' is 'No agreement'
df = df[df.Label_bias != "No agreement"]

# Remove rows where 'article' is 'NaN'
df = df[df.article != "NaN"]

# separate the data into dependent and independent variables and only use first 500 rows
X = df["sentence"]
y = df["Label_bias"]

print(X.head)
# Remove
# Replace label with 0, 1
y = y.replace("Biased", 0)
y = y.replace("Non-biased", 1)

# Remove numbers from all strings in X
X = X.str.replace("\d+", "", regex=True)

# Remove punctuation from all strings in X
X = X.str.replace("[^\w\s]", "", regex=True)


# Print feature names from countvectorizer
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
feature_vector = cv.fit(X)  # Fit the Data

# Get the feature names
word = feature_vector.get_feature_names_out()
print("Total number of features: ", len(word))

train_features = cv.transform(X)
type(train_features)

print(train_features.shape)

# Create dataframe from train_features
df_train_features = pd.DataFrame(train_features.toarray(), columns=word)

# Count the amount of times each word appears
word_count = df_train_features.sum(axis=0)

# Create dataframe from word_count
df_word_count = pd.DataFrame(dict(features=word, counts=word_count))
df_word_count.sort_values("counts", ascending=False)[0:15]
print(df_word_count.head(15))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df_train_features, y, test_size=0.2, random_state=42
)

# Fit the model to the data
from sklearn.naive_bayes import BernoulliNB

model = BernoulliNB()
model.fit(X_train, y_train)

# Predict the test set results
y_pred = model.predict(X_test)

# Print classification report
print(metrics.classification_report(y_test, y_pred))

# Print the accuracy score
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# Print the confusion matrix and heatmap
cm = metrics.confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d")
plt.title("Confusion matrix")
plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.show()
