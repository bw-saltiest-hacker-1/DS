# Importing necessary libraries
import logging
from fastapi import APIRouter
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator
from App.Api.model import preprocessing, sentiment_analysis
import sqlite3
import json


log = logging.getLogger(__name__)
router = APIRouter()


@router.get('/saltiest/')
async def get_saltiest_hackers(num_hackers: int = 10):
    """Returns the saltiest Hacker News commenters, default top 10."""

    if num_hackers < 1:
        return 'Number of commenters must be positive.'
    elif num_hackers > 28591:
        return f"""There are only 28591 commenters in this database. Please choose a smaller number."""
    else:
        pass
    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()

    saltiest_commenters_query = (f"""
        SELECT comment_author, saltiness, rankings
        FROM hn_users
        ORDER BY saltiness ASC
        LIMIT {num_hackers};
        """)

    saltiest_commenters_df = pd.read_sql(
        sql=saltiest_commenters_query, con=conn)

    # Make a shallow copy
    saltiest_commenters_df = saltiest_commenters_df[:]

    # Change index to comment_author
    saltiest_commenters_df = saltiest_commenters_df.set_index(
        keys='comment_author')

    # JSON response object
    saltiest_hackers = saltiest_commenters_df.to_json(orient='index')

    return saltiest_hackers


@router.get('/check/')
async def check_salt(comment_author: str = 'austenallred'):
    """Takes in a specific comment author and returns their saltiness score
    and saltiness ranking. Default username is Lambda School CEO Austen Allred."""

    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()

    # GET COMMENTER SALTINESS AND RANKING
    salt_query = (f"""
    SELECT comment_author, saltiness, rankings
    FROM hn_users
    WHERE comment_author = '{comment_author}'
    LIMIT 1;
    """)

    saltiness_df = pd.read_sql(
        sql=salt_query, con=conn, index_col='comment_author')
    saltiness_df = saltiness_df[:]
    author_saltiness_rank = saltiness_df.to_json(orient='records')

    return author_saltiness_rank


@router.get('/comments/')
async def get_comments(comment_author: str = 'austenallred',
                       num_comments: int = 10):
    """Takes in a specific comment author and returns their comments.
    Default username of Lambda School CEO Austen Allred."""

    conn = sqlite3.connect('hn_db.db')
    curs = conn.cursor()

    # GET COMMENT TEXT
    comments_query = (f"""
    SELECT comment_text
    FROM hn_comments
    WHERE comment_author = '{comment_author}'
    LIMIT {num_comments};
    """)

    comments_df = pd.read_sql(sql=comments_query, con=conn)
    comments_df = comments_df[:]
    author_comments = comments_df.to_json(orient='values')

    return author_comments
