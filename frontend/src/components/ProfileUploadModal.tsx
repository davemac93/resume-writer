"use client";

import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { getAccessToken } from '../lib/supabaseClient';

interface ProfileUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onProfileUploaded: (profile: any) => void;
}

export default function ProfileUploadModal({ isOpen, onClose, onProfileUploaded }: ProfileUploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setSuccess(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a JSON file');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const content = await file.text();
      const profile = JSON.parse(content);
      
      // Validate that it's a proper profile structure
      if (!profile.personal_info && !profile.name) {
        throw new Error('Invalid profile format. Please ensure your JSON file contains profile information.');
      }

      // Save profile to backend
      const token = await getAccessToken();
      if (token) {
        console.log("💾 Saving profile to backend...");
        
        const response = await fetch("http://localhost:8000/upsert-profile/", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ profile }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to save profile to database');
        }

        const result = await response.json();
        console.log("✅ Profile saved to database:", result);
      }

      setSuccess(true);
      setTimeout(() => {
        onProfileUploaded(profile);
        try {
          window.dispatchEvent(new Event('profile-updated'));
        } catch {}
        onClose();
        setFile(null);
        setSuccess(false);
      }, 1500);

    } catch (err) {
      console.error("❌ Profile upload error:", err);
      setError(err instanceof Error ? err.message : 'Failed to upload profile');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSkip = async () => {
    // Create a minimal profile for users who want to skip
    const minimalProfile = {
      personal_info: {
        full_name: "",
        email: "",
        phone: "",
        linkedin_url: "",
        location: ""
      },
      personal_summary: "",
      work_experience: [],
      education: [],
      skills: {
        technical_skills: [],
        process_project_skills: [],
        languages: []
      },
      certifications: [],
      projects: [],
      interests: []
    };

    try {
      // Save minimal profile to backend
      const token = await getAccessToken();
      if (token) {
        console.log("💾 Saving minimal profile to backend...");
        
        const response = await fetch("http://localhost:8000/upsert-profile/", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ profile: minimalProfile }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("❌ Failed to save minimal profile:", errorData);
        } else {
          console.log("✅ Minimal profile saved to database");
        }
      }
    } catch (err) {
      console.error("❌ Error saving minimal profile:", err);
    }
    
    onProfileUploaded(minimalProfile);
    try {
      window.dispatchEvent(new Event('profile-updated'));
    } catch {}
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex items-center mb-4">
          <FileText className="w-6 h-6 text-blue-600 mr-2" />
          <h2 className="text-xl font-semibold">Upload Your Profile</h2>
        </div>
        
        <p className="text-gray-600 mb-6">
          To get started, please upload your profile in JSON format. This will help us generate a personalized resume for you.
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select JSON Profile File
            </label>
            <Input
              type="file"
              accept=".json"
              onChange={handleFileChange}
              className="w-full"
            />
            {file && (
              <div className="mt-2 flex items-center text-sm text-green-600">
                <CheckCircle className="w-4 h-4 mr-1" />
                {file.name}
              </div>
            )}
          </div>

          {error && (
            <div className="flex items-center text-red-600 text-sm">
              <AlertCircle className="w-4 h-4 mr-1" />
              {error}
            </div>
          )}

          {success && (
            <div className="flex items-center text-green-600 text-sm">
              <CheckCircle className="w-4 h-4 mr-1" />
              Profile uploaded successfully!
            </div>
          )}

          <div className="flex space-x-3 pt-4">
            <Button
              onClick={handleUpload}
              disabled={!file || isUploading}
              className="flex-1"
            >
              {isUploading ? (
                <>
                  <Upload className="w-4 h-4 mr-2 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Upload Profile
                </>
              )}
            </Button>
            
            <Button
              variant="outline"
              onClick={handleSkip}
              disabled={isUploading}
            >
              Skip for Now
            </Button>
          </div>

          <div className="text-xs text-gray-500 mt-4">
            <p><strong>Need help?</strong></p>
            <p>• Download our sample profile template</p>
            <p>• Ensure your JSON file follows the correct format</p>
            <p>• You can always upload a profile later</p>
          </div>
        </div>
      </div>
    </div>
  );
}
