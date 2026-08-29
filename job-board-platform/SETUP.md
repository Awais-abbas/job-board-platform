# Setup Instructions

## Installation & Setup Guide

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Generate Dummy Data (Optional but Recommended)

```bash
cd backend
python generate_dummy_data.py
```

This creates sample users, jobs, profiles, and applications for testing.

### Step 3: Start the Backend Server

```bash
cd backend
python run.py
```

The API will be available at: http://localhost:5000

### Step 4: Open Frontend in Browser

Open `frontend/index.html` in your web browser

Alternatively, run a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
```

Then visit: http://localhost:8000

### Step 5: Test the Application

**Test Accounts (from dummy data):**

**Job Seeker:**
- Email: john@example.com
- Password: Password123

**Recruiter:**
- Email: recruitment@company.com
- Password: Password123

---

## Project Structure

```
job-board-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Flask app factory
│   │   ├── models/
│   │   │   └── data_models.py    # Data models & storage
│   │   ├── routes/
│   │   │   ├── auth.py           # Authentication routes
│   │   │   ├── users.py          # User profile routes
│   │   │   ├── jobs.py           # Job listing routes
│   │   │   ├── applications.py   # Application routes
│   │   │   └── recommendations.py # ML recommendations
│   │   ├── ml/
│   │   │   └── recommendation_engine.py  # TF-IDF ML engine
│   │   └── utils/
│   │       ├── auth_utils.py     # Password hashing, validation
│   │       └── cv_utils.py       # CV parsing utilities
│   ├── data/                      # JSON data files
│   ├── uploads/                   # User uploaded CVs
│   ├── config.py                  # Configuration
│   ├── run.py                     # Main entry point
│   ├── requirements.txt           # Dependencies
│   └── generate_dummy_data.py    # Dummy data generator
├── frontend/
│   ├── index.html                 # Main HTML file
│   └── assets/
│       ├── css/
│       │   ├── style.css          # Main styles
│       │   └── responsive.css     # Mobile responsive
│       └── js/
│           ├── app.js             # Core app logic
│           ├── auth.js            # Authentication
│           ├── jobs.js            # Jobs management
│           └── dashboard.js       # Dashboard logic
└── README.md
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user
- `GET /api/auth/check` - Check authentication status

### Users
- `GET /api/users/<user_id>` - Get user profile
- `PUT /api/users/<user_id>` - Update user profile
- `POST /api/users/<user_id>/upload-cv` - Upload CV
- `GET /api/users/search` - Search users

### Jobs
- `GET /api/jobs` - Get all jobs (with filters)
- `GET /api/jobs/<job_id>` - Get job details
- `POST /api/jobs` - Post new job (Recruiter)
- `PUT /api/jobs/<job_id>` - Update job (Recruiter)
- `DELETE /api/jobs/<job_id>` - Delete job (Recruiter)
- `GET /api/jobs/posted` - Get recruiter's posted jobs

### Applications
- `POST /api/applications` - Apply for job
- `GET /api/applications/user` - Get user's applications
- `GET /api/applications/job/<job_id>` - Get job applications (Recruiter)
- `GET /api/applications/<app_id>` - Get application details
- `PUT /api/applications/<app_id>/status` - Update status (Recruiter)

### Recommendations
- `GET /api/recommendations/personalized` - Get personalized job recommendations
- `GET /api/recommendations/for-job/<job_id>` - Get recommended candidates for job
- `POST /api/recommendations/update-engine` - Update recommendation engine

---

## Features

### Implemented
✓ User registration & authentication
✓ Profile management (Job seekers & Recruiters)
✓ Job posting & management
✓ Job applications
✓ CV upload & parsing
✓ ML-based job recommendations (TF-IDF similarity)
✓ Skill matching algorithm
✓ Experience level matching
✓ Responsive frontend design
✓ Session-based authentication

### To Do / Production Ready
- [ ] MongoDB Atlas integration
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Job application status tracking UI
- [ ] Recruiter job recommendations (top candidates)
- [ ] File upload validation & security
- [ ] Rate limiting & API security
- [ ] Unit tests & integration tests
- [ ] CI/CD pipeline
- [ ] Docker containerization

---

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: JSON (→ MongoDB Atlas)
- **ML**: scikit-learn (TF-IDF + Cosine Similarity)
- **Authentication**: PBKDF2-SHA256 password hashing

---

## Configuration

Edit `backend/config.py` to customize:
- Flask app settings
- File upload limits
- Session configuration
- CORS settings
- Data file locations

---

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Run: `pip install -r requirements.txt` again
- Check if port 5000 is available

**Frontend won't load:**
- Ensure backend is running first
- Check CORS settings in config.py
- Open browser console for errors

**Dummy data not loading:**
- Run: `python generate_dummy_data.py` from backend directory
- Check if data/ directory has JSON files

---

## Next Steps for Production

1. **Setup MongoDB Atlas**: Replace JSON storage with MongoDB
2. **Add Authentication**:  JWT tokens instead of sessions
3. **Email Service**: Send notifications for applications/updates
4. **Search Engine**: Elasticsearch for advanced job search
5. **Caching**: Redis for better performance
6. **Testing**: Unit & integration tests
7. **Deployment**: Docker + AWS/Heroku
8. **Monitoring**: Logging & error tracking

---

Built as a comprehensive final year project.
