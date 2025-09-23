"use client";
import { useAuth } from "../contexts/AuthContext";
import LoginButton from "./LoginButton";
import { ArrowLeft, User, LogOut, ChevronDown, LayoutDashboard } from "lucide-react";
import { useState, useEffect, useRef } from "react";

interface NavbarProps {
  showBackButton?: boolean;
  backButtonHref?: string;
  backButtonText?: string;
  showAuthButton?: boolean;
}

export default function Navbar({ 
  showBackButton = false, 
  backButtonHref = "/", 
  backButtonText = "Back to Home",
  showAuthButton = true 
}: NavbarProps) {
  const { user, signOut } = useAuth();
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsProfileDropdownOpen(false);
      }
    };

    if (isProfileDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isProfileDropdownOpen]);

  return (
    <header className="px-6 py-6 flex items-center justify-between">
      <div className="flex items-center">
        <a href="/" className="text-black text-4xl font-black hover:text-gray-700 transition-colors">
          resume.
        </a>
      </div>
      
      <nav className="hidden md:flex space-x-8">
        <a href="#pricing" className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
          • Pricing
        </a>
        {!user && (
          <a href="/signin" className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
            • Get Started
          </a>
        )}
      </nav>
      
      <div className="flex items-center space-x-4">
        {showBackButton && (
          <a 
            href={backButtonHref} 
            className="flex items-center text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {backButtonText}
          </a>
        )}
        
        {user ? (
          // Profile dropdown for logged-in users
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
              className="flex items-center space-x-2 text-black hover:text-gray-700 transition-colors"
            >
              <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              <span className="hidden md:block text-sm font-medium">
                {user.user_metadata?.full_name || user.email || 'User'}
              </span>
              <ChevronDown className="w-4 h-4" />
            </button>
            
            {isProfileDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                <div className="px-4 py-2 border-b border-gray-100">
                  <p className="text-sm font-medium text-gray-900">
                    {user.user_metadata?.full_name || 'User'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {user.email}
                  </p>
                </div>
                <a
                  href="/dashboard"
                  onClick={() => setIsProfileDropdownOpen(false)}
                  className="w-full flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                >
                  <LayoutDashboard className="w-4 h-4 mr-2" />
                  Dashboard
                </a>
                <button
                  onClick={() => {
                    signOut();
                    setIsProfileDropdownOpen(false);
                  }}
                  className="w-full flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </button>
              </div>
            )}
          </div>
        ) : (
          // Show auth button only for non-logged-in users
          showAuthButton && (
            <LoginButton user={user} onUserChange={() => {}} provider="google" />
          )
        )}
      </div>
    </header>
  );
}
