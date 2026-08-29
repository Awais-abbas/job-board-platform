import React from 'react'

const AboutPage = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">About JobIn</h1>
          <p className="text-xl text-gray-100 max-w-3xl mx-auto">
            Revolutionizing job matching with AI-powered resume analysis and personalized recommendations
          </p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Mission */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              To bridge the gap between talented job seekers and their dream opportunities through 
              intelligent matching technology that understands skills, experience, and potential.
            </p>
          </div>
        </section>

        {/* How It Works */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">How JobIn Works</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl mb-4">📄</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload Resume</h3>
              <p className="text-gray-600">
                Job seekers upload their resumes which are analyzed by our AI system
              </p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                Our ML algorithms extract skills, experience, and match them with job requirements
              </p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Perfect Matches</h3>
              <p className="text-gray-600">
                Get personalized job recommendations with match percentages and insights
              </p>
            </div>
          </div>
        </section>

        {/* Technology */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Powered by Advanced Technology</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="card p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Machine Learning</h3>
              <p className="text-gray-600">
                Our TF-IDF and Logistic Regression models analyze resumes with 85%+ accuracy, 
                identifying key skills and matching them to job requirements.
              </p>
            </div>
            <div className="card p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Natural Language Processing</h3>
              <p className="text-gray-600">
                Advanced NLP techniques understand job descriptions and resumes, 
                enabling semantic matching beyond simple keywords.
              </p>
            </div>
          </div>
        </section>

        {/* Features */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Key Features</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="card p-6 text-center">
              <div className="text-4xl mb-3">⚡</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Instant Results</h3>
              <p className="text-gray-600">Get job recommendations in seconds, not days</p>
            </div>
            <div className="card p-6 text-center">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Match Scoring</h3>
              <p className="text-gray-600">See exactly how well each job matches your profile</p>
            </div>
            <div className="card p-6 text-center">
              <div className="text-4xl mb-3">🔒</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure Platform</h3>
              <p className="text-gray-600">Your data is protected with enterprise-grade security</p>
            </div>
            <div className="card p-6 text-center">
              <div className="text-4xl mb-3">🌍</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Global Reach</h3>
              <p className="text-gray-600">Connect with opportunities worldwide</p>
            </div>
            <div className="card p-6 text-center">
              <div className="text-4xl mb-3">📱</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Mobile Friendly</h3>
              <p className="text-gray-600">Access ONJOB from any device, anywhere</p>
            </div>
            <div className="card p-6 text-center">
              <div className="text-4xl mb-3">💼</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Recruiter Tools</h3>
              <p className="text-gray-600">Powerful tools for employers to find talent</p>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="text-center">
          <div className="card p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Ready to Get Started?</h2>
            <p className="text-lg text-gray-600 mb-6">
              Join thousands of job seekers and recruiters who trust ONJOB
            </p>
            <div className="flex gap-4 justify-center">
              <button 
                onClick={() => onNavigate('register')}
                className="btn-primary"
              >
                Sign Up as Job Seeker
              </button>
              <button 
                onClick={() => onNavigate('register')}
                className="btn-secondary"
              >
                Sign Up as Recruiter
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default AboutPage
