# Importing necessary libraries
import logging
from fastapi import APIRouter
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator
from App.Api.model import preprocessing, sentiment_analysis
# from model import preprocessing, sentiment_analysis
import sqlite3
# import static database as dataframe
# from App.Api.update_db import db_as_df
# from update_db import db_as_df
# import App.Api.viz


log = logging.getLogger(__name__)
router = APIRouter()


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

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


@router.get('/salty')
async def predict(num: int = 1000):
    """Returns 1,000 saltiest Hacker News commenters, default 1,0000."""

    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()
    query = ("""
        SELECT comment_author, saltiness
        FROM hn_users
        ORDER BY saltiness ASC;
        """)
    df = pd.read_sql(sql=query, con=conn)

    # Subset dataframe
    df = df[:num]

    # Change index to comment_author
    df = df.set_index(keys='comment_author')

    # Return dataframe as a JSON object whose keys are comment_author
    # and whose values are the corresponding saltiness
    return df.to_json(orient='index')
