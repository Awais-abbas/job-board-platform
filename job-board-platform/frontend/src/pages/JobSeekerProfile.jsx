import React, { useState, useEffect } from 'react'

const API_BASE_URL = 'http://localhost:5000/api'

const JobSeekerProfile = ({ onNavigate, currentUser, onUpdateUser }) => {
  const [profile, setProfile] = useState({
    name: currentUser?.name || '',
    email: currentUser?.email || '',
    phone: '',
    location: '',
    position: '',
    bio: '',
    experience_years: '',
    education: '',
    skills: [],
    website: '',
    company: '',
    resumeUploaded: false,
    cv_path: null
  })

  const [isEditing, setIsEditing] = useState(false)
  const [resumeFile, setResumeFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [viewingResume, setViewingResume] = useState(false)

  // Fetch profile on mount
  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      setIsLoading(true)
      
      const response = await fetch(`${API_BASE_URL}/users/me`, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        const user = data.user || {}
        const profileData = data.profile || {}
        
        setProfile({
          name: user.name || currentUser?.name || '',
          email: user.email || currentUser?.email || '',
          phone: profileData.phone || '',
          location: profileData.location || '',
          position: profileData.position || profileData.title || '',
          bio: profileData.bio || '',
          experience_years: profileData.experience_years || profileData.experience || '',
          education: profileData.education || '',
          skills: profileData.skills || [],
          website: profileData.website || '',
          company: profileData.company || '',
          resumeUploaded: !!(profileData.cv_path),
          cv_path: profileData.cv_path || null
        })
      } else if (response.status === 401) {
        setError('Please login to view your profile')
        setTimeout(() => onNavigate('login'), 2000)
      } else {
        setError('Could not load profile data')
      }
    } catch (err) {
      console.error('Error fetching profile:', err)
      setError('Could not load profile data')
    } finally {
      setIsLoading(false)
    }
  }

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload PDF, DOC, or DOCX files only')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB')
      return
    }

    setResumeFile(file)
    setIsLoading(true)
    setError('')
    setMessage('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE_URL}/users/me/upload-cv`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
      })

      const data = await response.json()

      if (response.ok) {
        setProfile(prev => ({ 
          ...prev, 
          resumeUploaded: true,
          cv_path: data.profile?.cv_path,
          skills: data.cv_data?.skills || data.profile?.skills || prev.skills,
          experience_years: data.cv_data?.experience_years || data.profile?.experience_years || prev.experience_years
        }))
        setMessage('Resume uploaded and analyzed successfully! Skills extracted!')
        setTimeout(() => fetchProfile(), 1000)
      } else {
        setError(data.error || data.message || 'Failed to upload resume')
      }
    } catch (err) {
      setError('Error uploading resume')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleViewResume = async () => {
    if (!profile.cv_path) {
      setError('No resume uploaded')
      return
    }

    setViewingResume(true)
    try {
      const response = await fetch(`${API_BASE_URL}/users/me/download-cv`, {
        credentials: 'include'
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        window.open(url, '_blank')
        setTimeout(() => window.URL.revokeObjectURL(url), 100)
      } else if (response.status === 404) {
        setError('Resume file not found')
      } else {
        setError('Failed to load resume')
      }
    } catch (err) {
      console.error('Error viewing resume:', err)
      setError('Error loading resume')
    } finally {
      setViewingResume(false)
    }
  }

  const handleDownloadResume = async () => {
    if (!profile.cv_path) {
      setError('No resume uploaded')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/me/download-cv`, {
        credentials: 'include'
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = profile.cv_path
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
        setMessage('Resume downloaded successfully!')
        setTimeout(() => setMessage(''), 3000)
      } else if (response.status === 404) {
        setError('Resume file not found')
      } else {
        setError('Failed to download resume')
      }
    } catch (err) {
      console.error('Error downloading resume:', err)
      setError('Error downloading resume')
    }
  }

  const handleDeleteResume = async () => {
    if (!window.confirm('Are you sure you want to delete your uploaded resume?')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/me/delete-cv`, {
        method: 'DELETE',
        credentials: 'include'
      })

      if (response.ok) {
        setProfile(prev => ({
          ...prev,
          resumeUploaded: false,
          cv_path: null
        }))
        setMessage('Resume deleted successfully!')
        setTimeout(() => fetchProfile(), 1000)
      } else {
        const data = await response.json()
        setError(data.error || 'Failed to delete resume')
      }
    } catch (err) {
      console.error('Error deleting resume:', err)
      setError('Error deleting resume')
    }
  }

  const handleSaveProfile = async () => {
    setIsLoading(true)
    setError('')
    setMessage('')

    try {
      const profileData = {
        name: profile.name,
        phone: profile.phone,
        location: profile.location,
        position: profile.position,
        bio: profile.bio,
        skills: profile.skills,
        experience_years: profile.experience_years,
        education: profile.education,
        website: profile.website,
        company: profile.company
      }

      const response = await fetch(`${API_BASE_URL}/users/me`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profileData),
        credentials: 'include'
      })

      const data = await response.json()

      if (response.ok) {
        setMessage('Profile saved successfully!')
        setIsEditing(false)
        await fetchProfile()
        if (onUpdateUser && profile.name !== currentUser?.name) {
          onUpdateUser({ ...currentUser, name: profile.name })
        }
      } else {
        setError(data.error || 'Failed to save profile')
      }
    } catch (err) {
      setError('Error saving profile')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddSkill = () => {
    const skill = prompt('Enter a skill:')
    if (skill && skill.trim() && !profile.skills.includes(skill.trim())) {
      setProfile(prev => ({
        ...prev,
        skills: [...prev.skills, skill.trim()]
      }))
    }
  }

  const handleRemoveSkill = (skillToRemove) => {
    setProfile(prev => ({
      ...prev,
      skills: prev.skills.filter(skill => skill !== skillToRemove)
    }))
  }

  const getFileIcon = (filename) => {
    if (!filename) return '📄'
    const ext = filename.split('.').pop().toLowerCase()
    if (ext === 'pdf') return '📕'
    if (ext === 'doc' || ext === 'docx') return '📘'
    return '📄'
  }

  if (isLoading && !profile.name) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin border-4 border-gray-300 border-t-teal-600 rounded-full w-12 h-12"></div>
          <p className="mt-4 text-gray-600">Loading profile...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Profile Header */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-6">
              <div className="w-32 h-32 bg-white rounded-full flex items-center justify-center text-5xl">
                👤
              </div>
              <div>
                <h1 className="text-4xl font-bold">{profile.name || 'Complete Your Profile'}</h1>
                <p className="text-xl text-gray-100">{profile.position || 'Job Seeker'}</p>
                <p className="text-gray-200">{profile.location || 'Location not set'}</p>
              </div>
            </div>
            <button 
              onClick={() => setIsEditing(!isEditing)}
              className="bg-white text-teal-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              {isEditing ? 'Cancel' : 'Edit Profile'}
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      {message && (
        <div className="max-w-6xl mx-auto px-4 mt-4">
          <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg">{message}</div>
        </div>
      )}
      {error && (
        <div className="max-w-6xl mx-auto px-4 mt-4">
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg">{error}</div>
        </div>
      )}

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Resume Upload */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Resume & CV</h2>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <div className="text-5xl mb-4">{profile.resumeUploaded ? getFileIcon(profile.cv_path) : '📄'}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {profile.resumeUploaded ? 'Resume Uploaded' : 'Upload Your Resume'}
                </h3>
                <p className="text-gray-600 mb-4">
                  {profile.resumeUploaded 
                    ? 'Your resume has been analyzed for job recommendations'
                    : 'Upload your resume to get personalized job recommendations (PDF, DOC, DOCX up to 5MB)'
                  }
                </p>
                
                {profile.resumeUploaded && profile.cv_path && (
                  <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-2">📁 File: {profile.cv_path}</p>
                    <div className="flex gap-3 justify-center">
                      <button
                        onClick={handleViewResume}
                        disabled={viewingResume}
                        className="bg-teal-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors text-sm"
                      >
                        {viewingResume ? 'Loading...' : '👁️ View Resume'}
                      </button>
                      <button
                        onClick={handleDownloadResume}
                        className="bg-gray-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-gray-700 transition-colors text-sm"
                      >
                        💾 Download Resume
                      </button>
                      {isEditing && (
                        <button
                          onClick={handleDeleteResume}
                          className="bg-red-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-700 transition-colors text-sm"
                        >
                          🗑️ Delete Resume
                        </button>
                      )}
                    </div>
                  </div>
                )}

                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={handleResumeUpload}
                  className="hidden"
                  id="resume-upload"
                />
                <label 
                  htmlFor="resume-upload"
                  className="bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700 cursor-pointer inline-block transition-colors"
                >
                  {isLoading ? 'Uploading...' : (profile.resumeUploaded ? '📤 Update Resume' : '📤 Choose File')}
                </label>
                {resumeFile && (
                  <p className="mt-2 text-sm text-gray-600">Selected: {resumeFile.name}</p>
                )}
              </div>
              {profile.resumeUploaded && profile.skills && profile.skills.length > 0 && (
                <div className="mt-4 p-4 bg-green-50 rounded-lg">
                  <p className="text-green-800 text-sm">
                    ✅ Resume successfully analyzed! Extracted {profile.skills.length} skills.
                  </p>
                </div>
              )}
            </div>

            {/* Personal Information */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Personal Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    value={profile.name}
                    onChange={(e) => setProfile(prev => ({ ...prev, name: e.target.value }))}
                    disabled={!isEditing}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={profile.email}
                    disabled={true}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                  <input
                    type="tel"
                    value={profile.phone}
                    onChange={(e) => setProfile(prev => ({ ...prev, phone: e.target.value }))}
                    disabled={!isEditing}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                    placeholder="+92 300 1234567"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                  <input
                    type="text"
                    value={profile.location}
                    onChange={(e) => setProfile(prev => ({ ...prev, location: e.target.value }))}
                    disabled={!isEditing}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                    placeholder="e.g., Karachi, Pakistan"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Job Title / Position</label>
                  <input
                    type="text"
                    value={profile.position}
                    onChange={(e) => setProfile(prev => ({ ...prev, position: e.target.value }))}
                    disabled={!isEditing}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                    placeholder="e.g., Senior Software Engineer"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Website/Portfolio</label>
                  <input
                    type="url"
                    value={profile.website}
                    onChange={(e) => setProfile(prev => ({ ...prev, website: e.target.value }))}
                    disabled={!isEditing}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                    placeholder="https://yourportfolio.com"
                  />
                </div>
              </div>
              
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
                <textarea
                  value={profile.bio}
                  onChange={(e) => setProfile(prev => ({ ...prev, bio: e.target.value }))}
                  disabled={!isEditing}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="Tell us about yourself..."
                />
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Education</label>
                <input
                  type="text"
                  value={profile.education}
                  onChange={(e) => setProfile(prev => ({ ...prev, education: e.target.value }))}
                  disabled={!isEditing}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="e.g., Bachelor of Computer Science - ABC University"
                />
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Years of Experience</label>
                <input
                  type="number"
                  value={profile.experience_years}
                  onChange={(e) => setProfile(prev => ({ ...prev, experience_years: e.target.value }))}
                  disabled={!isEditing}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="e.g., 3"
                  min="0"
                  step="0.5"
                />
              </div>

              {isEditing && (
                <button
                  onClick={handleSaveProfile}
                  disabled={isLoading}
                  className="mt-6 bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? 'Saving...' : 'Save Changes'}
                </button>
              )}
            </div>

            {/* Skills */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-900">Skills</h2>
                {isEditing && (
                  <button
                    onClick={handleAddSkill}
                    className="text-teal-600 font-semibold hover:text-teal-700"
                  >
                    + Add Skill
                  </button>
                )}
              </div>
              <div className="flex flex-wrap gap-2">
                {profile.skills && profile.skills.length > 0 ? (
                  profile.skills.map((skill, index) => (
                    <span key={index} className="bg-teal-50 text-teal-700 px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-2">
                      {skill}
                      {isEditing && (
                        <button
                          onClick={() => handleRemoveSkill(skill)}
                          className="text-teal-500 hover:text-red-500"
                        >
                          ×
                        </button>
                      )}
                    </span>
                  ))
                ) : (
                  <p className="text-gray-500 text-sm">No skills added yet. Click "Add Skill" or upload a resume to extract skills automatically.</p>
                )}
              </div>
              <p className="mt-4 text-sm text-gray-600">
                {profile.resumeUploaded 
                  ? 'Skills are extracted from your resume. You can add or remove skills manually.'
                  : 'Upload your resume to automatically extract skills, or add them manually for better job matches.'}
              </p>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button 
                  onClick={() => onNavigate('recommendations')}
                  className="w-full bg-teal-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors"
                >
                  View Recommendations
                </button>
                <button 
                  onClick={() => onNavigate('jobs')}
                  className="w-full border border-teal-600 text-teal-600 px-4 py-2 rounded-lg font-semibold hover:bg-teal-50 transition-colors"
                >
                  Browse Jobs
                </button>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Profile Completion</h3>
              <div className="mb-2">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Overall</span>
                  <span>
                    {Math.round(Object.values({
                      name: profile.name ? 1 : 0,
                      email: profile.email ? 1 : 0,
                      resume: profile.resumeUploaded ? 1 : 0,
                      skills: profile.skills?.length > 0 ? 1 : 0,
                      location: profile.location ? 1 : 0,
                      position: profile.position ? 1 : 0,
                      experience: profile.experience_years ? 1 : 0
                    }).filter(v => v === 1).length / 7 * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-teal-600 h-2 rounded-full transition-all" 
                    style={{ width: `${Object.values({
                      name: profile.name ? 1 : 0,
                      email: profile.email ? 1 : 0,
                      resume: profile.resumeUploaded ? 1 : 0,
                      skills: profile.skills?.length > 0 ? 1 : 0,
                      location: profile.location ? 1 : 0,
                      position: profile.position ? 1 : 0,
                      experience: profile.experience_years ? 1 : 0
                    }).filter(v => v === 1).length / 7 * 100}%` }}
                  ></div>
                </div>
              </div>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>{profile.name ? '✅' : '❌'} Personal Information</li>
                <li>{profile.resumeUploaded ? '✅' : '❌'} Resume Uploaded</li>
                <li>{profile.skills?.length > 0 ? '✅' : '❌'} Skills Added ({profile.skills?.length || 0})</li>
                <li>{profile.position ? '✅' : '❌'} Job Title</li>
                <li>{profile.experience_years ? '✅' : '❌'} Experience</li>
                <li>{profile.location ? '✅' : '❌'} Location</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default JobSeekerProfile