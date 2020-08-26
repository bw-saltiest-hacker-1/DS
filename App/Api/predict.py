import logging
from fastapi import APIRouter
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator
from app.api.model import *
import sqlite3
import random
from random import randint

log = logging.getLogger(__name__)
router = APIRouter()

class Item(BaseModel):
    """Use this data model to parse the request body JSON."""
    # Potential code
    comment_author : str = Field(..., example='marshray')

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
#     return {'Top 10 most popular commenters': randint(1, 100)}

@router.post('/predict')
async def predict(item: Item):
    """Make random baseline predictions for classification problem"""
    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()
    SQL_Query = pd.read_sql_query(''' SELECT comment_author, comment_text FROM hn_comments ''',conn)
    df = pd.DataFrame(SQL_Query, columns=['comment_author', 'comment_text'])
    df = preprocessing(df)
    sentiment_analysis(df)
    # y_pred = comment_sentiment(item.comment.id)
    # return {'prediction': y_pred} 
    result = df.to_json()
    # breakpoint()
    return randint(1, 100)