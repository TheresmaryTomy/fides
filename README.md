# Fides - Catholic AI Companion 🙏

A faithful and trustworthy AI companion for Catholics — built with Python and local LLM technology.

## What is Fides?

Fides (Latin for _faith_) is an AI-powered companion that helps Catholics with:

- ✝️ Questions about Catholic teaching and the Catechism
- 📖 Scripture references and explanations
- 🙏 Prayer guidance and daily reflections
- 👼 Saints and their stories
- 👨‍👩‍👧 Raising children in the faith

Fides is designed to be **trustworthy and grounded** — always citing sources and always reminding users to consult their priest for matters of conscience.

## Tech Stack

- **Python** — core application
- **Ollama + Gemma3** — local LLM (no data sent to external servers)
- **RAG pipeline** _(coming soon)_ — grounded in the Catechism of the Catholic Church

## Why I Built This

As a practicing Catholic and new mom, I wanted a tool that could help me and my family stay connected to the faith — answering questions quickly, suggesting prayers, and explaining Church teaching simply and accurately.

This project also reflects my belief that AI should be built responsibly, with trustworthiness and domain expertise at its core.

## Getting Started

```bash
# Clone the repository
git clone https://github.com/TheresmaryTomy/fides.git
cd fides

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install ollama python-dotenv

# Pull the AI model
ollama pull gemma3

# Run Fides
python app.py
```

## Roadmap

- [x] Basic Q&A with local LLM
- [ ] Streamlit web interface
- [ ] RAG pipeline with Catechism documents
- [ ] Liturgical calendar integration
- [ ] Daily prayer and reflection feature
- [ ] Deployed web app

## Author

Theresmary Tomy — AI Engineer in the making | Masters in AI | Passionate about building trustworthy, purpose-driven AI

[GitHub](https://github.com/TheresmaryTomy)
