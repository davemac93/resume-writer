"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "../../../lib/supabaseClient";
import { CheckCircle, XCircle, Loader2 } from "lucide-react";
import Navbar from "../../../components/Navbar";

export default function AuthCallback() {
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        const { data, error } = await supabase?.auth.getSession();
        
        if (error) {
          console.error("Auth callback error:", error);
          setStatus("error");
          setMessage(error.message);
          return;
        }

        if (data.session) {
          setStatus("success");
          setMessage("Successfully signed in! Redirecting to your dashboard...");
          
          // Redirect to dashboard after a short delay
          setTimeout(() => {
            router.push("/dashboard");
          }, 2000);
        } else {
          setStatus("error");
          setMessage("No session found. Please try signing in again.");
        }
      } catch (error) {
        console.error("Unexpected error:", error);
        setStatus("error");
        setMessage("An unexpected error occurred. Please try again.");
      }
    };

    handleAuthCallback();
  }, [router]);

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Navbar showAuthButton={false} />
      
      <main className="flex-grow flex items-center justify-center px-6">
        <div className="text-center max-w-2xl mx-auto">
          {status === "loading" && (
            <>
              <div className="mb-8">
                <div 
                  className="w-16 h-16 mx-auto mb-6 rounded-full animate-spin"
                  style={{
                    background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57, #ff9ff3, #54a0ff)',
                    backgroundSize: '400% 400%',
                    animation: 'gradientShift 3s ease infinite, spin 1s linear infinite'
                  }}
                />
                <h1 className="text-4xl md:text-5xl font-black text-black uppercase leading-tight tracking-tight mb-4">
                  Signing You In
                </h1>
                <p className="text-xl text-black">Please wait while we complete your authentication.</p>
              </div>
            </>
          )}

          {status === "success" && (
            <>
              <div className="mb-8">
                <CheckCircle className="w-16 h-16 text-black mx-auto mb-6" />
                <h1 className="text-4xl md:text-5xl font-black text-black uppercase leading-tight tracking-tight mb-4">
                  Welcome!
                </h1>
                <p className="text-xl text-black mb-8">{message}</p>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                  <div className="bg-black h-2 rounded-full animate-pulse" style={{ width: '100%' }}></div>
                </div>
              </div>
            </>
          )}

          {status === "error" && (
            <>
              <div className="mb-8">
                <XCircle className="w-16 h-16 text-red-600 mx-auto mb-6" />
                <h1 className="text-4xl md:text-5xl font-black text-black uppercase leading-tight tracking-tight mb-4">
                  Sign In Failed
                </h1>
                <p className="text-xl text-black mb-8">{message}</p>
              </div>
              
              <div className="space-y-4">
                <button
                  onClick={() => router.push("/signin")}
                  className="px-12 py-6 text-xl font-medium text-white bg-black hover:bg-gray-800 transition-colors rounded-lg"
                >
                  Try Again
                </button>
                <div className="mt-4">
                  <button
                    onClick={() => router.push("/")}
                    className="px-12 py-6 text-xl font-medium text-black bg-white border-2 border-black hover:bg-gray-50 transition-colors rounded-lg"
                  >
                    Go Home
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
