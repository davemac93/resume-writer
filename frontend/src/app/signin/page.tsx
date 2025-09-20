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
    <div className="min-h-screen bg-[#f8f4f0] font-['Faro',sans-serif] flex flex-col">
      {/* Header */}
      <Navbar 
        showBackButton={true} 
        backButtonHref="/" 
        backButtonText="Back to Home"
        showAuthButton={false}
      />

      {/* Main Content */}
      <div className="flex items-center justify-center px-6 py-16">
        <div className="max-w-md w-full">
          {/* Sign In Card */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-[#cfdcff] rounded-full mx-auto mb-4 flex items-center justify-center">
                <User className="w-8 h-8 text-[#1e3a2b]" />
              </div>
              <h1 className="text-4xl font-bold text-[#1e3a2b] mb-2">Welcome Back</h1>
              <p className="text-xl text-[#1e3a2b] mb-4 leading-relaxed">
                Sign in to access your saved profiles and resumes
              </p>
            </div>

            {/* Sign In Options */}
            <div className="space-y-4">
              <div className="space-y-3">
                <LoginButton 
                  user={user} 
                  onUserChange={() => {}} 
                  provider="google"
                  className="w-full"
                />
                <LoginButton 
                  user={user} 
                  onUserChange={() => {}} 
                  provider="apple"
                  className="w-full"
                />
                <LoginButton 
                  user={user} 
                  onUserChange={() => {}} 
                  provider="github"
                  className="w-full"
                />
                <LoginButton 
                  user={user} 
                  onUserChange={() => {}} 
                  provider="facebook"
                  className="w-full"
                />
              </div>
              
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">or</span>
                </div>
              </div>
              
              <div className="text-center">
                <p className="text-sm text-gray-500">
                  By signing in, you agree to our{" "}
                  <a href="#" className="text-blue-600 hover:text-blue-700">
                    Terms of Service
                  </a>{" "}
                  and{" "}
                  <a href="#" className="text-blue-600 hover:text-blue-700">
                    Privacy Policy
                  </a>
                </p>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="mt-8 text-center">
            <h3 className="text-lg font-semibold text-[#1e3a2b] mb-4">
              What you get with an account:
            </h3>
            <div className="space-y-3 text-sm text-[#1e3a2b]">
              <div className="flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-[#1e3a2b] mr-2" />
                Save and manage multiple profiles
              </div>
              <div className="flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-[#1e3a2b] mr-2" />
                Store generated resumes in the cloud
              </div>
              <div className="flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-[#1e3a2b] mr-2" />
                Access your resume history
              </div>
              <div className="flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-[#1e3a2b] mr-2" />
                Generate PDFs and download anytime
              </div>
            </div>
          </div>

          {/* Alternative Options */}
          <div className="mt-8 text-center space-y-4">
            <p className="text-[#1e3a2b]">
              Don't want to sign in? You can still create resumes without an account.
            </p>
            <div className="space-y-2">
              <a 
                href="/simple" 
                className="inline-block bg-[#cfdcff] text-[#1e3a2b] px-6 py-3 rounded-full font-semibold hover:bg-[#b8ccff] transition-colors"
              >
                Create Resume Without Account
              </a>
            </div>
          </div>
        </div>
      </div>

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
  );
}
