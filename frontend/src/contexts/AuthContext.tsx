"use client";
import { createContext, useContext, useEffect, useState } from 'react';
import { supabase, isSupabaseConfigured, getAccessToken } from '../lib/supabaseClient';
import type { User, Session } from '@supabase/supabase-js';

interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  needsProfileUpload: boolean;
  setNeedsProfileUpload: (needs: boolean) => void;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  session: null,
  loading: true,
  needsProfileUpload: false,
  setNeedsProfileUpload: () => {},
  signOut: async () => {},
});

// Function to check if user needs to upload a profile
const checkProfileUploadNeeded = async (user: User, setNeedsProfileUpload: (needs: boolean) => void) => {
  try {
    const token = await getAccessToken();
    if (!token) {
      setNeedsProfileUpload(true);
      return;
    }

    // Check if profile already exists
    const checkResponse = await fetch("http://localhost:8000/profile", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    // If profile doesn't exist (404), user needs to upload one
    if (checkResponse.status === 404) {
      console.log("❌ No profile found - user needs to upload profile");
      setNeedsProfileUpload(true);
    } else if (checkResponse.ok) {
      console.log("✅ Profile exists - no upload needed");
      setNeedsProfileUpload(false);
    } else {
      console.warn("⚠️ Error checking profile, assuming upload needed");
      setNeedsProfileUpload(true);
    }
  } catch (error) {
    console.warn("⚠️ Error checking profile:", error);
    setNeedsProfileUpload(true);
  }
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [needsProfileUpload, setNeedsProfileUpload] = useState(false);

  useEffect(() => {
    // Check if Supabase is configured
    if (!isSupabaseConfigured()) {
      console.warn('Supabase is not configured, running without authentication');
      setLoading(false);
      return;
    }

    // Get initial session
    const getInitialSession = async () => {
      try {
        const { data: { session }, error } = await supabase!.auth.getSession();
        if (error) {
          console.error('Error getting session:', error);
        } else {
          setSession(session);
          setUser(session?.user ?? null);
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
      }
      setLoading(false);
    };

    getInitialSession();

    // Listen for auth changes
    const { data: { subscription } } = supabase!.auth.onAuthStateChange(
      async (event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        
        // Check if user needs to upload profile
        if (event === 'SIGNED_IN' && session?.user) {
          await checkProfileUploadNeeded(session.user, setNeedsProfileUpload);
        } else if (event === 'SIGNED_OUT') {
          setNeedsProfileUpload(false);
        }
        
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    if (supabase) {
      await supabase.auth.signOut();
    }
  };

  const value = {
    user,
    session,
    loading,
    needsProfileUpload,
    setNeedsProfileUpload,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
