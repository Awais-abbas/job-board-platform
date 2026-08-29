import React, { useState, useEffect } from 'react'

const API_BASE_URL = 'http://localhost:5000/api'

const RecruiterDashboard = ({ onNavigate, currentUser }) => {
  const [jobs, setJobs] = useState([])
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showPostJob, setShowPostJob] = useState(false)
  const [newJob, setNewJob] = useState({
    title: '',
    company: currentUser?.company || '',
    location: '',
    type: 'Full-time',
    category: 'Software Development',
    description: '',
    skills_required: [],
    experience_level: 'mid',
    salary_min: '',
    salary_max: '',
    salary_currency: 'PKR'
  })
  const [skillInput, setSkillInput] = useState('')
  const [postingJob, setPostingJob] = useState(false)
  const [updatingStatus, setUpdatingStatus] = useState(null)
  const [selectedCandidate, setSelectedCandidate] = useState(null)
  const [showCandidateModal, setShowCandidateModal] = useState(false)

  // Fetch jobs and applications on mount
  useEffect(() => {
    fetchJobs()
    fetchApplications()
  }, [])

  const fetchJobs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/jobs/posted`, {
        credentials: 'include'
      })

      if (response.ok) {
        const data = await response.json()
        setJobs(data.jobs || [])
      } else if (response.status === 401) {
        setError('Please login to view your dashboard')
        setTimeout(() => onNavigate('login'), 2000)
      } else {
        setError('Failed to fetch jobs')
      }
    } catch (err) {
      console.error('Error fetching jobs:', err)
      setError('Error connecting to server')
    }
  }

  const fetchApplications = async () => {
    try {
      // Fetch all jobs first to get their applications
      const jobsResponse = await fetch(`${API_BASE_URL}/jobs/posted`, {
        credentials: 'include'
      })

      if (jobsResponse.ok) {
        const jobsData = await jobsResponse.json()
        const allApplications = []

        // Fetch applications for each job
        for (const job of (jobsData.jobs || [])) {
          const jobId = job.id || job._id
          const appsResponse = await fetch(`${API_BASE_URL}/applications/job/${jobId}`, {
            credentials: 'include'
          })
          
          if (appsResponse.ok) {
            const appsData = await appsResponse.json()
            const enrichedApps = (appsData.applications || []).map(app => ({
              ...app,
              id: app.id || app._id,
              job_title: job.title,
              job_id: jobId,
              candidate_name: app.user?.name || app.candidate_name || 'Candidate',
              candidate_email: app.user?.email || app.candidate_email,
              skills: app.profile?.skills || app.skills || [],
              user_id: app.user_id || app.user?.id
            }))
            allApplications.push(...enrichedApps)
          }
        }

        setApplications(allApplications)
      }
    } catch (err) {
      console.error('Error fetching applications:', err)
    } finally {
      setLoading(false)
    }
  }

  const viewCandidateProfile = async (userId) => {
    if (!userId) {
      alert('No user ID found for this candidate')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        setSelectedCandidate(data)
        setShowCandidateModal(true)
      } else {
        alert('Could not load candidate profile')
      }
    } catch (err) {
      console.error('Error fetching candidate:', err)
      alert('Error loading profile')
    }
  }

  const handlePostJob = async (e) => {
    e.preventDefault()
    setPostingJob(true)
    setError('')

    try {
      if (!newJob.title || !newJob.location || !newJob.description) {
        setError('Please fill in all required fields')
        setPostingJob(false)
        return
      }

      const jobData = {
        title: newJob.title,
        company: newJob.company || currentUser?.company || 'Unknown Company',
        location: newJob.location,
        type: newJob.type,
        category: newJob.category,
        description: newJob.description,
        skills_required: newJob.skills_required,
        experience_level: newJob.experience_level,
        salary_currency: newJob.salary_currency
      }

      if (newJob.salary_min) {
        jobData.salary_min = parseFloat(newJob.salary_min) * 100000
      }
      if (newJob.salary_max) {
        jobData.salary_max = parseFloat(newJob.salary_max) * 100000
      }

      const response = await fetch(`${API_BASE_URL}/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jobData),
        credentials: 'include'
      })

      const data = await response.json()

      if (response.ok) {
        await fetchJobs()
        setShowPostJob(false)
        setNewJob({
          title: '',
          company: currentUser?.company || '',
          location: '',
          type: 'Full-time',
          category: 'Software Development',
          description: '',
          skills_required: [],
          experience_level: 'mid',
          salary_min: '',
          salary_max: '',
          salary_currency: 'PKR'
        })
        setSkillInput('')
        alert('Job posted successfully!')
      } else {
        setError(data.error || 'Failed to post job')
      }
    } catch (err) {
      console.error('Error posting job:', err)
      setError('Error posting job')
    } finally {
      setPostingJob(false)
    }
  }

  const handleAddSkill = () => {
    if (skillInput && skillInput.trim() && !newJob.skills_required.includes(skillInput.trim())) {
      setNewJob(prev => ({
        ...prev,
        skills_required: [...prev.skills_required, skillInput.trim()]
      }))
      setSkillInput('')
    }
  }

  const handleRemoveSkill = (skill) => {
    setNewJob(prev => ({
      ...prev,
      skills_required: prev.skills_required.filter(s => s !== skill)
    }))
  }

  const handleUpdateApplicationStatus = async (applicationId, status) => {
    if (!applicationId) {
      console.error('No application ID provided')
      alert('Error: Application ID missing')
      return
    }

    setUpdatingStatus(applicationId)
    
    try {
      console.log(`Updating application ${applicationId} to status: ${status}`)
      
      const response = await fetch(`${API_BASE_URL}/applications/${applicationId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status }),
        credentials: 'include'
      })

      const data = await response.json()
      console.log('Update response:', data)

      if (response.ok) {
        // Refresh applications to get updated status
        await fetchApplications()
        
        // Show success message with status emoji
        const statusMessages = {
          'pending': '📋 Application marked as Pending',
          'reviewed': '👀 Application marked as Reviewed',
          'shortlisted': '⭐ Candidate shortlisted!',
          'rejected': '❌ Application rejected',
          'hired': '🎉 Candidate hired! Congratulations!'
        }
        alert(statusMessages[status] || `Application ${status} successfully!`)
      } else {
        alert(data.error || 'Failed to update status')
      }
    } catch (err) {
      console.error('Error updating status:', err)
      alert('Error updating status')
    } finally {
      setUpdatingStatus(null)
    }
  }

  const handleDeleteJob = async (jobId) => {
    if (!window.confirm('Are you sure you want to delete this job posting?')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
        method: 'DELETE',
        credentials: 'include'
      })

      if (response.ok) {
        await fetchJobs()
        await fetchApplications()
        alert('Job deleted successfully!')
      } else {
        const data = await response.json()
        alert(data.error || 'Failed to delete job')
      }
    } catch (err) {
      console.error('Error deleting job:', err)
      alert('Error deleting job')
    }
  }

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'reviewed': return 'bg-blue-100 text-blue-800'
      case 'shortlisted': return 'bg-green-100 text-green-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      case 'hired': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  // Candidate Profile Modal Component
  const CandidateModal = ({ candidate, onClose }) => {
    if (!candidate) return null
    
    const user = candidate.user || {}
    const profile = candidate.profile || {}
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
        <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
          <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white p-6 rounded-t-lg">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center text-3xl">
                  👤
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{user.name || 'Candidate'}</h2>
                  <p className="text-gray-200">{profile.position || 'Job Seeker'}</p>
                </div>
              </div>
              <button onClick={onClose} className="text-white hover:text-gray-200 text-2xl">&times;</button>
            </div>
          </div>
          
          <div className="p-6">
            {/* Contact Information */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 border-b pb-2">Contact Information</h3>
              <div className="space-y-2">
                <p><span className="font-medium">📧 Email:</span> {user.email}</p>
                {profile.phone && <p><span className="font-medium">📞 Phone:</span> {profile.phone}</p>}
                {profile.website && (
                  <p><span className="font-medium">🌐 Website:</span> <a href={profile.website} target="_blank" rel="noopener noreferrer" className="text-teal-600 hover:underline">{profile.website}</a></p>
                )}
              </div>
            </div>
            
            {/* Professional Info */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 border-b pb-2">Professional Information</h3>
              <div className="space-y-2">
                {profile.location && <p><span className="font-medium">📍 Location:</span> {profile.location}</p>}
                {profile.experience_years && <p><span className="font-medium">💼 Experience:</span> {profile.experience_years} years</p>}
                {profile.education && <p><span className="font-medium">🎓 Education:</span> {profile.education}</p>}
              </div>
            </div>
            
            {/* Skills */}
            {profile.skills && profile.skills.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 border-b pb-2">Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill, index) => (
                    <span key={index} className="bg-teal-50 text-teal-700 px-3 py-1 rounded-full text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            {/* Bio */}
            {profile.bio && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 border-b pb-2">About</h3>
                <p className="text-gray-700">{profile.bio}</p>
              </div>
            )}
            
            <div className="flex justify-end gap-3 pt-4 border-t">
              <button
                onClick={() => window.location.href = `mailto:${user.email}`}
                className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors"
              >
                📧 Contact Candidate
              </button>
              <button
                onClick={onClose}
                className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Close
              </button>
            </div>
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
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Candidate Profile Modal */}
      {showCandidateModal && (
        <CandidateModal 
          candidate={selectedCandidate} 
          onClose={() => setShowCandidateModal(false)}
        />
      )}

      <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-12">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">Recruiter Dashboard</h1>
          <p className="text-xl text-gray-100">Manage your job postings and review applications</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="text-3xl font-bold text-teal-600 mb-2">{jobs.length}</div>
            <div className="text-gray-600">Active Jobs</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="text-3xl font-bold text-green-600 mb-2">{applications.length}</div>
            <div className="text-gray-600">Total Applications</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {applications.filter(app => app.status === 'pending').length}
            </div>
            <div className="text-gray-600">Pending Review</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="text-3xl font-bold text-orange-600 mb-2">
              {applications.filter(app => app.status === 'shortlisted' || app.status === 'hired').length}
            </div>
            <div className="text-gray-600">Shortlisted/Hired</div>
          </div>
        </div>

        <div className="mb-6">
          <button
            onClick={() => setShowPostJob(!showPostJob)}
            className="bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors"
          >
            {showPostJob ? 'Cancel' : '+ Post New Job'}
          </button>
        </div>

        {showPostJob && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Post a New Job</h2>
            <form onSubmit={handlePostJob}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Job Title *</label>
                  <input
                    type="text"
                    required
                    value={newJob.title}
                    onChange={(e) => setNewJob(prev => ({ ...prev, title: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    placeholder="e.g., Senior React Developer"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company Name *</label>
                  <input
                    type="text"
                    required
                    value={newJob.company}
                    onChange={(e) => setNewJob(prev => ({ ...prev, company: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    placeholder="Your company name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Location *</label>
                  <input
                    type="text"
                    required
                    value={newJob.location}
                    onChange={(e) => setNewJob(prev => ({ ...prev, location: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    placeholder="e.g., Karachi, Pakistan or Remote"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Job Type</label>
                  <select
                    value={newJob.type}
                    onChange={(e) => setNewJob(prev => ({ ...prev, type: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="Full-time">Full-time</option>
                    <option value="Part-time">Part-time</option>
                    <option value="Contract">Contract</option>
                    <option value="Internship">Internship</option>
                    <option value="Remote">Remote</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select
                    value={newJob.category}
                    onChange={(e) => setNewJob(prev => ({ ...prev, category: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="Software Development">Software Development</option>
                    <option value="Data Science">Data Science</option>
                    <option value="DevOps">DevOps</option>
                    <option value="Design">Design</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Sales">Sales</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Experience Level</label>
                  <select
                    value={newJob.experience_level}
                    onChange={(e) => setNewJob(prev => ({ ...prev, experience_level: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="entry">Entry Level (0-1 years)</option>
                    <option value="junior">Junior (1-3 years)</option>
                    <option value="mid">Mid Level (3-5 years)</option>
                    <option value="senior">Senior (5-8 years)</option>
                    <option value="lead">Lead (8+ years)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Salary Min (LPA)</label>
                  <input
                    type="number"
                    value={newJob.salary_min}
                    onChange={(e) => setNewJob(prev => ({ ...prev, salary_min: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    placeholder="e.g., 15"
                    min="0"
                    step="1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Salary Max (LPA)</label>
                  <input
                    type="number"
                    value={newJob.salary_max}
                    onChange={(e) => setNewJob(prev => ({ ...prev, salary_max: e.target.value }))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    placeholder="e.g., 25"
                    min="0"
                    step="1"
                  />
                </div>
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Job Description *</label>
                <textarea
                  required
                  rows={5}
                  value={newJob.description}
                  onChange={(e) => setNewJob(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  placeholder="Describe the role, responsibilities, and requirements..."
                />
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Required Skills</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill())}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    placeholder="e.g., React, Python, AWS"
                  />
                  <button
                    type="button"
                    onClick={handleAddSkill}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {newJob.skills_required.map((skill, index) => (
                    <span key={index} className="bg-teal-50 text-teal-700 px-3 py-1 rounded-full text-sm flex items-center gap-2">
                      {skill}
                      <button
                        type="button"
                        onClick={() => handleRemoveSkill(skill)}
                        className="text-teal-500 hover:text-red-500"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <div className="mt-6 flex gap-3">
                <button
                  type="submit"
                  disabled={postingJob}
                  className="bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700 disabled:opacity-50 transition-colors"
                >
                  {postingJob ? 'Posting...' : 'Post Job'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowPostJob(false)}
                  className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Recent Job Postings */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-900">Your Job Postings</h2>
            <span className="text-sm text-gray-500">{jobs.length} total</span>
          </div>
          {jobs.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No jobs posted yet. Click "Post New Job" to get started.
            </div>
          ) : (
            <div className="space-y-4">
              {jobs.map(job => (
                <div key={job.id || job._id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start flex-wrap gap-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{job.title}</h3>
                      <p className="text-sm text-gray-600">{job.company} • {job.location}</p>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">{job.type}</span>
                        <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">{job.category}</span>
                        <span className={`px-2 py-1 rounded text-xs ${job.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {job.status || 'active'}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">{job.applications_count || 0} applications</p>
                      <p className="text-sm text-gray-600">{job.views_count || 0} views</p>
                      <div className="flex gap-2 mt-2">
                        <button
                          onClick={() => onNavigate('jobDetails', job.id || job._id)}
                          className="text-teal-600 text-sm hover:underline"
                        >
                          View Details →
                        </button>
                        <button
                          onClick={() => handleDeleteJob(job.id || job._id)}
                          className="text-red-600 text-sm hover:underline"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Applications */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Applications</h2>
          {applications.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No applications yet. Share your job postings to receive applications.
            </div>
          ) : (
            <div className="space-y-4">
              {applications.map(app => (
                <div key={app.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start flex-wrap gap-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{app.candidate_name}</h3>
                      <p className="text-sm text-gray-600">{app.candidate_email}</p>
                      <p className="text-sm text-gray-600">Applied for: {app.job_title}</p>
                      {app.skills && app.skills.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {app.skills.slice(0, 3).map((skill, idx) => (
                            <span key={idx} className="bg-gray-100 text-gray-700 px-2 py-0.5 rounded text-xs">
                              {skill}
                            </span>
                          ))}
                          {app.skills.length > 3 && (
                            <span className="bg-gray-100 text-gray-700 px-2 py-0.5 rounded text-xs">
                              +{app.skills.length - 3} more
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="text-right">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                        {app.match_percentage || 85}% Match
                      </span>
                      <p className="text-sm text-gray-600 mt-1">
                        Applied: {app.applied_at ? new Date(app.applied_at).toLocaleDateString() : 'Recently'}
                      </p>
                      <div className="mt-2 flex gap-2">
                        <select
                          value={app.status || 'pending'}
                          onChange={(e) => handleUpdateApplicationStatus(app.id, e.target.value)}
                          disabled={updatingStatus === app.id}
                          className={`text-xs px-2 py-1 rounded ${getStatusColor(app.status)} border focus:ring-1 focus:ring-teal-500 ${updatingStatus === app.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          <option value="pending">📋 Pending</option>
                          <option value="reviewed">👀 Reviewed</option>
                          <option value="shortlisted">⭐ Shortlisted</option>
                          <option value="rejected">❌ Rejected</option>
                          <option value="hired">🎉 Hired</option>
                        </select>
                        <button
                          onClick={() => viewCandidateProfile(app.user_id)}
                          className="text-teal-600 text-xs hover:underline"
                        >
                          👤 View Profile
                        </button>
                      </div>
                      {updatingStatus === app.id && (
                        <p className="text-xs text-gray-500 mt-1">Updating...</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default RecruiterDashboard