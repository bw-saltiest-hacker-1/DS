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
async def get_salt(num: int = 1000):
    """Returns saltiest Hacker News commenters, default 1,0000."""

    if num < 1:
        return 'Number of commenters must be positive.'
    elif num > 28591:
        return f"""There are only 28591 commenters in this database. Please choose a smaller number."""
    else:
        pass
    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()
    saltiness_query = ("""
        SELECT comment_author, saltiness, rankings
        FROM hn_users
        ORDER BY saltiness ASC;
        """)
    saltiness_df = pd.read_sql(sql=saltiness_query, con=conn)

    # Make a shallow copy
    saltiness_df = saltiness_df[:]

    # Subset dataframe
    saltiness_df = saltiness_df[:num]

    # Change index to comment_author
    saltiness_df = saltiness_df.set_index(keys='comment_author')

    # JSON response object
    author_saltiness_rank = saltiness_df.to_json(orient='index')

    # GET COMMENT TEXT
    comments_query = ("""
    SELECT comment_author, comment_text
    FROM hn_comments
    ORDER BY comment_author;
    """)

    comments_df = pd.read_sql(sql=comments_query, con=conn)

    # Make a shallow copy
    comments_df = comments_df[:]

    # Return dataframe as a JSON object whose keys are comment_author
    # and whose values are the corresponding saltiness

    # JSON response object
    author_comments = comments_df.to_json()

    # Return Json users, Json comment
    return author_saltiness_rank, author_comments
