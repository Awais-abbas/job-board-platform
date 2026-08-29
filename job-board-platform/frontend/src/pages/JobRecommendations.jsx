import React, { useState, useEffect } from 'react'

const API_BASE_URL = 'http://localhost:5000/api'

const JobRecommendations = ({ onNavigate, currentUser }) => {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [needsProfile, setNeedsProfile] = useState(false)
  const [profileStatus, setProfileStatus] = useState({
    hasProfile: false,
    hasSkills: false,
    hasResume: false
  })

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async () => {
    try {
      setLoading(true)
      setError('')
      setNeedsProfile(false)
      
      const response = await fetch(`${API_BASE_URL}/recommendations/personalized`, {
        credentials: 'include'
      })

      if (response.ok) {
        const data = await response.json()
        
        // Check if profile needs completion
        if (data.needs_profile_completion) {
          setNeedsProfile(true)
          setError(data.error || 'Please complete your profile to get personalized recommendations')
          setProfileStatus({
            hasProfile: data.has_profile || false,
            hasSkills: data.has_skills || false,
            hasResume: data.has_resume || false
          })
          setRecommendations([])
        } else {
          // Transform recommendations with match percentages
          const transformedRecommendations = transformRecommendations(data.recommendations || [])
          setRecommendations(transformedRecommendations)
          setProfileStatus({
            hasProfile: data.has_profile || true,
            hasSkills: data.has_skills || false,
            hasResume: data.has_resume || false
          })
        }
      } else if (response.status === 401) {
        setError('Please login to see personalized recommendations')
        setRecommendations([])
      } else if (response.status === 404) {
        const data = await response.json()
        setNeedsProfile(true)
        setError(data.error || 'Please complete your profile first')
        setRecommendations([])
      } else {
        setError('Failed to fetch recommendations')
        setRecommendations([])
      }
    } catch (err) {
      console.error('Error fetching recommendations:', err)
      setError('Error connecting to server. Please try again later.')
      setRecommendations([])
    } finally {
      setLoading(false)
    }
  }

  const transformRecommendations = (recommendations) => {
    return recommendations.map(rec => {
      // Handle different response formats
      const job = rec.job || rec
      const matchPercentage = rec.match_percentage || 
                             rec.skill_match?.match_percentage || 0
      
      // Get skills from job
      const skills = job.skills_required || rec.skills_required || job.tags || rec.tags || []
      
      // Format salary
      let salaryDisplay = 'Salary not disclosed'
      if (job.salary_min && job.salary_max) {
        const currency = job.salary_currency || 'PKR'
        const minLPA = (job.salary_min / 100000).toFixed(1)
        const maxLPA = (job.salary_max / 100000).toFixed(1)
        salaryDisplay = `${currency} ${minLPA}-${maxLPA} LPA`
      } else if (job.salary_display) {
        salaryDisplay = job.salary_display
      }
      
      return {
        id: job.id || job._id || rec.job_id || rec.id,
        title: job.title || rec.title || 'Job Position',
        company: job.company || rec.company || 'Company Name',
        location: job.location || rec.location || 'Location',
        salary: salaryDisplay,
        type: job.type || rec.type || 'Full-time',
        category: job.category || rec.category || 'Software Development',
        tags: skills,
        matchPercentage: Math.round(matchPercentage),
        description: job.description || rec.description || 'Job description not available',
        matchedSkills: rec.skill_match?.matched_skills || [],
        missingSkills: rec.skill_match?.missing_skills || [],
        skillMatchPercentage: rec.skill_match?.match_percentage || 0,
        experienceMatchPercentage: rec.experience_match?.match_percentage || 0
      }
    })
  }

  const getMatchColor = (percentage) => {
    if (percentage >= 90) return 'bg-green-100 text-green-800'
    if (percentage >= 80) return 'bg-blue-100 text-blue-800'
    if (percentage >= 70) return 'bg-yellow-100 text-yellow-800'
    return 'bg-gray-100 text-gray-800'
  }

  const getMatchIcon = (percentage) => {
    if (percentage >= 90) return '🎯'
    if (percentage >= 80) return '📈'
    if (percentage >= 70) return '👍'
    return '📝'
  }

  const renderProfilePrompt = () => {
    if (!needsProfile && profileStatus.hasProfile) return null
    
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
        <div className="flex items-start gap-4">
          <div className="text-3xl">📝</div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-yellow-800 mb-2">
              Complete Your Profile for Better Recommendations
            </h3>
            <p className="text-yellow-700 mb-4">
              {error || 'Add your skills and experience to get personalized job matches from our database'}
            </p>
            
            <div className="space-y-3 mb-4">
              {!profileStatus.hasSkills && (
                <div className="flex items-center gap-2 text-sm text-yellow-700">
                  <span>❌</span>
                  <span>No skills added yet</span>
                </div>
              )}
              {!profileStatus.hasResume && (
                <div className="flex items-center gap-2 text-sm text-yellow-700">
                  <span>❌</span>
                  <span>No resume uploaded</span>
                </div>
              )}
            </div>
            
            <button
              onClick={() => onNavigate('profile')}
              className="bg-yellow-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-yellow-700 transition-colors cursor-pointer"
            >
              Complete Your Profile
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin border-4 border-gray-300 border-t-teal-600 rounded-full w-12 h-12"></div>
          <p className="mt-4 text-gray-600">Analyzing your resume and finding perfect matches...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-12">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4 text-center">Job Recommendations For You</h1>
          <p className="text-xl text-gray-100 text-center mb-8">
            AI-powered job matches based on your resume analysis and skills
          </p>

          {/* Stats */}
          <div className="flex justify-center gap-6">
            <div className="bg-gray-800 bg-opacity-50 rounded-lg px-6 py-3 text-center">
              <span className="text-2xl font-bold">{recommendations.length}</span>
              <span className="text-sm ml-2 text-gray-300">Jobs Found</span>
            </div>
            <div className="bg-gray-800 bg-opacity-50 rounded-lg px-6 py-3 text-center">
              <span className="text-2xl font-bold">
                {recommendations.length > 0 ? Math.max(...recommendations.map(r => r.matchPercentage)) : 0}%
              </span>
              <span className="text-sm ml-2 text-gray-300">Best Match</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Profile Completion Prompt */}
        {renderProfilePrompt()}

        {/* Error Message */}
        {error && !needsProfile && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Recommendations List */}
        {recommendations.length > 0 ? (
          <div className="space-y-4">
            {recommendations.map((job) => (
              <div key={job.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex gap-4">
                    <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-2xl">
                      🏢
                    </div>
                    <div>
                      <div className="flex items-center gap-3 mb-1 flex-wrap">
                        <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getMatchColor(job.matchPercentage)}`}>
                          {getMatchIcon(job.matchPercentage)} {job.matchPercentage}% Match
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">{job.company}</p>
                    </div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                  <span className="flex items-center gap-1">
                    <svg className="w-4 h-4 text-teal-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                    </svg>
                    {job.location}
                  </span>
                  <span className="flex items-center gap-1">
                    <svg className="w-4 h-4 text-teal-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                    </svg>
                    {job.salary}
                  </span>
                  <span className="flex items-center gap-1">
                    <svg className="w-4 h-4 text-teal-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
                      <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                    </svg>
                    {job.type}
                  </span>
                </div>

                <p className="text-gray-700 text-sm mb-4">{job.description.substring(0, 200)}...</p>

                {/* Skill Match Details */}
                {job.matchedSkills && job.matchedSkills.length > 0 && (
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-2 items-center mb-2">
                      <span className="text-xs font-semibold text-green-700 bg-green-100 px-2 py-1 rounded">
                        ✓ Matched: {job.matchedSkills.length} skills
                      </span>
                      {job.missingSkills && job.missingSkills.length > 0 && (
                        <span className="text-xs font-semibold text-red-700 bg-red-100 px-2 py-1 rounded">
                          ✗ Missing: {job.missingSkills.length} skills
                        </span>
                      )}
                    </div>
                    {job.missingSkills && job.missingSkills.length > 0 && (
                      <div className="text-xs text-gray-600">
                        <span className="font-medium">Skills to learn: </span>
                        {job.missingSkills.slice(0, 3).join(', ')}
                        {job.missingSkills.length > 3 && ` +${job.missingSkills.length - 3} more`}
                      </div>
                    )}
                  </div>
                )}

                <div className="flex flex-wrap gap-2 mb-4">
                  {job.tags.slice(0, 5).map((tag, index) => (
                    <span key={index} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs">
                      {tag}
                    </span>
                  ))}
                  {job.tags.length > 5 && (
                    <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs">
                      +{job.tags.length - 5} more
                    </span>
                  )}
                </div>

                <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                  <div className="flex gap-3">
                    <button
                      onClick={() => onNavigate('jobDetails', job.id)}
                      className="px-4 py-2 border border-teal-600 text-teal-600 rounded-lg hover:bg-teal-50 cursor-pointer transition-colors"
                    >
                      View Details
                    </button>
                    <button
                      onClick={() => {
                        if (currentUser) {
                          alert('Application submitted successfully!')
                        } else {
                          alert('Please login to apply for jobs')
                          onNavigate('login')
                        }
                      }}
                      className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 cursor-pointer transition-colors"
                    >
                      Apply Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* No Recommendations State */
          !needsProfile && !loading && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
              <div className="text-5xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No recommendations available</h3>
              <p className="text-gray-600 mb-4">
                {error || 'Complete your profile to get personalized job recommendations from our database'}
              </p>
              <button
                onClick={() => onNavigate('profile')}
                className="bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors cursor-pointer"
              >
                Complete Profile
              </button>
            </div>
          )
        )}

        {/* Refresh Button */}
        {recommendations.length > 0 && (
          <div className="text-center mt-8">
            <button
              onClick={fetchRecommendations}
              className="text-teal-600 hover:text-teal-700 text-sm font-medium"
            >
              ↻ Refresh Recommendations
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default JobRecommendations 