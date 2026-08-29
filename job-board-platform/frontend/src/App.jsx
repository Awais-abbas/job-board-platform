import React, { useState, useEffect } from 'react'
import NavBar from './components/NavBar'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import JobsPage from './pages/JobsPage'
import JobDetailsPage from './pages/JobDetailsPage'
import JobSeekerProfile from './pages/JobSeekerProfile'
import JobRecommendations from './pages/JobRecommendations'
import RecruiterDashboard from './pages/RecruiterDashboard'
import AboutPage from './pages/AboutPage'
import ContactPage from './pages/ContactPage'

const API_BASE_URL = 'http://localhost:5000/api'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [currentUser, setCurrentUser] = useState(null)
  const [selectedJobId, setSelectedJobId] = useState(null)
  const [selectedUserId, setSelectedUserId] = useState(null) // For viewing other users' profiles
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check session on app load
    checkSession()
  }, [])

  const checkSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        setCurrentUser(data.user)
      }
    } catch (err) {
      console.error('Session check failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      })
    } catch (err) {
      console.error('Logout error:', err)
    }
    
    setCurrentUser(null)
    setCurrentPage('home')
  }

  const handleNavigate = (page, id = null) => {
    setCurrentPage(page)
    if (page === 'jobDetails') {
      setSelectedJobId(id)
      setSelectedUserId(null)
    } else if (page === 'candidateProfile') {
      setSelectedUserId(id)
      setSelectedJobId(null)
    } else {
      setSelectedJobId(null)
      setSelectedUserId(null)
    }
  }

  const handleLogin = (userData) => {
    setCurrentUser(userData)
    // Redirect based on role
    if (userData.role === 'recruiter') {
      setCurrentPage('recruiter')
    } else {
      setCurrentPage('dashboard')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin border-4 border-gray-300 border-t-teal-600 rounded-full w-12 h-12"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} currentUser={currentUser} />
      case 'login':
        return <LoginPage onNavigate={handleNavigate} onLogin={handleLogin} />
      case 'register':
        return <RegisterPage onNavigate={handleNavigate} onLogin={handleLogin} />
      case 'jobs':
        return <JobsPage onNavigate={handleNavigate} currentUser={currentUser} />
      case 'jobDetails':
        return <JobDetailsPage jobId={selectedJobId} onNavigate={handleNavigate} currentUser={currentUser} />
      case 'profile':
        return currentUser ? <JobSeekerProfile onNavigate={handleNavigate} currentUser={currentUser} onUpdateUser={setCurrentUser} /> : <LoginPage onNavigate={handleNavigate} onLogin={handleLogin} />
      case 'candidateProfile':
        // View another user's profile (read-only mode)
        return <JobSeekerProfile 
          onNavigate={handleNavigate} 
          currentUser={currentUser} 
          viewUserId={selectedUserId}
          isViewOnly={true}
        />
      case 'dashboard':
        return currentUser ? <JobRecommendations onNavigate={handleNavigate} currentUser={currentUser} /> : <LoginPage onNavigate={handleNavigate} onLogin={handleLogin} />
      case 'recommendations':
        return currentUser ? <JobRecommendations onNavigate={handleNavigate} currentUser={currentUser} /> : <LoginPage onNavigate={handleNavigate} onLogin={handleLogin} />
      case 'recruiter':
        return currentUser ? <RecruiterDashboard onNavigate={handleNavigate} currentUser={currentUser} /> : <LoginPage onNavigate={handleNavigate} onLogin={handleLogin} />
      case 'about':
        return <AboutPage onNavigate={handleNavigate} />
      case 'contact':
        return <ContactPage onNavigate={handleNavigate} />
      default:
        return <HomePage onNavigate={handleNavigate} currentUser={currentUser} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar 
        currentPage={currentPage} 
        currentUser={currentUser} 
        onNavigate={handleNavigate}
        onLogout={handleLogout}
      />
      <main className="flex-grow">
        {renderPage()}
      </main>
    </div>
  )
}

export default App