# MongoDB Atlas Setup Guide for ONJOB

## 🚀 Quick Setup Steps

### Step 1: Get Your MongoDB Atlas URI

**Option A: Use Your Existing MongoDB Atlas URI**
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/onjob?retryWrites=true&w=majority
```

**Option B: Create a New MongoDB Atlas Cluster (Free)**

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up or log in
3. Create a new cluster (M0 - Free tier)
4. Click "Connect" → "Connect your application"
5. Copy the connection string

### Step 2: Configure the Backend

1. Open `backend/.env` file
2. Replace the MongoDB URI line:

```env
# Replace this:
MONGODB_URI=mongodb://localhost:27017/onjob

# With your Atlas URI:
MONGODB_URI=mongodb+srv://your_username:your_password@cluster0.xxxxx.mongodb.net/onjob?retryWrites=true&w=majority

# Enable MongoDB
USE_MONGODB=true
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Test the Connection

1. Start the backend:
```bash
python run.py
```

2. Check the health endpoint:
```
http://127.0.0.1:5000/api/health
```

You should see:
```json
{
  "status": "ok",
  "database": {
    "status": "connected",
    "mode": "mongodb_atlas",
    "database": "onjob"
  }
}
```

## 📋 MongoDB Atlas Configuration Checklist

- [ ] Created MongoDB Atlas account
- [ ] Created a new cluster (M0 free tier)
- [ ] Whitelisted your IP address (0.0.0.0/0 for all IPs)
- [ ] Created a database user with password
- [ ] Copied the connection string
- [ ] Updated `backend/.env` with your URI
- [ ] Set `USE_MONGODB=true`
- [ ] Installed dependencies: `pip install pymongo dnspython`
- [ ] Tested the connection

## 🔧 Troubleshooting

### Connection Timeout Error
```
ServerSelectionTimeoutError
```
**Solution**: 
- Whitelist your IP in MongoDB Atlas (Network Access → Add IP Address)
- Check your internet connection
- Verify the connection string format

### Authentication Failed
```
Authentication failed
```
**Solution**:
- Verify username and password in the URI
- Ensure the database user exists in MongoDB Atlas
- Check if the password contains special characters that need encoding

### DNS Resolution Error
```
dnspython not found
```
**Solution**:
```bash
pip install dnspython
```

## 📁 Collections Created Automatically

The following collections will be created in your `onjob` database:

- `users` - User accounts and authentication data
- `jobs` - Job listings and descriptions
- `applications` - Job applications from users
- `profiles` - User profiles and resume data
- `resumes` - Uploaded resume/CV files metadata

## 🔄 Switching Back to JSON Storage

If you want to use local JSON files instead of MongoDB:

1. Edit `backend/.env`:
```env
USE_MONGODB=false
```

2. Restart the backend

## 🔐 Security Best Practices

1. **Never commit your `.env` file** with real credentials
2. Use environment variables in production
3. Create a separate database user with limited permissions
4. Enable IP whitelisting in MongoDB Atlas
5. Use strong, unique passwords

## 🆘 Need Help?

If you're having trouble connecting, you can:

1. Use local MongoDB for development:
```env
MONGODB_URI=mongodb://localhost:27017/onjob
USE_MONGODB=true
```

2. Or use JSON file storage (no database needed):
```env
USE_MONGODB=false
```

## ✅ Connection Verification

After setup, run this test:

```bash
cd backend
python -c "
from database import init_db, check_db_health
db = init_db()
print(check_db_health())
"
```

Expected output:
```
✅ Successfully connected to MongoDB Atlas: onjob
{'status': 'connected', 'mode': 'mongodb_atlas', 'database': 'onjob'}
```
