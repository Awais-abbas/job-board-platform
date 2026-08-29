# Job Recommendation System & Job Board Platform

A fully-functional job board platform with ML-powered job recommendations based on CV/resume analysis.

## Features

### For Job Seekers
- User registration and profile creation
- CV/Resume upload and parsing
- View and search job listings
- Apply for jobs
- AI-powered personalized job recommendations
- Application history and tracking

### For Recruiters
- Company registration and profile setup
- Post and manage job listings
- View applicant profiles
- Track applications
- Review candidate CVs

### ML Recommendation System
- Parses and analyzes uploaded CVs
- Extracts skills, experience, and qualifications
- Recommends relevant jobs based on profile match
- Continuous model improvement with data

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React 18 + Tailwind CSS 3
- **Build Tool**: Vite
- **Data Storage**: JSON (will migrate to MongoDB Atlas)
- **ML**: scikit-learn (TF-IDF + Cosine Similarity)
- **CV Parsing**: Custom PDF text extraction

## Project Structure

```
job-board-platform/
├── backend/
│   ├── app/
│   │   ├── models/        # Data models
│   │   ├── routes/        # API endpoints
│   │   ├── ml/            # ML recommendation engine
│   │   ├── utils/         # Helper functions
│   │   └── __init__.py
│   ├── data/              # JSON data files
│   ├── uploads/           # User uploaded CVs
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   └── generate_dummy_data.py
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Generate dummy data (optional)**:
   ```bash
   python generate_dummy_data.py
   ```

3. **Run the backend server**:
   ```bash
   python run.py
   ```
   API will be available at: `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```
   Frontend will be available at: `http://localhost:3000`

3. **Build for production**:
   ```bash
   npm run build
   ```
2. **Run the application**:
   ```bash
   python run.py
   ```

3. **Access the frontend**:
   - Open `frontend/index.html` in your browser or run a local server

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout
+ Cosine Similarity for job recommendations
- All passwords are hashed using PBKDF2-SHA256
- Frontend uses React 18 with Tailwind CSS for modern, responsive UI
- `GET /api/users/<user_id>` - Get user profile
- `PUT /api/users/<user_id>` - Update profile
- `POST /api/upload-cv` - Upload CV
- `GET /api/jobs` - Search jobs
- `POST /api/applications` - Apply for job
- `GET /api/recommendations` - Get job recommendations

### Recruiter
- `POST /api/jobs` - Post a job
- `GET /api/jobs/posted` - Get posted jobs
- `PUT /api/jobs/<job_id>` - Update job
- `DELETE /api/jobs/<job_id>` - Delete job
- `GET /api/applications/<job_id>` - Get job applications

## Database Schema

See `backend/data/schema.txt` for complete data structure documentation.

## Notes

- Currently uses JSON for data storage
- Will be migrated to MongoDB Atlas
- ML models use TF-IDF vectorization for job recommendations
- All passwords are hashed using bcrypt

## Author

Built for final year project
