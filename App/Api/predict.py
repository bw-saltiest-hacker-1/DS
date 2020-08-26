# Importing necessary libraries
import logging
from fastapi import APIRouter
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator
from App.Api.model import *
import sqlite3
import random
from random import randint
# import viz


log = logging.getLogger(__name__)
router = APIRouter()


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""
    comment_author : str = Field(..., example='marshray')
    # Potential code
    comment_author: str = Field(..., example='marshray')

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    # Potential code
    # @validator('comment_id')
    # def comment_id_must_be_positive(cls, value):
    #     """Validate that comment_id is a positive number."""
    #     assert value > 0, f'comment_id == {value}, must be > 0'
    #     return value

# get path - to read data
# @router.get('/hn_db.db') 
#     return {'Top 10 most popular commenters rated by saltiness': randint(1, 100)}
# @router.get('/hn_db.db')
#     return {'Top 10 most popular commenters': randint(1, 100)}


@router.post('/predict')
async def predict(item: Item):
    """Make random baseline predictions for classification problem"""
    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()
    SQL_Query = pd.read_sql_query('''
                                  SELECT comment_author, comment_text, sentiment
                                  FROM hn_comments
                                  LIMIT 100
                                  ''', conn)
    df = pd.DataFrame(SQL_Query, columns=['comment_author', 'comment_text', 'sentiment'])
    df = preprocessing(df)
    sentiment_analysis(df)

    hn_rank = df.copy()
    df_test = hn_rank.groupby(['comment_author', 'sentiment']).size().unstack(fill_value=0)
    df_test['Saltiness'] = df_test['Negative'] - df_test['Positive']
    df_test = df_test.drop(['Negative','Positive'], axis=1)
    df_test = df_test.sort_values(by='Saltiness', ascending=False)
    df_final = df.merge(df_test, how='inner', on='comment_author').drop(column=['sentiment'])
    # y_pred = sentiment_analysis(item.comment.id)
    # return {'prediction': y_pred} 
    # y_pred = comment_sentiment(item.comment.id)
    # return {'prediction': y_pred}
    result = df.to_json()
    # breakpoint()
    return result

