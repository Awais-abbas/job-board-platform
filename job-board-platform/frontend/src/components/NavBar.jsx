import React, { useState } from 'react'

const NavBar = ({ currentPage, currentUser, onNavigate, onLogout }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)

  const handleNavClick = (page) => {
    onNavigate(page)
    setIsDropdownOpen(false)
  }

  return (
    <nav className="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <button 
              onClick={() => handleNavClick('home')}
              className="flex items-center gap-2 text-2xl font-bold text-primary-600 hover:text-primary-700 cursor-pointer transition-colors"
            >
              <span className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm">�</span>
              JobIn
            </button>
          </div>

          {/* Navigation Links - Centered */}
          <div className="hidden md:flex items-center space-x-8">
            <button 
              onClick={() => handleNavClick('home')}
              className={`nav-link ${currentPage === 'home' ? 'nav-link-active' : ''}`}
            >
              Home
            </button>
            <button 
              onClick={() => handleNavClick('jobs')}
              className={`nav-link ${currentPage === 'jobs' ? 'nav-link-active' : ''}`}
            >
              Jobs
            </button>
            {currentUser && (
              <button 
                onClick={() => handleNavClick('recommendations')}
                className={`nav-link ${currentPage === 'recommendations' ? 'nav-link-active' : ''}`}
              >
                For You
              </button>
            )}
            <button 
              onClick={() => handleNavClick('about')}
              className={`nav-link ${currentPage === 'about' ? 'nav-link-active' : ''}`}
            >
              About Us
            </button>
            <button 
              onClick={() => handleNavClick('contact')}
              className={`nav-link ${currentPage === 'contact' ? 'nav-link-active' : ''}`}
            >
              Contact Us
            </button>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {!currentUser ? (
              <div className="flex items-center space-x-3">
                <button 
                  onClick={() => handleNavClick('login')}
                  className="nav-link"
                >
                  Login
                </button>
                <button 
                  onClick={() => handleNavClick('register')}
                  className="btn-primary"
                >
                  Sign Up
                </button>
              </div>
            ) : (
              <div className="relative">
                <button
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                  className="flex items-center space-x-2 text-gray-700 hover:text-gray-900 cursor-pointer transition-colors"
                >
                  <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {currentUser.name.charAt(0).toUpperCase()}
                  </div>
                  <span className="font-medium">{currentUser.name}</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {/* Dropdown Menu */}
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                    <button 
                      onClick={() => handleNavClick('profile')}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                    >
                      My Profile
                    </button>
                    {currentUser.role === 'jobseeker' && (
                      <button 
                        onClick={() => handleNavClick('recommendations')}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                      >
                        Job Recommendations
                      </button>
                    )}
                    {currentUser.role === 'recruiter' && (
                      <button 
                        onClick={() => handleNavClick('recruiter')}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                      >
                        Recruiter Dashboard
                      </button>
                    )}
                    <hr className="my-1" />
                    <button 
                      onClick={onLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default NavBar
