"use client";
import { useAuth } from "../../contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Navbar from "../../components/Navbar";
import { FileText, Settings, ArrowRight } from "lucide-react";

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
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-black">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect to signin
  }

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Header */}
      <Navbar showAuthButton={false} />

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-6">
        <div className="max-w-4xl w-full text-center">
          {/* Welcome Message */}
          <div className="mb-16">
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-black text-black uppercase leading-[0.85] tracking-tight mb-8">
              WELCOME BACK, {user.user_metadata?.full_name?.toUpperCase() || user.email?.split('@')[0]?.toUpperCase() || 'USER'}!
            </h1>
            <p className="text-xl md:text-2xl text-black leading-relaxed max-w-3xl mx-auto">
              Ready to create your next professional resume? Let's get started with AI-powered generation.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <a
              href="/resume-writer"
              className="bg-black text-white px-12 py-6 text-xl font-medium hover:bg-gray-800 transition-colors rounded-lg border-0 flex items-center justify-center cursor-pointer"
              style={{
                background: 'linear-gradient(45deg, #3b82f6, #10b981, #f59e0b, #ef4444, #8b5cf6, #3b82f6)',
                backgroundSize: '400% 400%',
                animation: 'gradientShift 3s ease infinite'
              }}
            >
              <span className="relative z-10 flex items-center justify-center">
                <FileText className="w-6 h-6 mr-3" />
                Create Resume
              </span>
            </a>

            <a
              href="/resume-writer"
              className="bg-white text-black px-12 py-6 text-xl font-medium hover:bg-gray-50 transition-colors border-2 border-black rounded-lg flex items-center justify-center"
            >
              <Settings className="w-6 h-6 mr-3" />
              Manage Profile
              <ArrowRight className="w-5 h-5 ml-3" />
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
