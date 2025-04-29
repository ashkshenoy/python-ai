from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re
import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import string
import random

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

# CORS setup
origins = ["http://localhost:3000"]  # React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AIPostRequest(BaseModel):
    title: str
    content: str

class AIPostResponse(BaseModel):
    title: str
    summary: str
    tags: List[str]

# Summarize function
def summarize_text(text, max_sentences=2):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    freq = defaultdict(int)
    for word in words:
        if word not in stop_words:
            freq[word] += 1
    ranking = {}
    for i, sent in enumerate(sentences):
        for word in word_tokenize(sent.lower()):
            if word in freq:
                ranking[i] = ranking.get(i, 0) + freq[word]
    ranked_sentences = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    selected_indices = sorted([i for i, _ in ranked_sentences[:max_sentences]])
    return ' '.join([sentences[i] for i in selected_indices])

# Generate Tags Function Using spaCy
def generate_tags(text):
    # Process the text with spaCy to get entities, nouns, and adjectives
    doc = nlp(text)
    tags = set()

    # Extract named entities (persons, organizations, places)
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'GPE', 'PERSON']:  # Filtering by relevant entities
            tags.add(ent.text)

    # Extract nouns and adjectives as additional potential tags
    for token in doc:
        if token.pos_ in ['NOUN', 'ADJ'] and len(token.text) > 2:
            tags.add(token.text.lower())

    # Convert the set to a list
    tags = list(tags)

    # Fallback if no tags found
    if not tags:
        tags = ["General"]

    random.shuffle(tags)
    return tags[:5]

# Routes
@app.post("/summarize")
def summarize(req: AIPostRequest):
    summary = summarize_text(req.content)
    return {"summary": summary}

@app.post("/generate-tags")
def generate_tags_route(req: AIPostRequest):
    tags = generate_tags(req.content)
    return {"tags": tags}

@app.post("/generate", response_model=AIPostResponse)
def generate_post(request: AIPostRequest):
    # Simple summary generator: take the first sentence
    summary = re.split(r'(?<=[.!?]) +', request.content.strip())[0]

    # Generate tags based on content
    tags = generate_tags(request.content)

    # Fallback if no tags found
    if not tags:
        tags = ["General"]

    return {
        "title": request.title,
        "summary": summary,
        "tags": tags
    }
