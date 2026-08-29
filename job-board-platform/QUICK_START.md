# Quick Start Guide - Job Board Platform

## 🚀 Start Backend & Frontend in 2 Minutes

### Step 1: Start Backend Server
```bash
cd backend
python run.py
```
✓ Backend running at: `http://localhost:5000`

### Step 2: Start Frontend Development Server (New Terminal)
```bash
cd frontend
npm install  # First time only
npm run dev
```
✓ Frontend running at: `http://localhost:3000`

## 🧪 Test with Dummy Data

### Auto-Generated Test Accounts:

**Job Seeker:**
- Email: `john@example.com`
- Password: `Password123`
- Skills: Python, Django, Flask, SQL
- Experience: 3 years

**Recruiter:**
- Email: `recruitment@company.com`
- Password: `Password123`

## 📋 What You Can Do

### Job Seeker:
1. Register/Login
2. Update profile with bio, location, skills
3. Upload CV - system extracts skills automatically
4. Browse all job listings with filters
5. See AI-powered personalized job recommendations (based on CV/profile match)
6. Apply for jobs
7. Track applications in dashboard

### Recruiter:
1. Register as recruiter
2. Post job listings with skills requirements
3. See applications for posted jobs
4. View candidate recommendations for each job
5. Manage job listings (active/closed status)

## 🤖 ML Recommendation System

The system uses **TF-IDF + Cosine Similarity** to:
- Recommend jobs to job seekers based on their CV/profile
- Recommend top candidates to recruiters for each job
- Calculate skill match percentages (0-100%)
- Consider experience level requirements

**Example Match Factors:**
- Matched skills: ✓ Python, Django
- Missing skills: ✗ Kubernetes
- Overall match: 75% (Skills: 80% + Experience: 70%)

## 📁 Project Structure

```
├── backend/           # Flask API
│   ├── app/
│   │   ├── routes/   # API endpoints
│   │   ├── models/   # Data models
│   │   ├── ml/       # ML engine
│   │   └── utils/    # Helpers
│   ├── data/         # JSON database
│   └── run.py        # Start server
│
└── frontend/          # React + Tailwind
    ├── src/
    │   ├── pages/    # Page components
    │   ├── components/
    │   └── App.jsx
    └── package.json
```

## 🛠️ Generate Fresh Dummy Data

```bash
cd backend
python generate_dummy_data.py
```

Sample data includes:
- 2 job seekers
- 2 recruiters
- 5 job listings
- 3 applications

## 🔧 Common Issues

**Backend won't start:**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Or if specific errors:
pip install Flask==2.3.2 flask-cors PyPDF2 scikit-learn numpy
```

**Frontend issues:**
```bash
# Clear node_modules and reinstall
rm -r node_modules package-lock.json
npm install
npm run dev
```

**Can't connect Frontend to Backend:**
- Ensure backend is running on `http://localhost:5000`
- Check Vite proxy config in `frontend/vite.config.js`
- Check browser console for CORS errors

## 📚 API Examples

```javascript
// Login
fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  credentials: 'include',
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'Password123'
  })
})

// Get personalized recommendations
fetch('http://localhost:5000/api/recommendations/personalized', {
  credentials: 'include'
})

// Apply for job
fetch('http://localhost:5000/api/applications', {
  method: 'POST',
  credentials: 'include',
  body: JSON.stringify({ job_id: 1 })
})
```

## 🎨 Tech Stack

- **Backend**: Flask, scikit-learn, PyPDF2
- **Frontend**: React 18, Tailwind CSS, Vite
- **Data**: JSON (easily migrate to MongoDB Atlas)
- **Auth**: Session-based (upgrade to JWT for production)

## 📈 Next Steps

1. **Test full flow**: Register → Upload CV → Get recommendations
2. **Create more jobs**: Post jobs as recruiter
3. **Monitor logs**: Check console output for debugging
4. **Production setup**: Replace JSON with MongoDB Atlas, add JWT auth
5. **Deployment**: Docker + AWS/Heroku

## 💡 Tips

- Check browser DevTools console for errors
- Check terminal output for backend logs
- API is CORS-enabled and accepts credentials
- All passwords hashed with PBKDF2-SHA256
- Dummy data is generated fresh each time you run the script

---

**Ready to test?** Just run the two commands and navigate to `http://localhost:3000`! 🎉
