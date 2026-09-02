# 🔬 Code Review Agent — Day 05 of 14 AI Agents in 14 Days

Paste source code and get engineering-focused review comments.

Day **05** of a "14 AI Agents in 14 Days" build.

- **Live demo:** _(added once deployed — see the portfolio card)_
- **Stack:** Python · OpenAI (`gpt-5.6`) · Gradio · FastAPI · Cloud Run
- **Security:** see [SECURITY.md](SECURITY.md)

## Run locally

```bash
git clone https://github.com/amol-d/code-review-agent.git
cd code-review-agent
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then edit .env and set OPENAI_API_KEY
python app.py               # serves on http://localhost:8080
```

The OpenAI key is read from the environment by the SDK — never committed, logged,
or sent to the browser.

## Deploy to Google Cloud Run

```bash
gcloud run deploy code-review-agent \
  --source . --region asia-south1 --allow-unauthenticated \
  --set-secrets "OPENAI_API_KEY=OPENAI_API_KEY:latest" \
  --set-env-vars "^@^ALLOWED_EMBED_ORIGINS=https://amoldesai.in,https://www.amoldesai.in,https://amoldesai-portfolio.web.app"
```

## License

[MIT](LICENSE)
