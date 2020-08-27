from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from App.Api import predict, viz

app = FastAPI(
    title='Who is the Saltiest Hacker?',
    description="""Identifying and ranking negative commenters on 
    Hacker News using sentiment analysis.""",
    version='0.1',
    docs_url='/',
)

app.include_router(predict.router)
app.include_router(viz.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
