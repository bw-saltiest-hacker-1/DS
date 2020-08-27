from fastapi import APIRouter, HTTPException
import pandas as pd
import sqlite3
# import plotly.express as px

router = APIRouter()


@router.get('/viz/')  # check the documentation, assistance with router
async def viz():

    def salt_rank():
        """
        Querying the database for commenter, text, and sentiment for the text.

        Parameters:
        -----------
        mode: string. query mode.  returning the sentiment based on negative or positive

        Output:
        -----------
        results: json format string with format 
                {"sentiment": str,
                "author_comment_count": str,
                "comment_text": string,
                }
        """
        conn = sqlite3.connect('hn_db.db')

        # if conn.closed != 0:
        #     return app.response_class(response=json.dump({}),
        #                               status=400,
        #                               mimetype='application/json')
        curs = conn.cursor()

        # sql_mode = dict({"average": "AVG", "total": "SUM"})

        query = f'''
                SELECT comment_author, comment_text, sentiment
                FROM hn_comments
                LIMIT 100;
                '''
        curs.execute(query)
        data = curs.fetchall()
        # return data
