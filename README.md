# 🌟 AI Quote Generator

A personalized AI-powered motivational quote generator built with Flask, OpenRouter AI, and PostgreSQL. Users can enter a theme to receive uniquely generated quotes, which are stored and displayed in a dashboard.

> 🚀 This project was built as part of the AltSchool x PipeOps Cloud Engineering challenge.

---

## 🧠 Features

- 🎯 Personalized quote generation using OpenRouter (AI)
- 💾 Quote history stored in a database (PostgreSQL on PipeOps)
- 📋 Copy-to-clipboard functionality
- 🖼️ Responsive layout

---

## 📁 Project Structure

```
quotes-ai-api/
├── app/
│   ├── __init__.py       # App factory, config, DB init
│   ├── models.py         # SQLAlchemy DB models
│   ├── routes.py         # Flask routes and logic
│   └── templates/
│       └── index.html    # Main dashboard
├── instance/
│   └── quotes.db         # Local SQLite DB (dev only)
├── migrations/           # Alembic DB migrations
├── run.py                # Entry point to start the Flask app
├── requirements.txt      # Python dependencies
├── Procfile              # Web process declaration for deployment
├── .env                  # Environment variables (never push to GitHub)
└── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions

### 🔧 Local Development

1. **Clone the repo**

```bash
git clone https://github.com/AdetokunAdenike/quotes-ai-api.git
cd quotes-ai-api
```

2. **Create and activate virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** with the following:

```env
OPENROUTER_API_KEY=your_openrouter_key
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///instance/quotes.db
```

5. **Run the application**

```bash
flask run
```

Then go to `http://localhost:5000`

---

## 🛠️ Deployment with PipeOps

PipeOps allows deploying both your **PostgreSQL database** and **Flask app** on the same server using internal networking.

### ✅ Deployment Checklist

- Set `DATABASE_URL` to the PostgreSQL URI provided by PipeOps
- Add all environment variables on PipeOps dashboard
- Push code to GitHub and link it to PipeOps
- Add a `Procfile` with:
  ```
  web: gunicorn run:app
  ```

---

## 🔐 Environment Variables

| Key                 | Description                          |
|---------------------|--------------------------------------|
| `OPENROUTER_API_KEY` | API key from [OpenRouter.ai](https://openrouter.ai) |
| `SECRET_KEY`         | Flask session secret key             |
| `DATABASE_URL`       | Database URI (PostgreSQL in production) |

---

## 🤝 Contributing

Feel free to fork this repo and contribute! Issues and PRs welcome.

---

## 🧠 Credits

- [OpenRouter](https://openrouter.ai) – AI API
- [Flask](https://flask.palletsprojects.com/) – Python web framework
- [PipeOps](https://pipeops.io) – Deployment platform

---

## 📜 License

MIT License. Use freely, contribute widely.

---

## 👩🏽‍💻 Author

**Adenike Adetokun**  
[GitHub Profile](https://github.com/AdetokunAdenike)