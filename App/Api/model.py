from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np


def preprocessing(df):
    '''
    This function generates the columns necessary to
    house the sentiment analysis data.
    '''
    df = df[:]
    df = df[df['comment_text'].notna()]
    df['neg'], df['neu'], df['pos'], df['compound'] = [
        np.nan, np.nan, np.nan, np.nan]
    return df


def sentiment_analysis(df):
    '''
    This function takes a dataframe and runs sentiment analysis
    on each of the text cells to give outputs into the dataframe.
    The returns are positive, negative, and neutral as a percent,
    and compound which is a metric for running MAE or other numerical
    regression modeling.
    '''
    # Ensure preprocess has happened.
    df = df[:]
    df['neg'], df['neu'], df['pos'], df["compound"] = [
        np.nan, np.nan, np.nan, np.nan]
    # Instantiate the analyzer.
    sid_obj = SentimentIntensityAnalyzer()
    # Loop over the DF texts.
    for i, row in df.iterrows():
        comment = row['comment_text']
        returned_sentiment = sid_obj.polarity_scores(comment)
        for polarity in returned_sentiment:
            df.at[i, polarity] = returned_sentiment[polarity]
