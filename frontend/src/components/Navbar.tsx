"use client";
import { useAuth } from "../contexts/AuthContext";
import LoginButton from "./LoginButton";
import { ArrowLeft } from "lucide-react";

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
  const { user } = useAuth();

  return (
    <header className="px-6 py-4 flex items-center">
      <div className="flex items-center">
        <a href="/" className="text-[#1e3a2b] text-5xl font-bold hover:text-[#2d4a3b] transition-colors">
          Resume.
        </a>
      </div>
      
      <nav className="hidden md:flex space-x-8 flex-1 justify-center">
        <a href="#pricing" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">Pricing</a>
        <a href="#how-it-works" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">How it Works</a>
        <a href="#faq" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">FAQ</a>
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
        
        {showAuthButton && (
          <LoginButton user={user} onUserChange={() => {}} provider="google" />
        )}
      </div>
    </header>
  );
}
