import Navbar from "../components/Navbar";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f8f4f0] font-['Faro',sans-serif] flex flex-col">
      {/* Header */}
      <Navbar showAuthButton={false} />
      
      {/* Custom Get Started Button */}
      <div className="px-6 py-4 flex justify-end">
        <a href="/signin" className="bg-[#cfdcff] text-[#1e3a2b] px-6 py-2 rounded-full hover:bg-[#b8ccff] transition-colors font-semibold inline-block">
          Get Started
        </a>
      </div>

      {/* Hero Section */}
      <section className="px-6 py-16 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-[#1e3a2b] mb-6 max-w-4xl mx-auto leading-tight">
          Unlock <span className="relative">
            effortless
            <svg className="absolute -bottom-2 left-0 w-full h-3" viewBox="0 0 100 12" fill="none">
              <path d="M2 10C15 8 35 6 50 8C65 10 85 8 98 10" stroke="#cfdcff" strokeWidth="3" strokeLinecap="round" fill="none"/>
            </svg>
          </span> resume creation with AI
        </h1>
        <p className="text-xl text-[#1e3a2b] max-w-3xl mx-auto mb-8 leading-relaxed">
          Become the professional you've always dreamed of being. We give you the AI, templates, and tools you need to create winning resumes.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <a href="/simple" className="bg-[#cfdcff] text-[#1e3a2b] px-8 py-4 rounded-full text-lg font-semibold hover:bg-[#b8ccff] transition-colors inline-block text-center">
            Create Resume
          </a>
          <a href="/signin" className="border-2 border-[#1e3a2b] text-[#1e3a2b] px-8 py-4 rounded-full text-lg font-semibold hover:bg-[#1e3a2b] hover:text-white transition-colors inline-block text-center">
            Sign In
          </a>
        </div>

      </section>

      {/* Spacer to push footer to bottom */}
      <div className="flex-grow"></div>

      {/* Footer */}
      <footer className="px-6 py-8 bg-[#1e3a2b] text-white">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-4 md:mb-0">
            <span className="text-2xl font-bold">Resume.</span>
          </div>
          <div className="flex space-x-6">
            <a href="#" className="hover:text-gray-300 transition-colors">Terms</a>
            <a href="#" className="hover:text-gray-300 transition-colors">Privacy</a>
          </div>
        </div>
        <div className="text-center mt-4 text-sm text-gray-400">
          © 2024 CVBuilder. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
