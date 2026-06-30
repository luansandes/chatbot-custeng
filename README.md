# Gemini Chatbot on GitHub Pages

This is a bare-minimum chatbot setup:

- `docs/index.html` is the static frontend for GitHub Pages.
- `backend/main.py` is a small FastAPI backend using `google-genai` for local/non-Vercel hosting.
- `api/index.py` is the Vercel Python entrypoint.
- The Gemini API key stays on the backend.
- Requests are rate-limited to 15 per minute per client IP.

## Run Locally

Install backend dependencies:

```powershell
cd backend
pip install -r requirements.txt
```

Set your Gemini API key:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

Start the backend:

```powershell
uvicorn main:app --reload
```

Open `docs/index.html` in your browser.

## Deploy the Backend

Deploy this repo to Vercel or deploy `backend/` to another Python hosting service such as Render, Railway, Fly.io, or Google Cloud Run.

For Vercel, import the repo and keep the project root as the repository root. The included `vercel.json` routes requests to `api/index.py`.

Use this start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Set these environment variables on the backend host:

```text
GEMINI_API_KEY=your_api_key_here
ALLOWED_ORIGINS=https://YOUR_GITHUB_USERNAME.github.io
```

Optional:

```text
GEMINI_MODEL=gemini-2.5-flash
```

## Deploy the Frontend

In `docs/index.html`, replace:

```js
const API_URL = "http://localhost:8000/chat";
```

with your deployed backend URL:

```js
const API_URL = "https://YOUR_BACKEND_URL/chat";
```

Then enable GitHub Pages:

1. Open the GitHub repo settings.
2. Go to Pages.
3. Choose "Deploy from a branch".
4. Select the `main` branch and `/docs` folder.

## Notes

Do not put `GEMINI_API_KEY` in `docs/index.html`. Anything in GitHub Pages is public.
