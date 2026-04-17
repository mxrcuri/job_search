# Internship Search Backend

A powerful FastAPI-based backend for searching and matching internships. It features automated job scraping from top ATS platforms, cron-based scheduling, real-time alerts, and AI-powered resume matching.

## 🚀 Features

- **Automated Scraping**: Periodically scrapes job boards from Greenhouse, Lever, and Workday.
- **AI Resume Matching**: Uses Hugging Face embeddings to match your resume against job descriptions with semantic precision.
- **Cron Scheduling**: Background jobs run every 24 hours to keep the database fresh.
- **Real-time Alerts**: Notifications sent to users when new jobs matching their profile are detected.
- **Secure Authentication**: JWT-based auth for user profiles and saved jobs.

## 🛠 Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Scheduling**: [APScheduler](https://apscheduler.readthedocs.io/)
- **AI/ML**: [Hugging Face Inference API](https://huggingface.co/inference-api) for embeddings
- **Mailing**: `fastapi-mail` (Configured for Gmail/SMTP)
- **Scraping**: `BeautifulSoup4` & `Requests`

## 📦 Setup Instructions

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=your_postgres_url
   SECRET_KEY=your_secret_key
   HF_TOKEN=your_huggingface_api_token
   ```
4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧠 AI Matching Logic

The matching system works by:
1. Converting the resume text into a high-dimensional vector using `sentence-transformers`.
2. Doing the same for job titles and descriptions.
3. Calculating the **Cosine Similarity** between the resume vector and job vectors to find the best matches.

## 📅 Scheduler & Alerts

The system uses `APScheduler`'s `BackgroundScheduler` to run the `run_scraper` task daily. When new jobs are added, the `alerts.process_alerts` logic triggers notifications to registered users.
