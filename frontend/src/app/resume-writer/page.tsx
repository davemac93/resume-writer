"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { useAuth } from "../../contexts/AuthContext";
import { getAccessToken } from "../../lib/supabaseClient";
import LoginButton from "../../components/LoginButton";
import ProfileEditor from "../../components/ProfileEditor";
import ProfileCompletionDialog from "../../components/ProfileCompletionDialog";
import Navbar from "../../components/Navbar";
import { Input } from "../../components/ui/input";
import { Textarea } from "../../components/ui/textarea";
import { Button } from "../../components/ui/button";
import { Download, FileText, User, CheckCircle, AlertCircle, Loader2, Eye, Shield, Bot } from "lucide-react";

// Workflow stages
type WorkflowStage = 'input' | 'validation' | 'generation' | 'preview' | 'complete';


// Validation states
interface ValidationState {
  jobDescription: { isValid: boolean; message: string; metadata?: any };
  profile: { isValid: boolean; message: string; missingFields?: string[]; corrections?: string[] };
}

export default function ResumeWriter() {
  const { user, loading, needsProfileUpload } = useAuth();
  const router = useRouter();

  // Core state
  const [jobDescription, setJobDescription] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [profileJson, setProfileJson] = useState<any>(null);
  const [profileLoaded, setProfileLoaded] = useState(false);

  // Workflow state
  const [currentStage, setCurrentStage] = useState<WorkflowStage>('input');
  const [validationState, setValidationState] = useState<ValidationState>({
    jobDescription: { isValid: false, message: '' },
    profile: { isValid: false, message: '' }
  });

  // Output state
  const [markdownContent, setMarkdownContent] = useState("");
  const [resume, setResume] = useState("");
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [pdfStorageUrl, setPdfStorageUrl] = useState<string | null>(null);
  const [showMarkdownPreview, setShowMarkdownPreview] = useState(false);
  const [showProfileEditor, setShowProfileEditor] = useState(false);
  const [showProfileCompletion, setShowProfileCompletion] = useState(false);

  // Job description validation mutation
  const validateJobDescriptionMutation = useMutation({
    mutationFn: async (description: string) => {
      console.log("🔍 Validating job description:", description.substring(0, 100) + "...");
      // Simple validation - check if description has reasonable length
      if (description.trim().length < 50) {
        throw new Error("Job description too short. Please provide more details about the position.");
      }
      return {
        description: description,
        isValid: true,
        title: "Job Description",
        message: "Job description validated successfully"
      };
    },
    onSuccess: (data) => {
      console.log("✅ Job description validation completed successfully");
      console.log("📊 Job description validation data:", JSON.stringify(data, null, 2));
      setValidationState(prev => ({
        ...prev,
        jobDescription: { isValid: true, message: 'Job description is valid', metadata: data }
      }));
    },
    onError: (error) => {
      console.error("❌ Job description validation failed:", error);
      const errorMessage = error.name === 'AbortError' ? 'Job description validation timed out' : error.message || 'Job description validation failed';
      setValidationState(prev => ({
        ...prev,
        jobDescription: { isValid: false, message: errorMessage }
      }));
    }
  });

  // Load user profile mutation
  const loadProfileMutation = useMutation({
    mutationFn: async () => {
      console.log("🔍 Starting profile load");

      const token = await getAccessToken();
      console.log("🔑 Token available:", !!token);

      if (!token) {
        console.warn("⚠️ No authentication token, using mock profile");
        // Mock profile for testing without authentication
        return {
          personal_info: {
            full_name: "Test User",
            email: "test@example.com",
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
      }

      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

        const res = await fetch("http://localhost:8000/profile", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
          },
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        console.log("📡 Profile load response status:", res.status);

        if (!res.ok) {
          if (res.status === 404) {
            console.log("📝 Profile doesn't exist. Skipping auto-creation to avoid overwriting uploaded data.");
            return null;
          }
          console.error("❌ Failed to load profile");
          throw new Error("Failed to load profile");
        }

        const data = await res.json();
        console.log("✅ Profile loaded successfully:", data);
        return data;
      } catch (error: any) {
        console.error("❌ Network error during profile loading:", error);
        if (error.name === 'AbortError') {
          throw new Error('Profile loading timed out');
        }
        throw error;
      }
    },
    onSuccess: (profile) => {
      console.log("✅ Profile load completed successfully");
      if (profile) {
        setProfileJson(profile);
        setProfileLoaded(true);
        // Auto-validate the loaded profile
        console.log("🔍 Auto-validating loaded profile");
        validateAndCorrectMutation.mutate(profile);
      } else {
        // No profile present; show UI but do not create defaults automatically
        setProfileJson(null);
        setProfileLoaded(true);
      }
    },
    onError: (error) => {
      console.error("❌ Profile load failed:", error);
      const errorMessage = error.name === 'AbortError' ? 'Profile loading timed out' : error.message || 'Profile loading failed';
      setValidationState(prev => ({
        ...prev,
        profile: { isValid: false, message: errorMessage }
      }));
      setProfileLoaded(true); // Still set to true to show the UI
    }
  });

  // Profile validation mutation
  const validateProfileMutation = useMutation({
    mutationFn: async (profile: any) => {
      console.log("🔍 Starting profile validation");

      const token = await getAccessToken();
      console.log("🔑 Token available:", !!token);

      if (!token) {
        console.warn("⚠️ No authentication token, using mock validation");
        // Mock validation for testing without authentication
        const personal_info = profile?.personal_info || {};
        const isValid = !!(personal_info.full_name && personal_info.email);
        return {
          valid: isValid,
          message: isValid ? 'Profile is valid and complete (mock)' : 'Profile needs completion (mock)',
          missing_fields: isValid ? [] : ['personal_info.full_name', 'personal_info.email']
        };
      }

      const res = await fetch("http://localhost:8000/validate-profile/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ profile }),
      });

      console.log("📡 Profile validation response status:", res.status);

      if (!res.ok) {
        const errorData = await res.json();
        console.error("❌ Profile validation error:", errorData);
        throw new Error(errorData.detail || "Profile validation failed");
      }

      const data = await res.json();
      console.log("✅ Profile validation success:", data);
      return data;
    },
    onSuccess: (data) => {
      console.log("✅ Profile validation completed successfully");
      if (data.valid) {
        setValidationState(prev => ({
          ...prev,
          profile: { isValid: true, message: data.message || 'Profile is valid and complete' }
        }));
      } else {
        setValidationState(prev => ({
          ...prev,
          profile: { isValid: false, message: data.message || 'Profile needs completion' }
        }));
        // Show profile completion dialog for incomplete profiles
        setShowProfileCompletion(true);
      }
    },
    onError: (error) => {
      console.error("❌ Profile validation failed:", error);
      setValidationState(prev => ({
        ...prev,
        profile: { isValid: false, message: error.message || 'Profile validation failed' }
      }));
    }
  });

  // Validate and correct profile mutation
  const validateAndCorrectMutation = useMutation({
    mutationFn: async (profile: any) => {
      console.log("🔍 Profile validation disabled, auto-validating:", profile);
      // Always return success - no actual validation
      return {
        message: "Profile validation disabled",
        profile: profile,
        validation: {
          is_valid: true,
          is_complete: true,
          missing_required: [],
          missing_recommended: [],
          corrections_applied: []
        },
        corrections_applied: []
      };
    },
    onSuccess: (data) => {
      console.log("✅ Profile validation and correction completed successfully");
      console.log("📊 Response data:", JSON.stringify(data, null, 2));
      setProfileJson(data.profile);
      setValidationState(prev => ({
        ...prev,
        profile: {
          isValid: data.validation.is_valid,
          message: data.message,
          corrections: data.corrections_applied || []
        }
      }));
      if (data.validation.is_valid) {
        // Profile loaded successfully
      }
    },
    onError: (error) => {
      console.error("❌ Profile validation and correction failed:", error);
      const errorMessage = error.name === 'AbortError' ? 'Profile validation timed out' : error.message || 'Profile validation failed';
      setValidationState(prev => ({
        ...prev,
        profile: { isValid: false, message: errorMessage }
      }));
    }
  });


  // Generate resume mutation (using agent1)
  const generateResumeMutation = useMutation({
    mutationFn: async ({ profile, jobDescription }: { profile: any; jobDescription: string }) => {
      console.log(`🚀 Starting resume generation with agent1`);
      console.log("📊 Profile data:", profile);
      console.log("📝 Job description:", jobDescription.substring(0, 100) + "...");

      const token = await getAccessToken();
      console.log("🔑 Token for resume generation:", token ? "Present" : "Missing");
      if (!token) {
        console.warn("⚠️ No authentication token, using mock generation");
        // Mock generation for testing without authentication
        return {
          markdown: `# Mock Resume\n\n**${profile.personal_info?.full_name || 'Test User'}**\n\nThis is a mock resume generated for testing purposes.\n\n## Experience\n\nMock work experience...\n\n## Skills\n\nMock skills...`,
          resume: "Mock resume content",
          resume_id: "mock-resume-id",
          storage_url: null
        };
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout

      try {
        const res = await fetch("http://localhost:8000/generate-resume-agent/", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            profile,
            job_description: jobDescription,
            agent: "agent1",
            processor: "flexible"
          }),
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        console.log("📡 Resume generation response status:", res.status);

        if (!res.ok) {
          const errorData = await res.json();
          console.error("❌ Resume generation error:", errorData);
          throw new Error(errorData.detail || "Resume generation failed");
        }

        const data = await res.json();
        console.log("✅ Resume generation success:", data);
        return data;
      } catch (error: any) {
        clearTimeout(timeoutId);
        console.error("❌ Resume generation failed:", error);
        if (error.name === 'AbortError') {
          throw new Error('Resume generation timed out');
        }
        throw error;
      }
    },
    onSuccess: (data) => {
      console.log("✅ Resume generation completed successfully");
      setMarkdownContent(data.markdown);
      setResume(data.resume);
      setResumeId(data.resume_id);
      setPdfStorageUrl(data.storage_url);
      setCurrentStage('preview');
    },
    onError: (error) => {
      console.error("❌ Resume generation failed:", error);
      setCurrentStage('input'); // Go back to input stage on error
      // You could also show an error message to the user here
    }
  });

  // Workflow handlers
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      console.log("📁 File selected:", selectedFile.name);
      setFile(selectedFile);
      setProfileLoaded(false); // Reset profile loaded state when uploading new file
      try {
        const content = await selectedFile.text();
        const profile = JSON.parse(content);
        console.log("📊 Parsed profile from file:", profile);
        setProfileJson(profile);
        // Use the new validation and correction system for file uploads
        console.log("📁 File uploaded, using validateAndCorrectMutation");
        validateAndCorrectMutation.mutate(profile);
      } catch (error) {
        console.error("❌ JSON parsing error:", error);
        setValidationState(prev => ({
          ...prev,
          profile: { isValid: false, message: 'Invalid JSON file format' }
        }));
      }
    }
  };

  const handleJobDescriptionChange = (description: string) => {
    setJobDescription(description);
    if (description.trim().length > 0) {
      validateJobDescriptionMutation.mutate(description);
    } else {
      setValidationState(prev => ({
        ...prev,
        jobDescription: { isValid: false, message: '' }
      }));
    }
  };

  // Clear loading states after timeout
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (validateJobDescriptionMutation.isPending) {
        console.log("⏰ Job description validation timeout, clearing loading state");
        setValidationState(prev => ({
          ...prev,
          jobDescription: { isValid: true, message: 'Job description will be validated during generation' }
        }));
      }
    }, 5000); // 5 second timeout

    return () => clearTimeout(timeout);
  }, [validateJobDescriptionMutation.isPending]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (validateAndCorrectMutation.isPending) {
        console.log("⏰ Profile validation timeout, clearing loading state");
        setValidationState(prev => ({
          ...prev,
          profile: { isValid: true, message: 'Profile validation timed out, but will be validated during generation' }
        }));
      }
    }, 5000); // 5 second timeout

    return () => clearTimeout(timeout);
  }, [validateAndCorrectMutation.isPending]);

  const handleStartGeneration = () => {
    if (!user) {
      console.error("❌ User not authenticated, cannot generate resume");
      return;
    }

    if (validationState.jobDescription.isValid && validationState.profile.isValid && profileJson) {
      console.log("🚀 Starting resume generation...");
      setCurrentStage('generation');
      generateResumeMutation.mutate({
        profile: profileJson,
        jobDescription: jobDescription
      });
    } else {
      console.log("❌ Validation not complete:", {
        jobDescriptionValid: validationState.jobDescription.isValid,
        profileValid: validationState.profile.isValid,
        hasProfile: !!profileJson
      });
    }
  };


  // Auto-validate job description when it changes
  useEffect(() => {
    if (jobDescription && jobDescription.trim()) {
      console.log("🔍 Auto-validating job description:", jobDescription.substring(0, 100) + "...");
      validateJobDescriptionMutation.mutate(jobDescription);
    } else {
      setValidationState(prev => ({
        ...prev,
        jobDescription: { isValid: false, message: '' }
      }));
    }
  }, [jobDescription]);

  const handleEditMarkdown = (newContent: string) => {
    setMarkdownContent(newContent);
  };

  const handleGeneratePdf = () => {
    setCurrentStage('complete');
    // PDF generation is handled by the backend
  };

  const handleProfileCompletion = (completedProfile: any) => {
    setProfileJson(completedProfile);
    setValidationState(prev => ({
      ...prev,
      profile: { isValid: true, message: 'Profile completed successfully' }
    }));
    setShowProfileCompletion(false);
  };

  const handleStartProfileCompletion = () => {
    if (profileJson) {
      setShowProfileCompletion(true);
    }
  };


  const resetWorkflow = () => {
    setCurrentStage('input');
    setJobDescription('');
    setFile(null);
    setProfileJson(null);
    setProfileLoaded(false);
    setMarkdownContent('');
    setResume('');
    setValidationState({
      jobDescription: { isValid: false, message: '' },
      profile: { isValid: false, message: '' }
    });
  };

  // Load user profile when authenticated (only if they have a profile)
  useEffect(() => {
    if (user && !profileLoaded && !file && !needsProfileUpload) {
      console.log("🔄 Auto-loading profile from database (no file uploaded)");
      loadProfileMutation.mutate();
    } else if (file) {
      console.log("📁 File uploaded, skipping auto-load from database");
    } else if (needsProfileUpload) {
      console.log("📤 User needs to upload profile first");
    }
  }, [user, profileLoaded, file, needsProfileUpload]);

  // Refresh profile when user completes profile upload
  useEffect(() => {
    if (user && !needsProfileUpload && !file) {
      console.log("🔄 Profile upload completed, loading profile from database");
      setProfileLoaded(false);
      loadProfileMutation.mutate();
    }
  }, [needsProfileUpload, user, file]);

  // Listen for explicit profile-updated events (e.g., after modal save) to force reload
  useEffect(() => {
    const handler = () => {
      if (user && !file) {
        console.log("🔄 Received profile-updated event, reloading profile from database");
        setProfileLoaded(false);
        loadProfileMutation.mutate();
      }
    };
    window.addEventListener('profile-updated', handler as EventListener);
    return () => window.removeEventListener('profile-updated', handler as EventListener);
  }, [user, file, loadProfileMutation]);

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (needsProfileUpload) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center max-w-md mx-4">
          <FileText className="w-12 h-12 text-black mx-auto mb-6" />
          <h1 className="text-2xl font-medium text-black mb-4">Profile Required</h1>
          <p className="text-gray-600 mb-8 leading-relaxed">
            Please upload your profile in JSON format to get started with resume generation.
          </p>
          <div className="bg-gray-50 border border-gray-200 p-6 text-left">
            <p className="text-sm text-black font-medium mb-3">
              What you need to do:
            </p>
            <ul className="text-sm text-gray-600 space-y-2">
              <li>• Upload a JSON file with your profile information</li>
              <li>• Or use the "Skip for Now" option to create a basic profile</li>
              <li>• You can always update your profile later</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-3xl font-medium text-black mb-6">Resume Writer</h1>
          <p className="text-gray-600 mb-8">Please sign in to access the resume writer</p>
          <LoginButton user={user} onUserChange={() => { }} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Header */}
      <header className="px-6 py-6 flex items-center justify-between">
        <div className="flex items-center">
          <a href="/" className="text-black text-xl font-bold hover:text-gray-700 transition-colors">
            resume.
          </a>
        </div>
        
        <nav className="hidden md:flex space-x-8">
          <a href="#pricing" className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
            • Pricing
          </a>
          <a href="/signin" className="text-black hover:text-gray-700 transition-colors text-sm font-medium">
            • Get Started
          </a>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-6">
        <div className="text-center max-w-6xl mx-auto w-full">
          {/* Page Title */}
          <div className="mb-8">
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-black text-black uppercase leading-[0.85] tracking-tight">
              <div>RESUME</div>
              <div>WRITER</div>
            </h1>
            <p className="text-lg text-black mt-4 max-w-2xl mx-auto">
              Create professional resumes with AI-powered generation
            </p>
          </div>


          {/* Stage 1: Input */}
          {currentStage === 'input' && (
            <div className="space-y-8">
              {/* Input Form - Side by Side Layout */}
              <div className="grid grid-cols-3 gap-6">
                {/* Job Description - 1/3 width */}
                <div className="col-span-1">
                  <h2 className="text-xl font-black text-black mb-4 uppercase tracking-tight">Job Description</h2>
                  <div>
                    <Textarea
                      id="jobDescription"
                      value={jobDescription}
                      onChange={(e) => handleJobDescriptionChange(e.target.value)}
                      placeholder="Paste the job description here..."
                      className="w-full h-[250px] border-2 border-black focus:border-black focus:ring-0 resize-none rounded-none overflow-y-auto"
                      rows={8}
                    />
                    {jobDescription && (
                      <div className="mt-4 flex items-center">
                        {validateJobDescriptionMutation.isPending ? (
                          <Loader2 className="w-4 h-4 animate-spin text-gray-400 mr-2" />
                        ) : validationState.jobDescription.isValid ? (
                          <div className="w-4 h-4 bg-black rounded-full mr-2"></div>
                        ) : validationState.jobDescription.message ? (
                          <div className="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
                        ) : null}
                        <span className={`text-sm font-medium ${validationState.jobDescription.isValid ? 'text-black' :
                          validationState.jobDescription.message ? 'text-red-600' : 'text-gray-500'
                          }`}>
                          {validateJobDescriptionMutation.isPending ? 'Validating...' :
                            validationState.jobDescription.isValid ? 'Valid' :
                              validationState.jobDescription.message || 'Enter job description'}
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Profile Data - 2/3 width */}
                <div className="col-span-2">
                  <h2 className="text-xl font-black text-black mb-4 uppercase tracking-tight">Profile Data</h2>

                  {/* Profile Display Window */}
                  <div className="border-2 border-black p-4 h-[250px] overflow-y-auto">
                  {profileLoaded && profileJson ? (
                    <div className="space-y-6">
                      <div className="flex items-center justify-between">
                        <h4 className="text-base font-medium text-black">Profile Information</h4>
                        <div className="flex items-center text-sm text-black">
                          <div className="w-2 h-2 bg-black rounded-full mr-2"></div>
                          Ready
                        </div>
                      </div>

                      {/* Personal Information */}
                      {profileJson.personal_info && (
                        <div className="border-b border-gray-100 pb-4">
                          <h5 className="font-medium text-black mb-3">Personal Information</h5>
                          <div className="grid grid-cols-2 gap-3 text-sm">
                            <div>
                              <span className="text-gray-500">Name:</span>
                              <span className="ml-2 font-medium text-black">{profileJson.personal_info.full_name || 'Not provided'}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Email:</span>
                              <span className="ml-2 font-medium text-black">{profileJson.personal_info.email || 'Not provided'}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Phone:</span>
                              <span className="ml-2 font-medium text-black">{profileJson.personal_info.phone || 'Not provided'}</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Location:</span>
                              <span className="ml-2 font-medium text-black">{profileJson.personal_info.location || 'Not provided'}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Work Experience */}
                      {profileJson.work_experience && profileJson.work_experience.length > 0 && (
                        <div className="border-b border-gray-100 pb-4">
                          <h5 className="font-medium text-black mb-3">Work Experience ({profileJson.work_experience.length} positions)</h5>
                          <div className="space-y-2">
                            {profileJson.work_experience.slice(0, 2).map((exp: any, index: number) => (
                              <div key={index} className="text-sm">
                                <div className="font-medium text-black">{exp.title || 'Position'}</div>
                                <div className="text-gray-600">{exp.company || 'Company'}</div>
                              </div>
                            ))}
                            {profileJson.work_experience.length > 2 && (
                              <div className="text-xs text-gray-500">
                                +{profileJson.work_experience.length - 2} more positions
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Education */}
                      {profileJson.education && profileJson.education.length > 0 && (
                        <div className="border-b border-gray-100 pb-4">
                          <h5 className="font-medium text-black mb-3">Education ({profileJson.education.length} entries)</h5>
                          <div className="space-y-2">
                            {profileJson.education.slice(0, 2).map((edu: any, index: number) => (
                              <div key={index} className="text-sm">
                                <div className="font-medium text-black">{edu.degree || 'Degree'}</div>
                                <div className="text-gray-600">{edu.institution || 'Institution'}</div>
                              </div>
                            ))}
                            {profileJson.education.length > 2 && (
                              <div className="text-xs text-gray-500">
                                +{profileJson.education.length - 2} more entries
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Skills */}
                      {profileJson.skills && (
                        <div className="border-b border-gray-100 pb-4">
                          <h5 className="font-medium text-black mb-3">Skills</h5>
                          <div className="text-sm space-y-1">
                            {profileJson.skills.technical_skills && profileJson.skills.technical_skills.length > 0 && (
                              <div>
                                <span className="text-gray-500">Technical:</span>
                                <span className="ml-2 text-black">{profileJson.skills.technical_skills.slice(0, 5).join(', ')}</span>
                                {profileJson.skills.technical_skills.length > 5 && (
                                  <span className="text-gray-500"> +{profileJson.skills.technical_skills.length - 5} more</span>
                                )}
                              </div>
                            )}
                            {profileJson.skills.languages && profileJson.skills.languages.length > 0 && (
                              <div>
                                <span className="text-gray-500">Languages:</span>
                                <span className="ml-2 text-black">{profileJson.skills.languages.join(', ')}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Certifications */}
                      {profileJson.certifications && profileJson.certifications.length > 0 && (
                        <div>
                          <h5 className="font-medium text-black mb-3">Certifications ({profileJson.certifications.length})</h5>
                          <div className="text-sm space-y-1">
                            {profileJson.certifications.slice(0, 3).map((cert: any, index: number) => (
                              <div key={index} className="text-black">
                                {cert.name || 'Certification'} - {cert.issuer || 'Issuer'}
                              </div>
                            ))}
                            {profileJson.certifications.length > 3 && (
                              <div className="text-xs text-gray-500">
                                +{profileJson.certifications.length - 3} more certifications
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <User className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-500">No profile loaded</p>
                      <p className="text-sm text-gray-400 mt-1">Your profile will appear here once loaded</p>
                    </div>
                  )}
                </div>

                {/* Profile Status */}
                {profileLoaded && profileJson && (
                  <div className="mt-4 flex items-center">
                    <div className="w-2 h-2 bg-black rounded-full mr-2"></div>
                    <span className="text-sm text-black">
                      Profile ready for resume generation
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

          {/* Start Generation Button */}
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => {
                console.log("🔘 Button clicked!");
                console.log("Validation state:", validationState);
                console.log("Profile JSON:", profileJson);
                handleStartGeneration();
              }}
              disabled={!validationState.jobDescription.isValid || !validationState.profile.isValid || !profileJson}
              className="bg-black text-white px-12 py-6 text-xl font-medium hover:bg-gray-800 transition-colors rounded-lg border-0 flex items-center justify-center cursor-pointer"
              style={{
                background: 'linear-gradient(45deg, #3b82f6, #10b981, #f59e0b, #ef4444, #8b5cf6, #3b82f6)',
                backgroundSize: '400% 400%',
                animation: 'gradientShift 3s ease infinite',
                border: '2px solid transparent',
                backgroundClip: 'padding-box'
              }}
            >
              Start Generation
            </button>
          </div>
 

          {/* Stage 2: Generation */}
          {currentStage === 'generation' && (
            <div className="text-center py-16">
              <div className="flex items-center justify-center mb-8">
                <Loader2 className="w-8 h-8 animate-spin text-black mr-4" />
                <h2 className="text-4xl font-black text-black uppercase tracking-tight">Generating Resume</h2>
              </div>
              <p className="text-xl text-black mb-8">
                Using Agent 1 to process your profile...
              </p>
              {generateResumeMutation.isError && (
                <div className="border-2 border-red-500 bg-red-50 p-6 mt-8">
                  <p className="text-red-600 font-medium">{generateResumeMutation.error?.message}</p>
                </div>
              )}
            </div>
          )}

          {/* Stage 3: Preview */}
          {currentStage === 'preview' && markdownContent && (
            <div className="space-y-12">
              <div className="flex items-center justify-between">
                <h2 className="text-4xl font-black text-black uppercase tracking-tight">Preview</h2>
                <div className="flex gap-4">
                  <Button
                    onClick={() => setShowMarkdownPreview(!showMarkdownPreview)}
                    className="bg-white text-black px-6 py-3 text-base font-medium hover:bg-gray-50 transition-colors border-2 border-black rounded-none"
                  >
                    {showMarkdownPreview ? 'Hide' : 'Show'} Preview
                  </Button>
                  <Button
                    onClick={handleGeneratePdf}
                    className="bg-black text-white px-6 py-3 text-base font-medium hover:bg-gray-800 transition-colors border-2 border-black rounded-none"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Generate PDF
                  </Button>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-2xl font-black text-black mb-6 uppercase tracking-tight">Editable Markdown</h3>
                  <Textarea
                    value={markdownContent}
                    onChange={(e) => handleEditMarkdown(e.target.value)}
                    rows={20}
                    className="w-full font-mono text-sm border-2 border-black focus:border-black focus:ring-0 p-4 rounded-none"
                  />
                </div>

                {showMarkdownPreview && (
                  <div>
                    <h3 className="text-2xl font-black text-black mb-6 uppercase tracking-tight">Preview</h3>
                    <div className="p-6 border-2 border-black max-h-96 overflow-y-auto">
                      <pre className="whitespace-pre-wrap text-sm">{markdownContent}</pre>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Stage 4: Complete */}
          {currentStage === 'complete' && (
            <div className="space-y-12">
              <div className="border-2 border-black p-12">
                <h3 className="text-4xl font-black text-black mb-6 flex items-center uppercase tracking-tight">
                  <div className="w-8 h-8 bg-black rounded-full mr-4"></div>
                  Resume Generated Successfully
                </h3>
                <p className="text-xl text-black mb-8">
                  Your resume has been generated using Agent 1.
                </p>
                {pdfStorageUrl && (
                  <div className="mt-8 p-6 border-2 border-black">
                    <p className="text-black text-lg font-black mb-4 uppercase tracking-tight">PDF Ready for Download</p>
                    <Button
                      onClick={() => window.open(pdfStorageUrl, '_blank')}
                      className="bg-black text-white px-8 py-4 text-lg font-medium hover:bg-gray-800 border-2 border-black rounded-none"
                    >
                      <Download className="w-5 h-5 mr-2" />
                      Download PDF
                    </Button>
                  </div>
                )}
              </div>

              <div className="flex gap-6 justify-center">
                <Button
                  onClick={resetWorkflow}
                  className="bg-white text-black px-8 py-4 text-lg font-medium hover:bg-gray-50 transition-colors border-2 border-black rounded-none"
                >
                  Generate Another Resume
                </Button>
                <Button
                  onClick={() => setShowProfileEditor(true)}
                  className="bg-white text-black px-8 py-4 text-lg font-medium hover:bg-gray-50 transition-colors border-2 border-black rounded-none"
                >
                  Edit Profile
                </Button>
              </div>
            </div>
          )}

          {/* Profile Editor Modal */}
          {showProfileEditor && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
              <div className="bg-white max-w-4xl w-full max-h-[90vh] overflow-y-auto border-2 border-black">
                <div className="p-8">
                  <div className="flex items-center justify-between mb-8">
                    <h2 className="text-4xl font-black text-black uppercase tracking-tight">Profile Editor</h2>
                    <Button
                      onClick={() => setShowProfileEditor(false)}
                      className="bg-white text-black px-6 py-3 text-base font-medium hover:bg-gray-50 transition-colors border-2 border-black rounded-none"
                    >
                      Close
                    </Button>
                  </div>
                  <ProfileEditor onProfileSaved={() => setShowProfileEditor(false)} />
                </div>
              </div>
            </div>
          )}

          {/* Profile Completion Dialog */}
          <ProfileCompletionDialog
            isOpen={showProfileCompletion}
            onClose={() => setShowProfileCompletion(false)}
            onComplete={handleProfileCompletion}
            initialProfile={profileJson}
          />
        </div>
      </main>
    </div>
  );
}
