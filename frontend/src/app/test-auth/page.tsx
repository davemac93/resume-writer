"use client";
import { useState } from "react";
import { supabase } from "../../lib/supabaseClient";

export default function TestAuth() {
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const testProvider = async (provider: string) => {
    setLoading(true);
    setResult(`Testing ${provider}...`);
    
    try {
      const response = await supabase?.auth.signInWithOAuth({
        provider: provider as any,
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      });
      
      if (response?.error) {
        setResult(`Error with ${provider}: ${response.error.message}`);
      } else if (response?.data) {
        setResult(`Success! Redirecting to ${provider}...`);
      } else {
        setResult(`OAuth initiated for ${provider} (no data returned)`);
      }
    } catch (err) {
      setResult(`Exception with ${provider}: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">OAuth Provider Test</h1>
        
        <div className="space-y-4">
          <button
            onClick={() => testProvider("google")}
            disabled={loading}
            className="w-full p-4 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Test Google OAuth
          </button>
          
          <button
            onClick={() => testProvider("apple")}
            disabled={loading}
            className="w-full p-4 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50"
          >
            Test Apple OAuth
          </button>
          
          <button
            onClick={() => testProvider("github")}
            disabled={loading}
            className="w-full p-4 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:opacity-50"
          >
            Test GitHub OAuth
          </button>
          
          <button
            onClick={() => testProvider("facebook")}
            disabled={loading}
            className="w-full p-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Test Facebook OAuth
          </button>
        </div>
        
        {result && (
          <div className="mt-8 p-4 bg-white rounded-lg border">
            <h3 className="font-semibold mb-2">Result:</h3>
            <p className="text-sm text-gray-600">{result}</p>
          </div>
        )}
        
        <div className="mt-8 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
          <h3 className="font-semibold text-yellow-800 mb-2">Note:</h3>
          <p className="text-sm text-yellow-700">
            Only Google OAuth is currently configured in Supabase. 
            Other providers will show errors until they are set up in your Supabase dashboard.
          </p>
        </div>
      </div>
    </div>
  );
}
