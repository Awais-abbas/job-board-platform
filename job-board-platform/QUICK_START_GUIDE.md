# 🚀 Quick Start - Backend & Frontend Setup

## ✅ Current Status
- ✅ Backend API running on **http://localhost:5000**
- ✅ MongoDB Atlas connected (**onjob** database)
- ✅ Jobs endpoint working (empty database - needs data)
- ✅ Frontend can connect to backend

---

## 📋 Quick Start - 3 Steps

### **Step 1: Start Backend** (Keep running)

**Terminal 1:**
```bash
cd backend
& 'C:\Users\kamra\AppData\Local\Python\bin\python.exe' run.py
```

Expected output:
```
✅ Database indexes created successfully
Successfully connected to MongoDB Atlas: onjob
* Running on http://127.0.0.1:5000
```

**Verify it's working:**
```
http://localhost:5000/api/health  → Should show: status "ok"
http://localhost:5000/api/jobs    → Should show: count 0
```

---

### **Step 2: Start Frontend** (New Terminal)

**Terminal 2:**
```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

**Open browser:** http://localhost:5173

---

### **Step 3: Use the Application**

#### **A. Add Sample Jobs (Required for testing)**

**Option 1: Via API (Recommended)**

```bash
# 1. Register a recruiter
POST http://localhost:5000/api/auth/register
Body: {
    "email": "recruiter@company.com",
    "password": "Password123",
    "role": "recruiter",
    "name": "HR Manager"
}

# 2. Login (get session)
POST http://localhost:5000/api/auth/login
Body: {
    "email": "recruiter@company.com",
    "password": "Password123"
}

