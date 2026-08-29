"""
Dummy Data Generator for Testing
"""

import json
import os
from datetime import datetime
from app.utils.auth_utils import hash_password
from config import Config

def generate_dummy_data():
    """Generate dummy data for testing"""
    
    config = Config()
    
    # Sample Users
    users_data = {
        "users": [
            {
                "id": 1,
                "email": "john@example.com",
                "password_hash": hash_password("Password123"),
                "name": "John Seeker",
                "role": "job_seeker",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 2,
                "email": "alice@example.com",
                "password_hash": hash_password("Password123"),
                "name": "Alice Seeker",
                "role": "job_seeker",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 3,
                "email": "recruitment@company.com",
                "password_hash": hash_password("Password123"),
                "name": "Bob Recruiter",
                "role": "recruiter",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 4,
                "email": "hr@techcorp.com",
                "password_hash": hash_password("Password123"),
                "name": "Sarah Recruiter",
                "role": "recruiter",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ],
        "last_id": 4
    }
    
    # Sample Profiles
    profiles_data = {
        "profiles": [
            {
                "id": 1,
                "user_id": 1,
                "role": "job_seeker",
                "bio": "Passionate Python developer with 3 years of experience",
                "location": "San Francisco, CA",
                "website": "johnseeker.com",
                "cv_path": None,
                "company": "",
                "position": "Senior Python Developer",
                "skills": ["Python", "Django", "Flask", "SQL", "PostgreSQL", "REST API"],
                "experience_years": 3,
                "education": [{"degree": "BS", "field": "Computer Science", "school": "UC Berkeley"}],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 2,
                "user_id": 2,
                "role": "job_seeker",
                "bio": "Frontend specialist with strong JavaScript skills",
                "location": "New York, NY",
                "website": "aliceseeker.dev",
                "cv_path": None,
                "company": "",
                "position": "React Developer",
                "skills": ["JavaScript", "React", "Vue", "HTML", "CSS", "Node.js"],
                "experience_years": 2,
                "education": [{"degree": "BS", "field": "Information Technology", "school": "NYU"}],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 3,
                "user_id": 3,
                "role": "recruiter",
                "bio": "Recruiting talented engineers for innovative projects",
                "location": "Mountain View, CA",
                "website": "company.com",
                "cv_path": None,
                "company": "Tech Company Inc",
                "position": "HR Manager",
                "skills": ["Recruiting", "HR", "Talent Management"],
                "experience_years": 5,
                "education": [{"degree": "MBA", "field": "Business Administration", "school": "Stanford"}],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 4,
                "user_id": 4,
                "role": "recruiter",
                "bio": "Looking for top-tier software engineers",
                "location": "Austin, TX",
                "website": "techcorp.com",
                "cv_path": None,
                "company": "TechCorp Solutions",
                "position": "Recruitment Lead",
                "skills": ["Recruiting", "Interview", "Assessment"],
                "experience_years": 4,
                "education": [{"degree": "MS", "field": "Psychology", "school": "University of Texas"}],
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ],
        "last_id": 4
    }
    
    # Sample Jobs
    jobs_data = {
        "jobs": [
            {
                "id": 1,
                "recruiter_id": 3,
                "title": "Senior Python Developer",
                "description": "We're looking for an experienced Python developer to join our back-end team. You'll work on scalable web applications using Django and Flask frameworks. The ideal candidate has strong experience with databases, REST APIs, and cloud services.",
                "required_skills": ["Python", "Django", "Flask", "SQL", "AWS"],
                "experience_level": "senior",
                "salary_min": 120000,
                "salary_max": 160000,
                "status": "active",
                "applicants_count": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 2,
                "recruiter_id": 3,
                "title": "React Frontend Engineer",
                "description": "Join our front-end team and build beautiful user interfaces with React. We need someone passionate about web development who can write clean, maintainable code. You'll collaborate with designers and backend engineers to create amazing web experiences.",
                "required_skills": ["JavaScript", "React", "HTML", "CSS", "Redux"],
                "experience_level": "mid",
                "salary_min": 100000,
                "salary_max": 140000,
                "status": "active",
                "applicants_count": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 3,
                "recruiter_id": 4,
                "title": "Full Stack Developer",
                "description": "We're hiring a full stack developer who can work across our entire technology stack. Experience with both front-end and back-end is essential. This is a great opportunity to grow and take on leadership responsibilities.",
                "required_skills": ["Python", "JavaScript", "React", "Docker", "Kubernetes"],
                "experience_level": "senior",
                "salary_min": 130000,
                "salary_max": 170000,
                "status": "active",
                "applicants_count": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 4,
                "recruiter_id": 4,
                "title": "Junior Python Developer",
                "description": "Perfect opportunity for someone starting their development career. You'll receive mentorship from senior developers while working on real projects. Strong fundamentals in programming are recommended.",
                "required_skills": ["Python", "SQL", "Git"],
                "experience_level": "entry",
                "salary_min": 60000,
                "salary_max": 80000,
                "status": "active",
                "applicants_count": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            {
                "id": 5,
                "recruiter_id": 3,
                "title": "Machine Learning Engineer",
                "description": "We're building AI-powered features and need an ML expert. Experience with TensorFlow, scikit-learn, and data analysis is essential. You'll work on recommendation systems and predictive models.",
                "required_skills": ["Python", "Machine Learning", "TensorFlow", "Data Science", "Pandas"],
                "experience_level": "senior",
                "salary_min": 140000,
                "salary_max": 180000,
                "status": "active",
                "applicants_count": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        ],
        "last_id": 5
    }
    
    # Sample Applications
    applications_data = {
        "applications": [
            {
                "id": 1,
                "user_id": 1,
                "job_id": 1,
                "status": "pending",
                "resume_used": "cv_1_main.pdf",
                "applied_at": datetime.utcnow().isoformat(),
                "reviewed_at": None
            },
            {
                "id": 2,
                "user_id": 1,
                "job_id": 3,
                "status": "pending",
                "resume_used": "cv_1_main.pdf",
                "applied_at": datetime.utcnow().isoformat(),
                "reviewed_at": None
            },
            {
                "id": 3,
                "user_id": 2,
                "job_id": 2,
                "status": "pending",
                "resume_used": "cv_2_main.pdf",
                "applied_at": datetime.utcnow().isoformat(),
                "reviewed_at": None
            }
        ],
        "last_id": 3
    }
    
    # Write data to files
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    with open(config.USERS_DATA_FILE, 'w') as f:
        json.dump(users_data, f, indent=2)
    print(f"✓ Created {config.USERS_DATA_FILE}")
    
    with open(config.PROFILES_DATA_FILE, 'w') as f:
        json.dump(profiles_data, f, indent=2)
    print(f"✓ Created {config.PROFILES_DATA_FILE}")
    
    with open(config.JOBS_DATA_FILE, 'w') as f:
        json.dump(jobs_data, f, indent=2)
    print(f"✓ Created {config.JOBS_DATA_FILE}")
    
    with open(config.APPLICATIONS_DATA_FILE, 'w') as f:
        json.dump(applications_data, f, indent=2)
    print(f"✓ Created {config.APPLICATIONS_DATA_FILE}")
    
    print("\n✓ Dummy data generated successfully!")
    print("\nTest Credentials:")
    print("=" * 50)
    print("Job Seeker:")
    print("  Email: john@example.com")
    print("  Password: Password123")
    print("\nRecruiter:")
    print("  Email: recruitment@company.com")
    print("  Password: Password123")
    print("=" * 50)

if __name__ == '__main__':
    generate_dummy_data()
