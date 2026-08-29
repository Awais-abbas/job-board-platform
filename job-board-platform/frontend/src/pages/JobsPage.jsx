import React, { useState, useEffect } from 'react'

const API_BASE_URL = 'http://localhost:5000/api'

const JobsPage = ({ onNavigate, currentUser }) => {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({
    search: '',
    location: '',
    type: '',
    category: ''
  })

  useEffect(() => {
    fetchJobs()
  }, [])

  const fetchJobs = async () => {
    try {
      setLoading(true)
      setError('')
      
      // Build query string from filters
      const params = new URLSearchParams()
      if (filters.search) params.append('search', filters.search)
      if (filters.location) params.append('location', filters.location)
      if (filters.type) params.append('type', filters.type)
      if (filters.category) params.append('category', filters.category)
      
      const queryString = params.toString()
      const url = `${API_BASE_URL}/jobs${queryString ? `?${queryString}` : ''}`
      
      const response = await fetch(url, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        // Transform backend data to frontend format
        const transformedJobs = (data.jobs || []).map(job => ({
          id: job.id || job._id,
          title: job.title,
          company: job.company,
          location: job.location,
          salary: job.salary_min && job.salary_max 
            ? `${job.salary_currency === 'PKR' ? 'PKR' : '$'} ${(job.salary_min/100000).toFixed(1)}-${(job.salary_max/100000).toFixed(1)} LPA`
            : 'Salary not disclosed',
          type: job.type,
          category: job.category,
          tags: job.skills_required || [],
          description: job.description,
          postedDate: job.created_at ? new Date(job.created_at).toISOString().split('T')[0] : 'Recently'
        }))
        setJobs(transformedJobs)
      } else {
        setError('Failed to fetch jobs')
      }
    } catch (err) {
      console.error('Error fetching jobs:', err)
      setError('Error connecting to server')
    } finally {
      setLoading(false)
    }
  }

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchJobs()
    }, 500)
    return () => clearTimeout(timer)
  }, [filters.search, filters.location, filters.type, filters.category])

  const handleFilterChange = (e) => {
    setFilters(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(filters.search.toLowerCase()) ||
                         job.company.toLowerCase().includes(filters.search.toLowerCase())
    const matchesLocation = !filters.location || job.location.toLowerCase().includes(filters.location.toLowerCase())
    const matchesType = !filters.type || job.type === filters.type
    const matchesCategory = !filters.category || job.category === filters.category
    
    return matchesSearch && matchesLocation && matchesType && matchesCategory
  })

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin border-4 border-gray-300 border-t-teal-600 rounded-full w-12 h-12"></div>
          <p className="mt-4 text-gray-600">Loading jobs...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with Search Bar */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-4 text-center">Browse Jobs</h1>
          <p className="text-xl text-gray-100 text-center mb-8">
            Discover opportunities that match your skills and experience
          </p>

          {/* Prominent Search Bar */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg flex flex-col md:flex-row overflow-hidden">
              <div className="flex-1 flex items-center px-4 py-3 border-b md:border-b-0 md:border-r border-gray-200">
                <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  name="search"
                  placeholder="Job title, keywords"
                  value={filters.search}
                  onChange={handleFilterChange}
                  className="w-full outline-none text-gray-700 placeholder-gray-400"
                />
              </div>
              <div className="flex-1 flex items-center px-4 py-3 border-b md:border-b-0 md:border-r border-gray-200">
                <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <input
                  type="text"
                  name="location"
                  placeholder="Location (city, state)"
                  value={filters.location}
                  onChange={handleFilterChange}
                  className="w-full outline-none text-gray-700 placeholder-gray-400"
                />
              </div>
              <div className="flex-1 flex items-center px-4 py-3 border-b md:border-b-0 md:border-r border-gray-200">
                <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
                </svg>
                <select
                  name="category"
                  value={filters.category}
                  onChange={handleFilterChange}
                  className="w-full outline-none text-gray-700 bg-white cursor-pointer"
                >
                  <option value="">All Categories</option>
                  <option value="Software Development">Software Development</option>
                  <option value="Data Science">Data Science</option>
                  <option value="DevOps">DevOps</option>
                  <option value="Design">Design</option>
                  <option value="Marketing">Marketing</option>
                </select>
              </div>
              <button
                className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 font-semibold transition-colors cursor-pointer flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search
              </button>
            </div>
          </div>

          {/* Stats */}
          <div className="flex justify-center gap-6 mt-6">
            <div className="bg-gray-800 bg-opacity-50 rounded-lg px-6 py-3 text-center">
              <div className="text-2xl font-bold">{filteredJobs.length}</div>
              <div className="text-sm text-gray-300">Jobs Found</div>
            </div>
            <div className="bg-gray-800 bg-opacity-50 rounded-lg px-6 py-3 text-center">
              <div className="text-2xl font-bold">{jobs.length}</div>
              <div className="text-sm text-gray-300">Total Jobs</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <div className="lg:w-1/4">
            <div className="card p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">All Filters</h3>
                <button 
                  onClick={() => setFilters({ search: '', location: '', type: '', category: '' })}
                  className="text-teal-600 text-sm hover:underline cursor-pointer"
                >
                  Reset All
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
                    Location
                  </label>
                  <input
                    type="text"
                    id="location"
                    name="location"
                    value={filters.location}
                    onChange={handleFilterChange}
                    placeholder="City or country"
                    className="input-field"
                  />
                </div>

                <div>
                  <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-1">
                    Job Type
                  </label>
                  <select
                    id="type"
                    name="type"
                    value={filters.type}
                    onChange={handleFilterChange}
                    className="input-field"
                  >
                    <option value="">All Types</option>
                    <option value="Full-time">Full-time</option>
                    <option value="Part-time">Part-time</option>
                    <option value="Contract">Contract</option>
                    <option value="Internship">Internship</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                    Category
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={filters.category}
                    onChange={handleFilterChange}
                    className="input-field"
                  >
                    <option value="">All Categories</option>
                    <option value="Software Development">Software Development</option>
                    <option value="Data Science">Data Science</option>
                    <option value="DevOps">DevOps</option>
                    <option value="Design">Design</option>
                    <option value="Marketing">Marketing</option>
                  </select>
                </div>

                <button
                  onClick={() => setFilters({ search: '', location: '', type: '', category: '' })}
                  className="w-full border border-gray-300 text-gray-700 py-2 rounded-md text-sm hover:bg-gray-50 transition-colors cursor-pointer"
                >
                  Clear All Filters
                </button>
              </div>
            </div>
          </div>

          {/* Jobs List */}
          <div className="lg:w-3/4">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                {filteredJobs.length} Jobs Found
              </h2>
              {currentUser && (
                <button
                  onClick={() => onNavigate('recommendations')}
                  className="bg-teal-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors cursor-pointer"
                >
                  View Recommendations
                </button>
              )}
            </div>

            <div className="space-y-4">
              {filteredJobs.map(job => (
                <div key={job.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex gap-4">
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-2xl">
                        🏢
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                        <p className="text-sm text-gray-600">{job.company}</p>
                      </div>
                    </div>
                    <span className="text-sm text-gray-500">{new Date(job.postedDate).toLocaleDateString()}</span>
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
                  </div>

                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="flex items-center gap-1 text-sm text-gray-700">
                      <svg className="w-4 h-4 text-teal-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
                        <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                      </svg>
                      {job.category}
                    </span>
                    <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
                      {job.type}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {job.tags.map((tag, index) => (
                      <span key={index} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs">
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className="flex justify-end">
                    <button
                      onClick={() => onNavigate('jobDetails', job.id)}
                      className="text-teal-600 font-medium text-sm hover:text-teal-700 transition-colors cursor-pointer"
                    >
                      View Details →
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {filteredJobs.length === 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-5xl mb-4">🔍</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No jobs found</h3>
                <p className="text-gray-600 mb-4">
                  Try adjusting your filters or search terms
                </p>
                <button
                  onClick={() => setFilters({ search: '', location: '', type: '', category: '' })}
                  className="bg-teal-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors cursor-pointer"
                >
                  Clear Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default JobsPage
