"""
Job Seeder - Add 20 real jobs to MongoDB Atlas
Run: cd backend && py seed_jobs.py
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_jobs_collection
from bson import ObjectId

# 20 Real Job Listings
JOBS_DATA = [
    {
        "title": "Senior React Developer",
        "company": "TechCorp Solutions",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "category": "Software Development",
        "description": "We are looking for an experienced React Developer to join our growing team. You will be responsible for building modern, responsive web applications using React, TypeScript, and related technologies.",
        "requirements": ["5+ years of React experience", "Strong TypeScript skills", "Experience with Redux or Context API", "Knowledge of REST APIs and GraphQL"],
        "responsibilities": ["Develop new user-facing features", "Build reusable components", "Optimize applications for performance", "Collaborate with backend developers"],
        "skills_required": ["React", "TypeScript", "JavaScript", "Redux", "HTML/CSS"],
        "experience_level": "Senior",
        "salary_min": 2500000,
        "salary_max": 3500000,
        "salary_currency": "PKR"
    },
    {
        "title": "Full Stack JavaScript Developer",
        "company": "Digital Innovations",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "category": "Software Development",
        "description": "Join our team as a Full Stack Developer working on cutting-edge web applications. You will work on both frontend and backend development using modern JavaScript technologies.",
        "requirements": ["3+ years of full stack development", "Experience with Node.js and Express", "MongoDB or SQL database knowledge", "Frontend framework experience"],
        "responsibilities": ["Develop full stack features", "Design and implement APIs", "Database design and optimization", "Code reviews and mentoring"],
        "skills_required": ["JavaScript", "Node.js", "React", "Express", "MongoDB"],
        "experience_level": "Mid",
        "salary_min": 1800000,
        "salary_max": 2500000,
        "salary_currency": "PKR"
    },
    {
        "title": "Data Scientist",
        "company": "AI Analytics Pakistan",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "category": "Data Science",
        "description": "Looking for a talented Data Scientist to work on machine learning projects. You will analyze complex datasets, build predictive models, and help drive data-driven decisions.",
        "requirements": ["Masters in Data Science, CS, or related field", "Strong Python programming skills", "Experience with ML frameworks", "Statistical analysis knowledge"],
        "responsibilities": ["Develop machine learning models", "Analyze large datasets", "Create data visualizations", "Present findings to stakeholders"],
        "skills_required": ["Python", "TensorFlow", "Pandas", "NumPy", "Scikit-learn"],
        "experience_level": "Senior",
        "salary_min": 3000000,
        "salary_max": 4500000,
        "salary_currency": "PKR"
    },
    {
        "title": "Frontend Developer",
        "company": "Creative Agency Lahore",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "category": "Software Development",
        "description": "We need a creative Frontend Developer to build beautiful user interfaces. You will work closely with designers to implement pixel-perfect designs.",
        "requirements": ["2+ years of frontend development", "Strong HTML/CSS/JavaScript skills", "Experience with modern CSS frameworks", "UI/UX sensibility"],
        "responsibilities": ["Implement responsive designs", "Optimize website performance", "Ensure cross-browser compatibility", "Collaborate with design team"],
        "skills_required": ["HTML5", "CSS3", "JavaScript", "React", "Tailwind CSS"],
        "experience_level": "Mid",
        "salary_min": 1200000,
        "salary_max": 1800000,
        "salary_currency": "PKR"
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudTech Pakistan",
        "location": "Remote",
        "type": "Full-time",
        "category": "DevOps",
        "description": "Join our DevOps team to manage cloud infrastructure and deployment pipelines. You will work with AWS, Docker, and Kubernetes to ensure reliable deployments.",
        "requirements": ["3+ years of DevOps experience", "AWS or Azure certification preferred", "Docker and Kubernetes expertise", "CI/CD pipeline experience"],
        "responsibilities": ["Manage cloud infrastructure", "Build and maintain CI/CD pipelines", "Monitor system performance", "Implement security best practices"],
        "skills_required": ["AWS", "Docker", "Kubernetes", "Jenkins", "Terraform"],
        "experience_level": "Senior",
        "salary_min": 2500000,
        "salary_max": 4000000,
        "salary_currency": "PKR"
    },
    {
        "title": "Mobile App Developer (Flutter)",
        "company": "AppWorks Studio",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "category": "Mobile Development",
        "description": "We are seeking a Flutter developer to build cross-platform mobile applications. You will create beautiful, performant apps for iOS and Android.",
        "requirements": ["2+ years of Flutter development", "Published apps on App Store/Play Store", "Dart programming expertise", "REST API integration experience"],
        "responsibilities": ["Develop Flutter applications", "Implement UI/UX designs", "Optimize app performance", "Maintain existing applications"],
        "skills_required": ["Flutter", "Dart", "Firebase", "REST APIs", "Git"],
        "experience_level": "Mid",
        "salary_min": 1500000,
        "salary_max": 2200000,
        "salary_currency": "PKR"
    },
    {
        "title": "Backend Developer (Python/Django)",
        "company": "WebSolutions PK",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "category": "Software Development",
        "description": "Looking for a Python backend developer with Django experience. You will build scalable APIs and backend systems for our web applications.",
        "requirements": ["3+ years of Python/Django experience", "Database design expertise", "API development experience", "Knowledge of caching strategies"],
        "responsibilities": ["Design and implement APIs", "Database schema design", "Optimize backend performance", "Write unit and integration tests"],
        "skills_required": ["Python", "Django", "Django REST Framework", "PostgreSQL", "Redis"],
        "experience_level": "Mid",
        "salary_min": 1800000,
        "salary_max": 2800000,
        "salary_currency": "PKR"
    },
    {
        "title": "UI/UX Designer",
        "company": "Design Hub Lahore",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "category": "Design",
        "description": "We need a talented UI/UX Designer to create beautiful, user-friendly interfaces. You will work on web and mobile applications for various clients.",
        "requirements": ["Portfolio demonstrating UI/UX work", "Proficiency in Figma or Sketch", "Understanding of user research", "HTML/CSS knowledge a plus"],
        "responsibilities": ["Create wireframes and prototypes", "Design user interfaces", "Conduct user research", "Collaborate with developers"],
        "skills_required": ["Figma", "Adobe XD", "Prototyping", "User Research", "Design Systems"],
        "experience_level": "Mid",
        "salary_min": 1400000,
        "salary_max": 2000000,
        "salary_currency": "PKR"
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Dynamics",
        "location": "Remote",
        "type": "Full-time",
        "category": "Data Science",
        "description": "Join our AI team to build production-grade machine learning systems. You will deploy and maintain ML models at scale.",
        "requirements": ["Masters or PhD in ML/AI related field", "Experience deploying ML models", "MLOps knowledge", "Strong Python and SQL skills"],
        "responsibilities": ["Build and deploy ML models", "Create data pipelines", "Monitor model performance", "Optimize inference speed"],
        "skills_required": ["Python", "TensorFlow", "PyTorch", "MLflow", "Docker"],
        "experience_level": "Senior",
        "salary_min": 3500000,
        "salary_max": 5000000,
        "salary_currency": "PKR"
    },
    {
        "title": "WordPress Developer",
        "company": "WebAgency PK",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "category": "Web Development",
        "description": "Seeking an experienced WordPress developer to build custom themes and plugins. You will work on various client projects ranging from blogs to e-commerce sites.",
        "requirements": ["3+ years of WordPress development", "Custom theme development experience", "PHP and MySQL expertise", "Plugin development knowledge"],
        "responsibilities": ["Develop custom WordPress themes", "Create custom plugins", "Optimize site performance", "Maintain existing websites"],
        "skills_required": ["WordPress", "PHP", "JavaScript", "MySQL", "WooCommerce"],
        "experience_level": "Mid",
        "salary_min": 1000000,
        "salary_max": 1600000,
        "salary_currency": "PKR"
    },
    {
        "title": "Project Manager (IT)",
        "company": "TechVentures Pakistan",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "category": "Management",
        "description": "We need an experienced IT Project Manager to lead software development projects. You will coordinate between clients and development teams.",
        "requirements": ["PMP or Agile certification", "5+ years of project management", "Software development background", "Excellent communication skills"],
        "responsibilities": ["Plan and execute projects", "Manage project timelines", "Coordinate with stakeholders", "Risk management"],
        "skills_required": ["Project Management", "Agile/Scrum", "JIRA", "Risk Management", "Communication"],
        "experience_level": "Senior",
        "salary_min": 2800000,
        "salary_max": 4000000,
        "salary_currency": "PKR"
    },
    {
        "title": "QA Engineer",
        "company": "QualityFirst Software",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "category": "Quality Assurance",
        "description": "Join our QA team to ensure software quality. You will write test cases, perform manual and automated testing, and report bugs.",
        "requirements": ["2+ years of QA experience", "Test automation experience", "Selenium or similar tools", "API testing knowledge"],
        "responsibilities": ["Write test cases", "Perform manual testing", "Develop automated tests", "Report and track bugs"],
        "skills_required": ["Selenium", "Test Automation", "API Testing", "JIRA", "Manual Testing"],
        "experience_level": "Mid",
        "salary_min": 1200000,
        "salary_max": 1800000,
        "salary_currency": "PKR"
    },
    {
        "title": "Technical Support Specialist",
        "company": "HelpDesk Solutions",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "category": "Technical Support",
        "description": "Provide technical support for software products. You will help customers resolve issues and maintain high satisfaction levels.",
        "requirements": ["Technical background", "Customer service experience", "Problem-solving skills", "Knowledge of common software issues"],
        "responsibilities": ["Respond to support tickets", "Troubleshoot technical issues", "Document solutions", "Escalate complex issues"],
        "skills_required": ["Customer Support", "Troubleshooting", "Documentation", "Communication", "CRM Tools"],
        "experience_level": "Entry",
        "salary_min": 600000,
        "salary_max": 1000000,
        "salary_currency": "PKR"
    },
    {
        "title": "Blockchain Developer",
        "company": "CryptoInnovate PK",
        "location": "Remote",
        "type": "Full-time",
        "category": "Blockchain",
        "description": "Looking for a blockchain developer to work on decentralized applications. Experience with Ethereum and smart contracts required.",
        "requirements": ["Solidity programming experience", "Understanding of blockchain concepts", "Web3.js or Ethers.js knowledge", "Smart contract deployment experience"],
        "responsibilities": ["Develop smart contracts", "Build DApps", "Integrate blockchain solutions", "Research new blockchain technologies"],
        "skills_required": ["Solidity", "Ethereum", "Web3.js", "Smart Contracts", "DeFi"],
        "experience_level": "Senior",
        "salary_min": 4000000,
        "salary_max": 6000000,
        "salary_currency": "PKR"
    },
    {
        "title": "Cloud Architect",
        "company": "CloudFirst Pakistan",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "category": "Cloud Computing",
        "description": "Design and implement cloud infrastructure solutions. You will work with AWS, Azure, or GCP to build scalable systems.",
        "requirements": ["AWS/Azure/GCP certification", "5+ years of cloud experience", "Infrastructure as Code expertise", "Security best practices"],
        "responsibilities": ["Design cloud architecture", "Implement IaC solutions", "Optimize cloud costs", "Ensure security compliance"],
        "skills_required": ["AWS", "Azure", "Terraform", "Docker", "Kubernetes"],
        "experience_level": "Senior",
        "salary_min": 4500000,
        "salary_max": 7000000,
        "salary_currency": "PKR"
    },
    {
        "title": "PHP Laravel Developer",
        "company": "CodeCrafters Lahore",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "category": "Web Development",
        "description": "Seeking a Laravel developer to build robust web applications. You will work on e-commerce, CMS, and custom business applications.",
        "requirements": ["3+ years of Laravel experience", "Strong PHP fundamentals", "MySQL expertise", "API development experience"],
        "responsibilities": ["Develop Laravel applications", "Design database schemas", "Build RESTful APIs", "Maintain existing projects"],
        "skills_required": ["PHP", "Laravel", "MySQL", "REST APIs", "Git"],
        "experience_level": "Mid",
        "salary_min": 1400000,
        "salary_max": 2200000,
        "salary_currency": "PKR"
    },
    {
        "title": "SEO Specialist",
        "company": "DigitalMarketing Pro",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "category": "Marketing",
        "description": "Help clients improve their search engine rankings. You will develop SEO strategies and implement best practices.",
        "requirements": ["Proven SEO results", "Experience with SEO tools", "Content optimization knowledge", "Analytics expertise"],
        "responsibilities": ["Develop SEO strategies", "Perform keyword research", "Optimize website content", "Track and report rankings"],
        "skills_required": ["SEO", "Google Analytics", "SEMrush", "Content Strategy", "Link Building"],
        "experience_level": "Mid",
        "salary_min": 1000000,
        "salary_max": 1600000,
        "salary_currency": "PKR"
    },
    {
        "title": "Network Administrator",
        "company": "Enterprise Systems PK",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "category": "Networking",
        "description": "Manage and maintain network infrastructure. You will ensure network security, performance, and reliability.",
        "requirements": ["CCNA or CCNP certification", "Network security knowledge", "Experience with firewalls", "Troubleshooting expertise"],
        "responsibilities": ["Maintain network infrastructure", "Monitor network performance", "Implement security measures", "Troubleshoot network issues"],
        "skills_required": ["Cisco", "Network Security", "Firewalls", "VPN", "Linux"],
        "experience_level": "Mid",
        "salary_min": 1600000,
        "salary_max": 2400000,
        "salary_currency": "PKR"
    },
    {
        "title": "Content Writer (Tech)",
        "company": "TechContent Hub",
        "location": "Remote",
        "type": "Part-time",
        "category": "Content Writing",
        "description": "Write technical content including blog posts, tutorials, and documentation. Knowledge of programming concepts required.",
        "requirements": ["Excellent writing skills", "Technical background", "SEO knowledge", "Research skills"],
        "responsibilities": ["Write technical articles", "Create tutorials", "Develop documentation", "Research tech topics"],
        "skills_required": ["Technical Writing", "SEO", "Research", "Documentation", "Markdown"],
        "experience_level": "Entry",
        "salary_min": 400000,
        "salary_max": 800000,
        "salary_currency": "PKR"
    },
    {
        "title": "Database Administrator",
        "company": "DataSystems Pakistan",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "category": "Database Administration",
        "description": "Manage and optimize database systems. You will work with PostgreSQL, MySQL, and MongoDB to ensure data integrity and performance.",
        "requirements": ["3+ years of DBA experience", "PostgreSQL and MySQL expertise", "Performance tuning skills", "Backup and recovery knowledge"],
        "responsibilities": ["Maintain database systems", "Optimize query performance", "Implement backup strategies", "Monitor database health"],
        "skills_required": ["PostgreSQL", "MySQL", "MongoDB", "Query Optimization", "Linux"],
        "experience_level": "Senior",
        "salary_min": 2500000,
        "salary_max": 3800000,
        "salary_currency": "PKR"
    }
]


def seed_jobs():
    """Insert jobs into MongoDB"""
    print("=" * 60)
    print("Seeding Jobs to MongoDB Atlas")
    print("=" * 60)
    
    # Connect to database
    db = init_db()
    if db is None:
        print("Failed to connect to MongoDB")
        return False
    
    jobs_collection = db.jobs
    
    # Check existing jobs
    existing_count = jobs_collection.count_documents({})
    print(f"\nExisting jobs in database: {existing_count}")
    
    # Create a recruiter user ID (we'll use a placeholder)
    recruiter_id = ObjectId()
    
    # Prepare jobs with additional fields
    jobs_to_insert = []
    now = datetime.utcnow()
    
    for i, job_data in enumerate(JOBS_DATA, 1):
        job = {
            "_id": ObjectId(),
            "title": job_data["title"],
            "company": job_data["company"],
            "location": job_data["location"],
            "type": job_data["type"],
            "category": job_data["category"],
            "description": job_data["description"],
            "requirements": job_data["requirements"],
            "responsibilities": job_data["responsibilities"],
            "skills_required": job_data["skills_required"],
            "experience_level": job_data["experience_level"],
            "salary_min": job_data["salary_min"],
            "salary_max": job_data["salary_max"],
            "salary_currency": job_data["salary_currency"],
            "posted_by": recruiter_id,
            "status": "active",
            "created_at": now - timedelta(days=i),  # Staggered posting dates
            "updated_at": now,
            "views_count": 0,
            "applications_count": 0
        }
        jobs_to_insert.append(job)
    
    # Insert jobs
    try:
        result = jobs_collection.insert_many(jobs_to_insert)
        print(f"\nSuccessfully inserted {len(result.inserted_ids)} jobs")
        
        # Display inserted jobs
        print("\nInserted Jobs:")
        for job in jobs_to_insert[:5]:  # Show first 5
            print(f"  - {job['title']} at {job['company']} ({job['location']})")
        
        if len(jobs_to_insert) > 5:
            print(f"  ... and {len(jobs_to_insert) - 5} more jobs")
        
        print("\n" + "=" * 60)
        print("Job seeding completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"Error inserting jobs: {e}")
        return False


def cleanup_test_data():
    """Remove test data from database"""
    print("\n" + "=" * 60)
    print("Cleaning up test data")
    print("=" * 60)
    
    db = init_db()
    if db is None:
        print("Failed to connect to MongoDB")
        return
    
    # Remove test users
    users_result = db.users.delete_many({
        "email": {"$in": ["test@example.com", "test@test.com", "john@test.com", "hr@company.com"]}
    })
    print(f"Removed {users_result.deleted_count} test users")
    
    # Remove test jobs
    jobs_result = db.jobs.delete_many({
        "$or": [
            {"company": "Test Company"},
            {"title": {"$regex": "^Test", "$options": "i"}},
            {"description": {"$regex": "test", "$options": "i"}}
        ]
    })
    print(f"Removed {jobs_result.deleted_count} test jobs")
    
    print("Cleanup completed!")


if __name__ == "__main__":
    # First cleanup test data
    cleanup_test_data()
    
    # Then seed real jobs
    success = seed_jobs()
    
    if success:
        print("\n✅ Database seeded successfully!")
        print("\nYou can now view jobs at:")
        print("  - Frontend: http://localhost:3000/jobs")
        print("  - API: http://127.0.0.1:5000/api/jobs")
        sys.exit(0)
    else:
        print("\n❌ Failed to seed database")
        sys.exit(1)
