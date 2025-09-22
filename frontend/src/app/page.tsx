"use client";
import Navbar from "../components/Navbar";
import { useAuth } from "../contexts/AuthContext";

export default function Home() {
  const { user } = useAuth();
  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Header */}
      <header className="px-6 py-6 flex items-center justify-between">
        <div className="flex items-center">
          <a href="/" className="text-black text-xl font-bold hover:text-gray-700 transition-colors">
            resume.
          </a>
        </div>
        
        <nav className="hidden md:flex space-x-8">
          <a href="#pricing" className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
            • Pricing
          </a>
          <a href={user ? "/resume-writer" : "/signin"} className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
            • Get Started
          </a>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-6">
        <div className="text-center max-w-5xl mx-auto">
          {/* Large Bold Text */}
          <div className="mb-20">
            <div className="text-4xl md:text-6xl lg:text-7xl font-black text-black uppercase leading-[0.85] tracking-tight">
              <div>HELLO! I'M DAVE</div>
              <div>YOUR PERSONAL AI</div>
              <div>ASSISTANT</div>
              <div>HERE TO HELP YOU</div>
              <div>CREATE THE PERFECT</div>
              <div>RESUME FOR YOUR</div>
              <div>FUTURE JOB</div>
            </div>
          </div>

          {/* Start Creating Button with Geometric Effects */}
          <div className="relative inline-block">
            <a 
              href={user ? "/resume-writer" : "/signin"} 
              className="relative bg-white text-black px-16 py-8 text-2xl font-medium hover:bg-gray-50 transition-colors inline-block border-2 border-black group"
            >
              Start creating
            </a>
            
            {/* Geometric Lines - Top Left Corner */}
            <div className="absolute -top-0.5 -left-0.5 w-20 h-px bg-black"></div>
            <div className="absolute -top-0.5 -left-0.5 w-px h-20 bg-black"></div>
            
            {/* Geometric Lines - Top Right Corner */}
            <div className="absolute -top-0.5 -right-0.5 w-20 h-px bg-black"></div>
            <div className="absolute -top-0.5 -right-0.5 w-px h-20 bg-black"></div>
            
            {/* Geometric Lines - Bottom Left Corner */}
            <div className="absolute -bottom-0.5 -left-0.5 w-20 h-px bg-black"></div>
            <div className="absolute -bottom-0.5 -left-0.5 w-px h-20 bg-black"></div>
            
            {/* Geometric Lines - Bottom Right Corner */}
            <div className="absolute -bottom-0.5 -right-0.5 w-20 h-px bg-black"></div>
            <div className="absolute -bottom-0.5 -right-0.5 w-px h-20 bg-black"></div>
          </div>
        </div>
      </main>

    </div>
  )
}