# 3. Post a job
POST http://localhost:5000/api/jobs
Body: {
    "title": "Senior React Developer",
    "description": "Looking for experienced React dev",
    "skills_required": ["React", "Node.js"],
    "experience_level": "Senior"
}
```

**Option 2: Via Frontend UI**

1. Go to http://localhost:5173
2. Click "Register"
3. Fill form:
   - Email: `recruiter@company.com`
   - Password: `Password123`
   - Role: **Recruiter**
   - Name: `HR Manager`
4. Click "Create Account"
5. Login with same credentials
6. Click "Post a Job" (or "Recruiter Dashboard")
7. Fill job details and submit

#### **B. View Jobs as Job Seeker**

1. **Register new account:**
   - Go to http://localhost:5173
   - Click "Register"
   - Email: `jobseeker@gmail.com`
   - Password: `Password123`
   - Role: **Job Seeker**
   - Name: `John Doe`

2. **See all jobs:**
   - After login, go to "Jobs" page
   - All jobs posted by recruiters will show here

3. **Apply for jobs:**
   - Click job details
   - Click "Apply Now"

---

## ⚙️ How It Works Together

```
┌─────────────────┐         ┌──────────────────┐         ┌────────────────┐
│                 │         │                  │         │                │
│  Frontend       │ ◄────►  │  Flask Backend   │ ◄────►  │  MongoDB Atlas │
│  (Vite/React)   │ HTTP    │  (http://5000)   │ Wire    │  (onjob db)    │
│  Port 5173      │ API     │  MongoDB Routes  │ Protocol│                │
│                 │         │                  │         │                │
└─────────────────┘         └──────────────────┘         └────────────────┘
```

**Data Flow:**
1. User registers → Frontend sends to Backend → Saved in MongoDB
2. User posts job → Frontend sends POST to Backend → Saved in MongoDB  
3. User views jobs → Frontend fetches from Backend → Retrieved from MongoDB
4. User updates profile → Frontend PATCH to Backend → Updated in MongoDB

---

## 🔧 Troubleshooting

### **Problem: "Cannot fetch jobs" on frontend**
- ✅ Backend running? Check: `http://localhost:5000/api/health`
- ✅ MongoDB connected? Health should show `"status": "connected"`
- ✅ Jobs empty? Add sample data using methods above
- ✅ CORS error? Already enabled - no changes needed

```bash
# Test if backend responds
Invoke-WebRequest -Uri 'http://localhost:5000/api/jobs' -UseBasicParsing
```

### **Problem: "Cannot connect to MongoDB"**
Seen in backend console like:
```
MongoDB Connection Failed: ...
Falling back to JSON storage
```

**Solutions:**
1. Check internet connection
2. Whitelist your IP in MongoDB Atlas:
   - Go to https://cloud.mongodb.com
   - Access Control → Network Access
   - Add IP: `0.0.0.0/0` (for testing only)
3. Verify credentials in `.env`:
   ```
   MONGODB_URI=mongodb://kamranAK:hggqOSoptchg1VYk@...
   USE_MONGODB=true
   ```

### **Problem: Frontend shows old/demo data instead of MongoDB data**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- MongoDB may be using old seed data

---

## 📝 API Endpoints - For Testing

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check backend & MongoDB status |
| `/api/auth/register` | POST | Register new account |
| `/api/auth/login` | POST | Login (creates session) |
| `/api/jobs` | GET | Fetch all jobs |
| `/api/jobs` | POST | Post new job (recruiter only) |
| `/api/jobs/{id}` | GET | Get job details |
| `/api/users/{id}` | GET | Get user profile |
| `/api/users/{id}` | PUT | Update user profile |

---

## 🎯 Complete Workflow - Step by Step

### **Scenario: Recruiter posts job → Job seeker applies**

**TIME: 0 min - Start everything**
```bash
# Terminal 1: Backend
cd backend
& 'C:\Users\kamra\AppData\Local\Python\bin\python.exe' run.py

# Terminal 2: Frontend
cd frontend  
npm run dev
```

**TIME: 2 min - Register Recruiter**
- Go to http://localhost:5173
- Register: `recruiter@company.com` / `Password123` / Role: Recruiter
- Login

**TIME: 4 min - Post 3 Jobs**
- Click "Post a Job"
- Job 1: Senior React Dev, Salary: $100k-150k, Skills: [React, TypeScript]
- Job 2: Python Backend Dev, Salary: $80k-120k, Skills: [Python, FastAPI]
- Job 3: Full Stack Dev, Salary: $90k-140k, Skills: [React, Node.js, MongoDB]

**TIME: 6 min - Register Job Seeker** (New browser/incognito)
- Go to http://localhost:5173
- Register: `jobseeker@gmail.com` / `Password123` / Role: Job Seeker
- Login

**TIME: 8 min - Browse & Apply**
- Go to "Jobs" page
- See all 3 jobs listed
- Click job details
- Click "Apply Now"
- Check "Applications" in sidebar

**TIME: 10 min - Recruiter Views Applications**
- Switch back to recruiter browser
- Go to "Recruiter Dashboard"
- View applications for each job
- Review candidate profiles

---

## 📦 Features Currently Working

| Feature | Status | Details |
|---------|--------|---------|
| **User Registration** | ✅ | Job Seeker & Recruiter roles |
| **User Login** | ✅ | Session-based authentication |
| **View Jobs** | ✅ | Real-time from MongoDB |
| **Post Jobs** | ✅ | By recruiters only |
| **Job Filtering** | ✅ | Search, location, type, category |
| **View Job Details** | ✅ | Full job info + recruiter contact |
| **Apply for Jobs** | ✅ | Job seeker can apply |
| **Application Tracking** | ✅ | View your applications |
| **User Profile** | ⚠️ | Update partially working |
| **CV Upload** | ⚠️ | Upload working, parsing needs test |
| **Recommendations** | ⚠️ | Not fully wired to MongoDB |

---

## 🔐 Important Notes

### **Security (Development Only)**
⚠️ Your MongoDB password is in `.env` and `.backend/config.py`:
```
mongodb://kamranAK:hggqOSoptchg1VYk@ac-zm1w0v6-...
```

**For production:**
- Use environment variables only
- Change MongoDB password
- Restrict IP whitelist to specific servers
- Use HTTPS
- Add rate limiting

### **Database Info**
- Database: `onjob` (MongoDB Atlas)
- Collections: `users`, `jobs`, `applications`, `profiles`, `resumes`
- Currently: Empty (add test data to use)

### **File Storage**
- Uploads: `backend/uploads/` folder
- CVs: Stored locally, path saved in MongoDB
- Max size: 16MB

---

## ✨ What's Next (After Testing)

1. **Add more test data** to see the app in action
2. **Fix remaining routes** (users.py completely done, need: applications.py, recommendations.py)
3. **Deploy to production** (change security settings, use environment variables)
4. **Create additional features** (notifications, advanced filtering, etc.)

---

## 📞 Help Commands

```bash
# Check if ports are in use
netstat -ano | findstr :5000  # Backend
netstat -ano | findstr :5173  # Frontend

# Kill stuck backend process (if needed)
taskkill /PID {pid_number} /F

# Check backend logs (if running in foreground)
# Just read terminal output - Flask prints debug info

# Test API directly
Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -UseBasicParsing
Invoke-WebRequest -Uri 'http://localhost:5000/api/jobs' -UseBasicParsing
```

---

**You're ready to go! 🎉 Start with Step 1 above and enjoy testing!**
