"use client";
import { useState } from "react";
import { supabase, isSupabaseConfigured } from "../lib/supabaseClient";
import { Button } from "./ui/button";
import { LogIn, LogOut, User } from "lucide-react";

interface LoginButtonProps {
  user: any;
  onUserChange: (user: any) => void;
  provider?: "google" | "apple" | "github" | "facebook";
  className?: string;
}

export default function LoginButton({ user, onUserChange, provider = "google", className }: LoginButtonProps) {
  const [loading, setLoading] = useState(false);

  const onLogin = async () => {
    if (!supabase) {
      console.error('Supabase is not configured');
      return;
    }
    
    console.log(`Attempting to sign in with ${provider}...`);
    setLoading(true);
    
    try {
      const response = await supabase.auth.signInWithOAuth({
        provider: provider,
        options: {
          redirectTo: `${window.location.origin}/auth/callback`
        }
      });
      
      if (response?.error) {
        console.error(`${provider} login error:`, response.error);
        alert(`Error with ${provider}: ${response.error.message}`);
      } else if (response?.data) {
        console.log(`${provider} login initiated successfully:`, response.data);
      } else {
        console.log(`${provider} login initiated (no data returned)`);
      }
    } catch (error) {
      console.error(`${provider} login exception:`, error);
      alert(`Exception with ${provider}: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const onLogout = async () => {
    if (!supabase) {
      console.error('Supabase is not configured');
      return;
    }
    
    setLoading(true);
    try {
      const { error } = await supabase.auth.signOut();
      if (error) {
        console.error('Logout error:', error);
      } else {
        onUserChange(null);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getProviderConfig = (provider: string) => {
    const configs = {
      google: {
        name: "Google",
        bgColor: "bg-white",
        textColor: "text-gray-700",
        borderColor: "border-gray-300",
        hoverColor: "hover:bg-gray-50",
        icon: (
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
        )
      },
      apple: {
        name: "Apple",
        bgColor: "bg-black",
        textColor: "text-white",
        borderColor: "border-black",
        hoverColor: "hover:bg-gray-800",
        icon: (
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.79 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
          </svg>
        )
      },
      github: {
        name: "GitHub",
        bgColor: "bg-gray-900",
        textColor: "text-white",
        borderColor: "border-gray-900",
        hoverColor: "hover:bg-gray-800",
        icon: (
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
        )
      },
      facebook: {
        name: "Facebook",
        bgColor: "bg-blue-600",
        textColor: "text-white",
        borderColor: "border-blue-600",
        hoverColor: "hover:bg-blue-700",
        icon: (
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
        )
      }
    };
    return configs[provider as keyof typeof configs] || configs.google;
  };

  // If Supabase is not configured, show a message
  if (!isSupabaseConfigured()) {
    return (
      <div className="text-sm text-gray-500">
        Authentication not configured
      </div>
    );
  }

  if (user) {
    return (
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <User className="w-4 h-4" />
          <span className="text-sm">{user.email}</span>
        </div>
        <Button 
          onClick={onLogout} 
          disabled={loading}
          variant="outline"
          size="sm"
        >
          <LogOut className="w-4 h-4 mr-2" />
          {loading ? "Signing out..." : "Sign out"}
        </Button>
      </div>
    );
  }

  const config = getProviderConfig(provider);

  return (
    <Button 
      onClick={onLogin} 
      disabled={loading}
      className={`${config.bgColor} ${config.textColor} ${config.borderColor} ${config.hoverColor} border-2 font-semibold ${className || ""}`}
    >
      {config.icon}
      {loading ? "Signing in..." : `Continue with ${config.name}`}
    </Button>
  );
}
