# ReelSnap Backend 🎬

Production-ready Flask API for downloading Instagram Reels, Stories, and Audio.

---

## 📁 Project Structure

```
reelsnap-backend/
│
├── app/
│   ├── __init__.py          ← App factory (creates Flask app)
│   ├── routes/
│   │   ├── download.py      ← All /api/download/* endpoints
│   │   └── health.py        ← GET /api/health
│   ├── services/
│   │   └── downloader.py    ← yt-dlp logic (only place!)
│   ├── middlewares/
│   │   └── rate_limiter.py  ← IP-based rate limiting
│   └── utils/
│       ├── validators.py    ← URL validation
│       └── response.py      ← Standardised JSON responses
│
├── config/
│   └── settings.py          ← All config from .env
│
├── run.py                   ← Dev entry point
├── Procfile                 ← For Render.com / Heroku
├── render.yaml              ← Render.com auto-deploy config
├── requirements.txt         ← All Python dependencies
├── .env.example             ← Copy to .env and fill values
└── .gitignore
```

---

## 🚀 Local Setup

```bash
# 1. Clone / unzip the project
cd reelsnap-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your values

# 5. Run development server
python run.py
```

Server starts at: `http://localhost:5000`

---

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Download Reel
```
POST /api/download/reel
Content-Type: application/json

{ "url": "https://www.instagram.com/reel/ABC123/" }
```

### Download Audio
```
POST /api/download/audio
Content-Type: application/json

{ "url": "https://www.instagram.com/reel/ABC123/" }
```

### Download Story/Status
```
POST /api/download/story
Content-Type: application/json

{ "url": "https://www.instagram.com/stories/username/123/" }
```

### Response Format (all endpoints)
```json
{
  "success": true,
  "message": "Reel fetched successfully.",
  "data": {
    "title": "Video title",
    "thumbnail": "https://...",
    "duration": 30,
    "uploader": "username",
    "best_url": "https://cdn.instagram.com/video.mp4",
    "formats": [
      { "url": "...", "quality": "720p", "ext": "mp4", "type": "video" },
      { "url": "...", "quality": "480p", "ext": "mp4", "type": "video" }
    ]
  },
  "error": null
}
```

---

## ☁️ Deploy to Render.com (Free)

1. Push this code to a **GitHub repo**
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` → click **Deploy**
5. Your API is live at: `https://reelsnap-backend.onrender.com`

> **Free tier note:** Server sleeps after 15 min inactivity.
> Use [UptimeRobot](https://uptimerobot.com) (free) to ping `/api/health` every 5 min to keep it awake.

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | — | Flask secret (change this!) |
| `FLASK_ENV` | `production` | `development` or `production` |
| `FLASK_DEBUG` | `False` | Enable debug mode |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `5000` | Server port |
| `ALLOWED_ORIGINS` | `*` | CORS allowed origins |
| `RATE_LIMIT` | `10` | Max requests per minute per IP |

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Language |
| Flask | Web framework |
| yt-dlp | Instagram media extraction |
| flask-cors | CORS handling |
| gunicorn | Production WSGI server |
| python-dotenv | Environment variable loading |
