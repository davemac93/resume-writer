"use client";
import Navbar from "../components/Navbar";
import { useAuth } from "../contexts/AuthContext";

export default function Home() {
  const { user } = useAuth();
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Navbar showAuthButton={false} />

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

          {/* Start Creating Button with Colorful Gradient */}
          <div className="flex justify-center">
            <a 
              href={user ? "/resume-writer" : "/signin"} 
              className="px-16 py-8 text-2xl font-medium text-white bg-black hover:bg-gray-800 transition-colors relative overflow-hidden group rounded-lg"
              style={{
                background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57, #ff9ff3, #54a0ff)',
                backgroundSize: '400% 400%',
                animation: 'gradientShift 3s ease infinite'
              }}
            >
              <span className="relative z-10 flex items-center justify-center">
                Start creating
              </span>
            </a>
          </div>
        </div>
      </main>

    </div>
  )
}
