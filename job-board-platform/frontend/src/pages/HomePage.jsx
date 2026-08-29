import React, { useState } from 'react'

const HomePage = ({ onNavigate, currentUser }) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [locationQuery, setLocationQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')

  const jobs = [
    {
      id: 1,
      title: 'Frontend Developer',
      company: 'Melton Ltd',
      location: 'Copelandtown, Cuba',
      salary: '$105068',
      salaryType: 'per year',
      type: 'Internship',
      category: 'Frontend Developer',
      tags: ['Kubernetes', 'Django', 'Python'],
      postedDate: '8/1/2025',
      companyLogo: '🟦'
    },
    {
      id: 2,
      title: 'Data Scientist',
      company: 'Marsh, Flores and Vega',
      location: 'Lake Alexis, Ethiopia',
      salary: '$170212',
      salaryType: 'per year',
      type: 'Remote',
      category: 'Data Scientist',
      tags: ['Flask', 'Tailwind CSS', 'JavaScript'],
      postedDate: '8/1/2025',
      companyLogo: '🟢'
    },
    {
      id: 3,
      title: 'Mobile App Developer',
      company: 'Young-Lee',
      location: 'North Paulbury, Sierra Leone',
      salary: '$117233',
      salaryType: 'per year',
      type: 'Remote',
      category: 'Mobile App Developer',
      tags: ['Adobe XD', 'Docker', 'React'],
      postedDate: '8/1/2025',
      companyLogo: '🍎'
    }
  ]

  const handleSearch = () => {
    onNavigate('jobs')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section with Search Bar */}
      <section className="relative bg-gradient-to-r from-gray-800 to-gray-900 text-white py-16">
        <div className="absolute inset-0 bg-black opacity-40"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Explore Available Jobs
            </h1>
            <p className="text-lg text-gray-200">
              A personalized career search and hiring system.
            </p>
          </div>

          {/* Search Bar - Horizontal */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg flex flex-col md:flex-row overflow-hidden">
              <div className="flex-1 flex items-center px-4 py-3 border-b md:border-b-0 md:border-r border-gray-200">
                <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="Job title, keywords"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
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
                  placeholder="Location (city, state)"
                  value={locationQuery}
                  onChange={(e) => setLocationQuery(e.target.value)}
                  className="w-full outline-none text-gray-700 placeholder-gray-400"
                />
              </div>
              <div className="flex-1 flex items-center px-4 py-3 border-b md:border-b-0 md:border-r border-gray-200">
                <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
                </svg>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full outline-none text-gray-700 bg-white cursor-pointer"
                >
                  <option value="">All Categories</option>
                  <option value="Frontend Developer">Frontend Developer</option>
                  <option value="Data Scientist">Data Scientist</option>
                  <option value="Mobile App Developer">Mobile App Developer</option>
                  <option value="Backend Developer">Backend Developer</option>
                </select>
              </div>
              <button
                onClick={handleSearch}
                className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 font-semibold transition-colors cursor-pointer flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search
              </button>
            </div>
          </div>

          {/* Stats */}
          <div className="flex justify-center gap-6 mt-8">
            <div className="bg-gray-800 bg-opacity-50 rounded-lg px-6 py-3 text-center">
              <div className="text-2xl font-bold">20,100</div>
              <div className="text-sm text-gray-300">Active Jobs</div>
            </div>
            <div className="bg-gray-800 bg-opacity-50 rounded-lg px-6 py-3 text-center">
              <div className="text-2xl font-bold">2</div>
              <div className="text-sm text-gray-300">Job Seekers</div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content - Filters + Job Cards */}
      <section className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Left Sidebar - Filters */}
            <div className="lg:w-1/4">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">All Filters</h3>
                  <button className="text-primary-600 text-sm hover:underline cursor-pointer">Reset All</button>
                </div>

                {/* Location Filter */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    </svg>
                    Location
                  </h4>
                  <input
                    type="text"
                    placeholder="City or postcode"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm outline-none focus:border-primary-600"
                  />
                </div>

                {/* Job Category Filter */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    Job Category
                  </h4>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm outline-none focus:border-primary-600 cursor-pointer">
                    <option>All Categories</option>
                    <option>Frontend Developer</option>
                    <option>Data Scientist</option>
                    <option>Mobile App Developer</option>
                  </select>
                </div>

                {/* Sort By */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                    </svg>
                    Sort By
                  </h4>
                  <div className="space-y-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="sort" className="text-primary-600" defaultChecked />
                      <span className="text-sm text-gray-700">Most Recent</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="sort" className="text-primary-600" />
                      <span className="text-sm text-gray-700">Oldest</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="sort" className="text-primary-600" />
                      <span className="text-sm text-gray-700">Salary High to Low</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input type="radio" name="sort" className="text-primary-600" />
                      <span className="text-sm text-gray-700">Salary Low to High</span>
                    </label>
                  </div>
                </div>

                <button className="w-full border border-gray-300 text-gray-700 py-2 rounded-md text-sm hover:bg-gray-50 transition-colors cursor-pointer">
                  Clear All Filters
                </button>
              </div>
            </div>

            {/* Right Side - Job Cards */}
            <div className="lg:w-3/4">
              <div className="space-y-4">
                {jobs.map((job) => (
                  <div key={job.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex gap-4">
                        <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-2xl">
                          {job.companyLogo}
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">{job.title} at {job.company}</h3>
                          <p className="text-sm text-gray-600">{job.company}</p>
                        </div>
                      </div>
                      <span className="text-sm text-gray-500">{job.postedDate}</span>
                    </div>

                    <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                        </svg>
                        {job.location}
                      </span>
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                        </svg>
                        ${job.salary} {job.salaryType}
                      </span>
                    </div>

                    <div className="flex flex-wrap gap-2 mb-4">
                      <span className="flex items-center gap-1 text-sm text-gray-700">
                        <svg className="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
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
                        className="text-primary-600 font-medium text-sm hover:text-primary-700 transition-colors cursor-pointer"
                      >
                        View Details →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
