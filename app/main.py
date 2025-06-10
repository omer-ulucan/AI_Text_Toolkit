from fastapi import FastAPI
from transformers import pipeline
from contextlib import asynccontextmanager

from app.routers import simplify, summarize, paraphrase, sentiment

app = FastAPI(title="Modular NLP Microservice")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.simplify_pipeline = pipeline(
        "text2text-generation", model="t5-small"
    )
    app.state.summarize_pipeline = pipeline(
        "summarization", model="facebook/bart-large-cnn"
    )
    app.state.paraphrase_pipeline = pipeline(
        "text2text-generation", model="ramsrigouthamg/t5_paraphraser"
    )
    app.state.sentiment_pipeline = pipeline(
        "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    yield

app = FastAPI(
    title="Modular NLP Microservice",
    lifespan=lifespan
)

app.include_router(simplify.router)
app.include_router(summarize.router)
app.include_router(paraphrase.router)
app.include_router(sentiment.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Modular NLP Microservice!"}