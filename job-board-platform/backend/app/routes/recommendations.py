"""
Job recommendations routes - Updated for MongoDB
"""

from flask import Blueprint, request, jsonify, session, current_app
from app.models.data_models import JobModel, ProfileModel, UserModel
from app.ml.recommendation_engine import JobRecommendationEngine
from app.services.db_services import JobService, ProfileService, UserService
from config import get_config

recommendations_bp = Blueprint('recommendations', __name__)
config = get_config()

# Legacy JSON models (fallback)
job_model = JobModel(config)
profile_model = ProfileModel(config)
user_model = UserModel(config)

# Global recommendation engine
rec_engine = None

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def use_mongodb():
    """Check if MongoDB should be used"""
    try:
        return current_app.config.get('USE_MONGODB', False)
    except:
        return False

def initialize_engine():
    """Initialize recommendation engine with current jobs"""
    global rec_engine
    rec_engine = JobRecommendationEngine()
    
    # Get jobs from MongoDB or JSON
    if use_mongodb():
        jobs = JobService.get_all_jobs()
        print(f"[DEBUG] Loaded {len(jobs)} jobs from MongoDB for recommendations")
    else:
        jobs = job_model.get_all()
        print(f"[DEBUG] Loaded {len(jobs)} jobs from JSON for recommendations")
    
    rec_engine.fit(jobs)

