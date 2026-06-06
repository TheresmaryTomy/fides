# ✝️ Fides - Catholic AI Companion

A faithful and trustworthy AI companion for Catholics, grounded in Church
teaching via a RAG pipeline.

## What is Fides?

Fides (Latin for _faith_) is an AI-powered companion that helps Catholics with:

- ✝️ Questions about Catholic teaching and the Catechism
- 📖 Scripture references and explanations
- 🙏 Prayer guidance and daily reflections
- 👼 Saints and their stories
- 👨‍👩‍👧 Raising children in the faith

Fides is designed to be **trustworthy and grounded** - always citing sources,
always pointing to God first, and always reminding users that it is a companion,
not a replacement for their priest, their Bible, or their prayer life.

## How it works

Fides uses a **RAG (Retrieval Augmented Generation)** pipeline:

1. Catholic documents (Catechism, Scripture, Vatican docs) are chunked and
   stored in a ChromaDB vector database
2. When a user asks a question, the most relevant chunks are retrieved
3. Claude (Anthropic) generates a response grounded in those documents
4. Every answer cites its source - CCC paragraph numbers, scripture references

This architecture prevents hallucination and ensures trustworthy,
source-grounded responses.

## Pastoral philosophy

Fides follows a deliberate response hierarchy inspired by
_Magnifica Humanitas_ (Pope Leo XIV, 2026):

| Situation                        | Fides responds with         |
| -------------------------------- | --------------------------- |
| Personal / emotional / spiritual | Warmth → Prayer → Scripture |
| Doctrinal question               | Scripture → CCC citation    |
| Factual Church question          | CCC → Scripture             |
| Conscience / discernment         | Warmth → Prayer → Priest    |
| Off-topic                        | Gentle redirect             |

## Tech stack

- **Python** - core application
- **Streamlit** - web interface
- **Claude (Anthropic API)** - AI model
- **ChromaDB** - local vector database
- **Sentence Transformers** - embeddings
- **RAG pipeline** - grounded in Catholic documents

## Getting started

```bash
# Clone the repository
git clone https://github.com/TheresmaryTomy/fides.git
cd fides

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install streamlit anthropic chromadb sentence-transformers python-dotenv

# Add your API key
echo ANTHROPIC_API_KEY=your_key_here > .env

# Ingest Catholic documents
python rag/ingest.py

# Run Fides
streamlit run streamlit_app.py
```

## Roadmap

- [x] Basic Q&A with local LLM
- [x] Streamlit web interface
- [x] RAG pipeline with Catechism documents
- [x] Claude API integration
- [x] Pastoral response hierarchy
- [ ] Full Catechism + Bible ingestion
- [ ] Deployed web app
- [ ] Liturgical calendar integration
- [ ] Daily prayer and reflection feature

## Why I built this

As a practicing Catholic and new mom, I wanted a tool that could help me
and my family stay connected to the faith - answering questions accurately,
suggesting prayers, and explaining Church teaching simply and honestly.

This project also reflects my belief that AI should be built responsibly,
with trustworthiness and domain expertise at its core - in the spirit of
_Magnifica Humanitas_.

## Author

**Theresmary Tomy** - AI Engineer | Masters in AI |
Building purposeful, trustworthy AI

[GitHub](https://github.com/TheresmaryTomy)
