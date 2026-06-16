# ✝️ Fides - Catholic AI Companion

A faithful and trustworthy AI companion for Catholics, grounded in Church
teaching via a RAG pipeline.

🔗 **Live app: [fides-catholic-ai.streamlit.app](https://fides-catholic-ai.streamlit.app)**

## What is Fides?

Fides (Latin for _faith_) is an AI-powered companion that helps Catholics with:

- ✝️ Questions about Catholic teaching and the Catechism
- 📖 Scripture references and explanations
- 🙏 Prayer guidance and daily reflections
- 📅 Daily Mass readings and liturgical calendar
- 👼 Saints and their stories
- 👨‍👩‍👧 Raising children in the faith

Fides is designed to be **trustworthy and grounded** - always citing sources,
always pointing to God first, and always reminding users that it is a companion,
not a replacement for their priest, their Bible, or their prayer life.

## How it works

Fides uses a **RAG (Retrieval Augmented Generation)** pipeline:

1. Catholic documents (Catechism, Scripture) are chunked and stored in a
   Pinecone vector database (3,079 chunks)
2. When a user asks a question, the most relevant chunks are retrieved
3. Claude (Anthropic) generates a response grounded in those documents
4. Every answer cites its source - CCC paragraph numbers, scripture references
5. Daily Mass readings are pulled live from USCCB

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
- **Claude Haiku (Anthropic API)** - AI model
- **Pinecone** - cloud vector database (3,079 chunks)
- **Sentence Transformers** - embeddings (all-MiniLM-L6-v2)
- **RAG pipeline** - grounded in Catechism and Scripture
- **USCCB API** - daily Mass readings
- **Catholic Calendar API** - liturgical season and celebrations

## Getting started

```bash
# Clone the repository
git clone https://github.com/TheresmaryTomy/fides.git
cd fides

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API keys to .env
ANTHROPIC_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here

# Upload documents to Pinecone
python rag/upload_to_pinecone.py

# Run Fides
streamlit run streamlit_app.py
```

## Roadmap

- [x] Basic Q&A with local LLM
- [x] Streamlit web interface
- [x] RAG pipeline with Catechism and Bible (3,079 chunks)
- [x] Claude API integration
- [x] Pastoral response hierarchy
- [x] Daily Mass readings from USCCB
- [x] Liturgical calendar integration
- [x] Deployed as live web app
- [ ] Saint of the day from Vatican News
- [ ] Examination of conscience feature
- [ ] Mobile optimisation

## Why I built this

As a practicing Catholic and new mom, I wanted a tool that could help me
and my family stay connected to the faith - answering questions accurately,
suggesting prayers, and explaining Church teaching simply and honestly.

This project also reflects my belief that AI should be built responsibly,
with trustworthiness and domain expertise at its core - in the spirit of
_Magnifica Humanitas_ (Pope Leo XIV, 2026).

## Author

**Theresmary Tomy** - AI Engineer | Masters in AI |
Building purposeful, trustworthy AI

[GitHub](https://github.com/TheresmaryTomy) ·
[LinkedIn](https://linkedin.com/in/theresmary)
