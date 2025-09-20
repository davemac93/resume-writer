"use client";
import { useAuth } from "../../contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Navbar from "../../components/Navbar";
import { User, FileText, Download, Settings, ArrowRight } from "lucide-react";

export default function Dashboard() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/signin");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect to signin
  }

  return (
    <div className="min-h-screen bg-[#f8f4f0] font-['Faro',sans-serif] flex flex-col">
      {/* Header */}
      <Navbar showAuthButton={true} />

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200 mb-8">
          <div className="flex items-center mb-6">
            <div className="w-16 h-16 bg-[#cfdcff] rounded-full flex items-center justify-center mr-4">
              <User className="w-8 h-8 text-[#1e3a2b]" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-[#1e3a2b]">
                Welcome back, {user.user_metadata?.full_name || user.email}!
              </h1>
              <p className="text-xl text-[#1e3a2b] leading-relaxed">
                Manage your profiles and resumes from your dashboard
              </p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl transition-shadow">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-[#cfdcff] rounded-full mr-4">
                <FileText className="w-6 h-6 text-[#1e3a2b]" />
              </div>
              <h3 className="text-xl font-bold text-[#1e3a2b]">Create Resume</h3>
            </div>
            <p className="text-[#1e3a2b] mb-4">
              Generate a new professional resume using AI
            </p>
            <a
              href="/resume-writer"
              className="inline-flex items-center text-[#1e3a2b] hover:text-[#2d4a3b] font-semibold"
            >
              Get Started
              <ArrowRight className="w-4 h-4 ml-2" />
            </a>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl transition-shadow">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-[#cfdcff] rounded-full mr-4">
                <Settings className="w-6 h-6 text-[#1e3a2b]" />
              </div>
              <h3 className="text-xl font-bold text-[#1e3a2b]">Manage Profile</h3>
            </div>
            <p className="text-[#1e3a2b] mb-4">
              Edit your personal information and experience
            </p>
            <a
              href="/resume-writer"
              className="inline-flex items-center text-[#1e3a2b] hover:text-[#2d4a3b] font-semibold"
            >
              Edit Profile
              <ArrowRight className="w-4 h-4 ml-2" />
            </a>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200 hover:shadow-xl transition-shadow">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-[#cfdcff] rounded-full mr-4">
                <Download className="w-6 h-6 text-[#1e3a2b]" />
              </div>
              <h3 className="text-xl font-bold text-[#1e3a2b]">View Resumes</h3>
            </div>
            <p className="text-[#1e3a2b] mb-4">
              Access your saved resumes and PDFs
            </p>
            <a
              href="/resume-writer"
              className="inline-flex items-center text-[#1e3a2b] hover:text-[#2d4a3b] font-semibold"
            >
              View All
              <ArrowRight className="w-4 h-4 ml-2" />
            </a>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200">
          <h2 className="text-2xl font-bold text-[#1e3a2b] mb-6">Recent Activity</h2>
          <div className="text-center py-8">
            <FileText className="w-12 h-12 text-[#1e3a2b] mx-auto mb-4" />
            <p className="text-[#1e3a2b]">No recent activity yet</p>
            <p className="text-sm text-[#1e3a2b] mt-2">
              Create your first resume to see activity here
            </p>
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