@recommendations_bp.route('/personalized', methods=['GET'])
def get_personalized_recommendations():
    """Get personalized job recommendations for current user"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if session.get('role') != 'job_seeker':
            return jsonify({'error': 'Only job seekers can get recommendations'}), 403
        
        # Initialize engine if needed
        if rec_engine is None:
            initialize_engine()
        
        user_id = session.get('user_id')
        
        # Get profile from MongoDB or JSON
        profile = None
        if use_mongodb():
            profile = ProfileService.get_profile_by_user_id(user_id)
            print(f"[DEBUG] Profile from MongoDB: {profile is not None}")
        else:
            profile = profile_model.get_by_user_id(user_id)
        
        if not profile:
            return jsonify({
                'error': 'User profile not found. Please complete your profile first.',
                'needs_profile': True
            }), 404
        
        # Check if profile has skills or resume
        has_skills = profile.get('skills') and len(profile.get('skills', [])) > 0
        has_resume = profile.get('resume_url') is not None
        
        if not has_skills and not has_resume:
            return jsonify({
                'error': 'Please add skills or upload your resume to get personalized recommendations',
                'needs_profile_completion': True,
                'recommendations': get_fallback_recommendations()
            }), 200
        
        # Get recommendations
        recommendations = rec_engine.recommend(profile, top_n=10)
        
        # Enrich with skill and experience matching
        for rec in recommendations:
            job = rec['job']
            rec['skill_match'] = rec_engine.get_skill_match(
                profile.get('skills', []),
                job.get('skills_required', job.get('required_skills', []))
            )
            
            # Extract min experience from experience_level
            min_exp = _get_min_experience(job.get('experience_level', ''))
            rec['experience_match'] = rec_engine.get_experience_match(
                profile.get('experience_years', 0),
                min_exp
            )
            
            # Calculate overall match percentage
            skill_percent = rec['skill_match'].get('match_percentage', 0)
            exp_percent = rec['experience_match'].get('match_percentage', 0)
            rec['match_percentage'] = int((skill_percent * 0.7 + exp_percent * 0.3))
        
        # Sort by match percentage
        recommendations.sort(key=lambda x: x.get('match_percentage', 0), reverse=True)
        
        return jsonify({
            'count': len(recommendations),
            'recommendations': recommendations,
            'has_profile': True,
            'has_skills': has_skills,
            'has_resume': has_resume
        }), 200
    
    except Exception as e:
        print(f"[ERROR] get_personalized_recommendations: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'recommendations': get_fallback_recommendations()
        }), 200

@recommendations_bp.route('/for-job/<job_id>', methods=['GET'])
def get_job_recommendations(job_id):
    """Get recommended candidates for a job (Recruiter only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if session.get('role') != 'recruiter':
            return jsonify({'error': 'Only recruiters can access this'}), 403
        
        # Get job from MongoDB or JSON
        job = None
        if use_mongodb():
            job = JobService.get_job_by_id(job_id)
        else:
            try:
                job_id_int = int(job_id)
            except:
                job_id_int = job_id
            job = job_model.get_by_id(job_id_int)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Check authorization
        posted_by = job.get('posted_by') or job.get('recruiter_id')
        if str(posted_by) != str(session.get('user_id')):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all profiles and rank by match
        from app.models.data_models import DataStore
        
        if use_mongodb():
            # Get all profiles from MongoDB
            from database import get_profiles_collection
            profiles_collection = get_profiles_collection()
            if profiles_collection:
                profiles = list(profiles_collection.find({}))
                # Convert ObjectId to string
                for p in profiles:
                    p['_id'] = str(p['_id'])
                    if 'user_id' in p:
                        p['user_id'] = str(p['user_id'])
            else:
                profiles = []
        else:
            profile_store = DataStore(config.PROFILES_DATA_FILE)
            profiles = profile_store.get_all('profiles')
        
        # Filter to job seekers only
        profiles = [p for p in profiles if p.get('role') == 'job_seeker']
        
        ranked = []
        for profile in profiles:
            skill_match = rec_engine.get_skill_match(
                profile.get('skills', []),
                job.get('skills_required', job.get('required_skills', []))
            )
            
            min_exp = _get_min_experience(job.get('experience_level', ''))
            exp_match = rec_engine.get_experience_match(
                profile.get('experience_years', 0),
                min_exp
            )
            
            # Calculate overall score
            skill_score = skill_match.get('match_percentage', 0)
            exp_score = exp_match.get('match_percentage', 0)
            overall_score = (skill_score * 0.7 + exp_score * 0.3)
            
            # Get user info
            user = None
            if use_mongodb():
                user = UserService.get_user_by_id(profile.get('user_id'))
            else:
                user = user_model.get_by_id(profile.get('user_id'))
            
            ranked.append({
                'profile': profile,
                'user': {
                    'id': user.get('id') if user else None,
                    'name': user.get('name') if user else None,
                    'email': user.get('email') if user else None
                } if user else None,
                'skill_match': skill_match,
                'experience_match': exp_match,
                'overall_score': round(overall_score, 2)
            })
        
        # Sort by overall score
        ranked.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return jsonify({
            'count': len(ranked),
            'job': job,
            'recommended_candidates': ranked[:20]  # Top 20
        }), 200
    
    except Exception as e:
        print(f"[ERROR] get_job_recommendations: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/update-engine', methods=['POST'])
def update_recommendation_engine():
    """Update recommendation engine (should be called periodically)"""
    try:
        initialize_engine()
        return jsonify({'message': 'Recommendation engine updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_fallback_recommendations():
    """Return fallback recommendations when no profile exists"""
    # Get top jobs from database
    if use_mongodb():
        jobs = JobService.get_all_jobs(limit=5)
    else:
        jobs = job_model.get_all()[:5]
    
    fallback_recs = []
    for job in jobs:
        fallback_recs.append({
            'job': job,
            'job_id': job.get('id') or job.get('_id'),
            'title': job.get('title'),
            'company': job.get('company'),
            'location': job.get('location'),
            'skills_required': job.get('skills_required', []),
            'match_percentage': 50,  # Default match for fallback
            'skill_match': {'match_percentage': 50, 'matched_skills': [], 'missing_skills': []},
            'experience_match': {'match_percentage': 50, 'is_match': True}
        })
    return fallback_recs

def _get_min_experience(experience_level: str) -> int:
    """Extract minimum years of experience from level string"""
    if not experience_level:
        return 0
    level_map = {
        'entry': 0,
        'entry-level': 0,
        'junior': 1,
        'mid': 3,
        'mid-level': 3,
        'senior': 5,
        'lead': 8,
        'principal': 10
    }
    return level_map.get(experience_level.lower(), 0)

# Initialize engine on blueprint load
@recommendations_bp.before_app_request
def init_engine():
    global rec_engine
    if rec_engine is None:
        initialize_engine()