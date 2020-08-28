import nltk
import pandas as pd
import re, string
import random

from nltk.tag import pos_tag 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier
from sklearn.model_selection import train_test_split

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

hn_df = pd.read_csv('cleaned_comments.csv')

df = hn_df.copy()

positive_words = ['good','great', 'love', 'cool', 'nice', 'useful', 'excited', 'happy', 'fantastic', 'amazing', 'spectacular', 'beauitful']
negative_words = ['bad', 'wrong', 'cant', 'ridiculous', 'problem', 'dont', 'horrible', 'terrible', 'shit', 'idiot', 'stupid', 'trash']

positive_columns = []
negative_columns = []

for i, word in enumerate(positive_words):
  df[f'positive{i}'] = df['comment_text'].str.contains(word)
  positive_columns.append(f'positive{i}')

for i, word in enumerate(negative_words):
  df[f'negative{i}'] = df['comment_text'].str.contains(word)
  negative_columns.append(f'negative{i}')

pos_dfs = {}

for column in positive_columns:
  pos_dfs[column] = df[df[column] == True]

positive = []

for column in positive_columns:
  positive.append(pos_dfs[column])

hn_positive = pd.concat(positive).reset_index(drop=True)

neg_dfs = {}

for column in negative_columns:
  neg_dfs[column] = df[df[column] == True]

negative = []

for column in negative_columns:
  negative.append(neg_dfs[column])

hn_negative = pd.concat(negative).reset_index(drop=True)

hn_pos_comments = hn_positive['comment_text']
hn_neg_comments = hn_negative['comment_text']


def tokenize(comments):

    text = comments.str.replace('[^A-z ]','').str.replace(' +',' ').str.strip()

    split_words = [nltk.word_tokenize(str(words)) for words in text]

    return split_words


pos_tokens = tokenize(hn_pos_comments)
neg_tokens = tokenize(hn_neg_comments)

def remove_noise(comment_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(comment_tokens):
        token = re.sub('http[s]?(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 2 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


stop_words = stopwords.words('english')

#cleaned_tokens_all = []

#for tokens in comment_tokens:
    #cleaned_tokens_all.append(remove_noise(tokens, stop_words))

#def get_all_words(cleaned_tokens_all):
    #for tokens in cleaned_tokens_all:
        #for token in tokens:
            #yield token

#all_words = get_all_words(cleaned_tokens_all)

#freq_words = FreqDist(all_words)

#print(freq_words.most_common(300))

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in pos_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in neg_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


def get_comments_for_model(cleaned_tokens_list):
    for comment_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in comment_tokens)

positive_tokens_for_model = get_comments_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_comments_for_model(negative_cleaned_tokens_list)


positive_dataset = [(comment_dict, "Positive")
                     for comment_dict in positive_tokens_for_model]

negative_dataset = [(comment_dict, "Negative")
                     for comment_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:73124]
test_data = dataset[73124:]

classifier = NaiveBayesClassifier.train(train_data)

print('Accuracy is:', classify.accuracy(classifier, test_data))

print(classifier.show_most_informative_features(10))

#These two lines will take a comment and return whether it is positive or negative, must go in model.py 'sentiment analysis' function
custom_tokens = remove_noise(word_tokenize(comment))

classifier.classify(dict([token, True] for token in custom_tokens))