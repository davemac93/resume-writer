"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "../../../lib/supabaseClient";
import { CheckCircle, XCircle, Loader2 } from "lucide-react";

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
    <div className="min-h-screen bg-[#f8f4f0] font-['Faro',sans-serif] flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200 max-w-md w-full mx-4">
        <div className="text-center">
          {status === "loading" && (
            <>
              <Loader2 className="w-16 h-16 text-[#1e3a2b] mx-auto mb-4 animate-spin" />
              <h1 className="text-2xl font-bold text-[#1e3a2b] mb-2">Signing you in...</h1>
              <p className="text-[#1e3a2b]">Please wait while we complete your authentication.</p>
            </>
          )}

          {status === "success" && (
            <>
              <CheckCircle className="w-16 h-16 text-[#1e3a2b] mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-[#1e3a2b] mb-2">Welcome!</h1>
              <p className="text-[#1e3a2b] mb-4">{message}</p>
              <div className="animate-pulse">
                <div className="h-2 bg-[#cfdcff] rounded-full">
                  <div className="h-2 bg-[#1e3a2b] rounded-full animate-pulse"></div>
                </div>
              </div>
            </>
          )}

          {status === "error" && (
            <>
              <XCircle className="w-16 h-16 text-red-600 mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-[#1e3a2b] mb-2">Sign In Failed</h1>
              <p className="text-[#1e3a2b] mb-6">{message}</p>
              <div className="space-y-3">
                <button
                  onClick={() => router.push("/signin")}
                  className="w-full bg-[#1e3a2b] text-white px-6 py-3 rounded-full font-semibold hover:bg-[#2d4a3b] transition-colors"
                >
                  Try Again
                </button>
                <button
                  onClick={() => router.push("/")}
                  className="w-full bg-[#cfdcff] text-[#1e3a2b] px-6 py-3 rounded-full font-semibold hover:bg-[#b8ccff] transition-colors"
                >
                  Go Home
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
