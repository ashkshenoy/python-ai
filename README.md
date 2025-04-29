# python-ai

# 🧠 Blog AI Microservice — FastAPI NLP Tool

A standalone Python microservice built with **FastAPI** to power smart content features in the Blog Platform. It uses **spaCy** and **NLTK** to provide real-time content summarization and tag generation.

---

## 🚀 Features

- ✂️ Text summarization (extractive)
- 🏷️ Auto tag generation using:
  - Named entities (ORG, GPE, PERSON)
  - Nouns and adjectives
- JSON API with 3 main endpoints

---

## 📦 Tech Stack

- **FastAPI** — Lightweight web API framework
- **spaCy** — NLP for tag extraction
- **NLTK** — Summarization + tokenization
- **pydantic** — Request/response validation
- **CORS** — Enabled for React frontend

---

## 🔄 Endpoints

| Method | Endpoint         | Description                     |
|--------|------------------|---------------------------------|
| POST   | `/summarize`     | Summarizes blog content         |
| POST   | `/generate-tags` | Suggests tags based on content |
| POST   | `/generate`      | Returns both summary + tags     |

---

## 🧪 Running the Service

### 1. Install dependencies

```bash
pip install fastapi uvicorn spacy nltk
python -m nltk.downloader punkt stopwords
python -m spacy download en_core_web_sm

Start the server
  uvicorn main:app --reload

Service will be live at http://localhost:8000.


Integration Notes

    The main Spring Boot backend connects to this microservice for blog enhancements.

    React frontend triggers it via POST requests from the UI.

📁 File Structure

ai-service/
├── main.py         # FastAPI application


🛠️ Future Enhancements

    GPT-assisted title rewriting
    Language detection and translation
    Model fine-tuning for tag accuracy

📜 License

Free to use for educational or personal projects.
