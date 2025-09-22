"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../contexts/AuthContext";
import LoginButton from "../../components/LoginButton";
import Navbar from "../../components/Navbar";
import { User, CheckCircle } from "lucide-react";

export default function SignInPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (!loading && user) {
      router.push("/resume-writer");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Already Signed In</h1>
          <p className="text-gray-600 mb-4">Redirecting to your dashboard...</p>
        </div>
      </div>
    );
  }

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
          <a href="/signin" className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
            • Get Started
          </a>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-6">
        <div className="text-center max-w-2xl mx-auto">
          {/* Large Bold Text */}
          <div className="mb-16">
            <div className="text-4xl md:text-6xl lg:text-7xl font-black text-black uppercase leading-[0.85] tracking-tight">
              <div>WELCOME</div>
              <div>TO RESUME.</div>
              <div>SIGN IN TO</div>
              <div>GET STARTED</div>
            </div>
          </div>

          {/* Sign In Options */}
          <div className="space-y-4 mb-12">
            <div className="w-full">
              <LoginButton 
                user={user} 
                onUserChange={() => {}} 
                provider="google"
                className="w-full justify-start"
              />
            </div>
            <div className="w-full">
              <LoginButton 
                user={user} 
                onUserChange={() => {}} 
                provider="apple"
                className="w-full justify-start"
              />
            </div>
            <div className="w-full">
              <LoginButton 
                user={user} 
                onUserChange={() => {}} 
                provider="github"
                className="w-full justify-start"
              />
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
