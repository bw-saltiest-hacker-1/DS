"""Code to add hn_users table with comment_author and their saltiness
to database of Hacker News comments."""
import sqlite3
import pandas as pd
from App.Api.model import preprocessing, sentiment_analysis   # For app deployment
# from model import preprocessing, sentiment_analysis     # For testing locally

# Run once, save to databsae, and changes will persist


def update_db(db='hn_db.db', table_name='hn_users'):
    """
    Generates dataframe from SQLite3 query of all rows in database.
    Makes and adds SQL table to sqlite3 database passed in.
    Returns dataframe.

    Default database is hn_db.db, default table_name is hn_users.
    """

    conn = sqlite3.connect(db)
    curs = conn.cursor()
    df = pd.read_sql(
        """SELECT comment_author, comment_text, sentiment
        FROM hn_comments""", conn)

    df = preprocessing(df)
    df = sentiment_analysis(df)
    hn_rank = df.copy()

    # Make separate columns for df[sentiment] values: Positive and Negative
    df_test = hn_rank.groupby(
        ['comment_author', 'sentiment']).size().unstack(fill_value=0)
    df_test['saltiness'] = df_test['Positive'] - df_test['Negative']
    df_test = df_test.drop(['Positive', 'Negative'], axis=1)
    df_test = df_test.sort_values(by='saltiness', ascending=True)

    # If this table already exists, drop it before inserting new values
    df_test.to_sql(name=table_name, con=conn, if_exists='replace')

    # Feature engineer saltiness rankings(1, 2, 3..)
    rankings = []
    for i, _ in enumerate(df_test['saltiness']):
        rankings.append(i+1)


# Add new SQL table to database
db_as_df = update_db()
