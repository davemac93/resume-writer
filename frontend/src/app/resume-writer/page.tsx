"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { useAuth } from "../../contexts/AuthContext";
import { getAccessToken } from "../../lib/supabaseClient";
import LoginButton from "../../components/LoginButton";
import ProfileEditor from "../../components/ProfileEditor";
import Navbar from "../../components/Navbar";
import { Input } from "../../components/ui/input";
import { Textarea } from "../../components/ui/textarea";
import { Button } from "../../components/ui/button";
import { Download, FileText, User } from "lucide-react";

export default function ResumeWriter() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [jobOfferUrl, setJobOfferUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [resume, setResume] = useState("");
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [showProfileEditor, setShowProfileEditor] = useState(false);

  const generateResumeMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/generate-resume/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to generate resume");
      }
      return res.json();
    },
    onSuccess: (data) => {
      setResume(data.resume);
      setResumeId(data.resume_id);
    },
  });

  const generatePdfMutation = useMutation({
    mutationFn: async (resumeContent: string) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const formData = new FormData();
      formData.append("resume_content", resumeContent);

      const res = await fetch("http://localhost:8000/generate-html-pdf/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to generate PDF");
      }
      return res.blob();
    },
    onSuccess: (blob) => {
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `resume_${user?.id || 'unknown'}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    },
  });

  const generateAndStorePdfMutation = useMutation({
    mutationFn: async ({ resumeContent, resumeId }: { resumeContent: string; resumeId: string }) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const formData = new FormData();
      formData.append("resume_content", resumeContent);
      formData.append("resume_id", resumeId);

      const res = await fetch("http://localhost:8000/generate-and-store-html-pdf/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to generate and store PDF");
      }
      return res.json();
    },
    onSuccess: (data) => {
      console.log("PDF generated and stored:", data);
      // Optionally show success message or update UI
    },
  });

  const getUserResumesMutation = useMutation({
    mutationFn: async () => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/user-resumes/", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to fetch resumes");
      }
      return res.json();
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !jobOfferUrl) return;
    const formData = new FormData();
    formData.append("job_offer_url", jobOfferUrl);
    formData.append("profile_json", file);
    generateResumeMutation.mutate(formData);
  };

  const handleDownloadPdf = () => {
    if (resume) {
      generatePdfMutation.mutate(resume);
    }
  };

  const handleStorePdf = () => {
    if (resume && resumeId) {
      generateAndStorePdfMutation.mutate({ resumeContent: resume, resumeId });
    }
  };

  const handleLoadResumes = () => {
    getUserResumesMutation.mutate();
  };

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto p-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">Loading...</div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="max-w-md w-full mx-4">
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20 text-center">
            <div className="space-y-6">
              <div className="space-y-2">
                <User className="w-16 h-16 mx-auto text-gray-400" />
                <h1 className="text-2xl font-bold">Welcome to CV Builder</h1>
                <p className="text-gray-600">
                  Sign in to start generating professional resumes with AI
                </p>
              </div>
              <div className="space-y-3">
                <LoginButton user={user} onUserChange={() => {}} provider="google" />
                <a 
                  href="/simple" 
                  className="block w-full bg-gray-100 text-gray-700 px-6 py-3 rounded-full font-semibold hover:bg-gray-200 transition-colors"
                >
                  Create Resume Without Account
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f8f4f0] font-['Faro',sans-serif] flex flex-col">
      {/* Header */}
      <Navbar showAuthButton={true} />
      
      <div className="max-w-6xl mx-auto p-8 flex-grow">
        {/* Page Title */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-[#1e3a2b] mb-2">Resume Writer</h1>
          <p className="text-xl text-[#1e3a2b]">Generate professional resumes with AI and authentication</p>
        </div>

        {/* Profile Editor */}
        {showProfileEditor && (
          <div className="mb-8">
            <ProfileEditor onProfileSaved={() => setShowProfileEditor(false)} />
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="space-y-6">
            <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20">
              <div className="flex items-center mb-6">
                <div className="p-3 bg-blue-100 rounded-full mr-4">
                  <FileText className="w-6 h-6 text-blue-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Resume Generation</h2>
              </div>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">
                    Job Offer URL
                  </label>
                  <Input
                    type="url"
                    placeholder="https://example.com/job-offer"
                    value={jobOfferUrl}
                    onChange={e => setJobOfferUrl(e.target.value)}
                    required
                    className="h-12 text-base"
                  />
                  <p className="text-xs text-gray-500">
                    Paste the URL of the job posting you're applying for
                  </p>
                </div>
                
                <div className="space-y-2">
                  <label className="block text-sm font-semibold text-gray-700">
                    Profile JSON File
                  </label>
                  <Input
                    type="file"
                    accept="application/json"
                    onChange={e => setFile(e.target.files?.[0] || null)}
                    required
                    className="h-12 text-base file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                  <p className="text-xs text-gray-500">
                    Upload your candidate profile in JSON format. See example in backend folder.
                  </p>
                </div>
                
                <Button 
                  type="submit" 
                  disabled={generateResumeMutation.isPending}
                  className="w-full h-12 text-base font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg"
                >
                  {generateResumeMutation.isPending ? (
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Generating Resume...
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <FileText className="w-4 h-4 mr-2" />
                      Generate Resume
                    </div>
                  )}
                </Button>
              </form>
          </div>

            {/* Profile Management */}
            <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-xl border border-white/20">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Management</h3>
              <p className="text-sm text-gray-600 mb-4">
                Your profile will be automatically saved when you generate a resume.
              </p>
              <div className="space-y-2">
                <Button variant="outline" className="w-full shadow-sm" onClick={handleLoadResumes}>
                  View Saved Resumes
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full shadow-sm"
                  onClick={() => setShowProfileEditor(!showProfileEditor)}
                >
                  {showProfileEditor ? "Hide Profile Editor" : "Edit Profile"}
                </Button>
              </div>
            </div>
          </div>

          {/* Output */}
          <div className="space-y-6">
            {resume && (
              <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center">
                    <div className="p-3 bg-green-100 rounded-full mr-4">
                      <Download className="w-6 h-6 text-green-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">Generated Resume</h2>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={handleDownloadPdf}
                      disabled={generatePdfMutation.isPending}
                      size="sm"
                      variant="outline"
                      className="shadow-sm"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      {generatePdfMutation.isPending ? "Generating..." : "Download PDF"}
                    </Button>
                    <Button
                      onClick={handleStorePdf}
                      disabled={generateAndStorePdfMutation.isPending}
                      size="sm"
                      className="shadow-sm bg-green-600 hover:bg-green-700 text-white"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      {generateAndStorePdfMutation.isPending ? "Storing..." : "Store PDF"}
                    </Button>
                  </div>
                </div>
                <Textarea 
                  value={resume} 
                  readOnly 
                  rows={20} 
                  className="w-full font-mono text-sm bg-gray-50 border-2 border-gray-200 rounded-lg p-4 resize-none"
                />
                {resumeId && (
                  <p className="text-xs text-gray-500 mt-2">
                    Resume ID: {resumeId}
                  </p>
                )}
              </div>
            )}

            {generateResumeMutation.isError && (
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 shadow-lg">
                <h3 className="text-red-800 font-semibold text-lg mb-2">❌ Error</h3>
                <p className="text-red-600">
                  {generateResumeMutation.error?.message}
                </p>
              </div>
            )}

            {generatePdfMutation.isError && (
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 shadow-lg">
                <h3 className="text-red-800 font-semibold text-lg mb-2">❌ PDF Generation Error</h3>
                <p className="text-red-600">
                  {generatePdfMutation.error?.message}
                </p>
              </div>
            )}

            {generateAndStorePdfMutation.isError && (
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 shadow-lg">
                <h3 className="text-red-800 font-semibold text-lg mb-2">❌ PDF Storage Error</h3>
                <p className="text-red-600">
                  {generateAndStorePdfMutation.error?.message}
                </p>
              </div>
            )}

            {generateAndStorePdfMutation.isSuccess && (
              <div className="bg-green-50 border-2 border-green-200 rounded-2xl p-6 shadow-lg">
                <h3 className="text-green-800 font-semibold text-lg mb-2">✅ PDF Stored Successfully</h3>
                <p className="text-green-600">
                  Your resume has been saved to your account.
                </p>
              </div>
            )}

            {/* Saved Resumes List */}
            {getUserResumesMutation.data && (
              <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Your Saved Resumes</h3>
                <div className="space-y-3">
                  {getUserResumesMutation.data.resumes.map((resume: any) => (
                    <div key={resume.resume_id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900">Resume {resume.resume_id.slice(0, 8)}...</p>
                        <p className="text-sm text-gray-500">
                          Created: {new Date(resume.created_at).toLocaleDateString()}
                        </p>
                        {resume.job_url && (
                          <p className="text-sm text-blue-600">
                            Job: {resume.job_url}
                          </p>
                        )}
                      </div>
                      <div className="flex gap-2">
                        {resume.storage_url && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => window.open(resume.storage_url, '_blank')}
                          >
                            View PDF
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="outline"
                          className="text-red-600 hover:text-red-700"
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  ))}
                  {getUserResumesMutation.data.resumes.length === 0 && (
                    <p className="text-gray-500 text-center py-4">No saved resumes yet.</p>
                  )}
                </div>
              </div>
            )}

            {!resume && !generateResumeMutation.isError && (
              <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20 text-center">
                <div className="p-4 bg-gray-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <FileText className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">Ready to Generate</h3>
                <p className="text-gray-500">
                  Fill in the form and click "Generate Resume" to create your professional CV
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Spacer to push footer to bottom */}
      <div className="flex-grow"></div>

      {/* Footer */}
      <footer className="px-6 py-8 bg-[#1e3a2b] text-white">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-4 md:mb-0">
            <span className="text-2xl font-bold">Resume.</span>
          </div>
          <div className="flex space-x-6">
            <a href="#" className="hover:text-gray-300 transition-colors">Terms</a>
            <a href="#" className="hover:text-gray-300 transition-colors">Privacy</a>
          </div>
        </div>
        <div className="text-center mt-4 text-sm text-gray-400">
          © 2024 CVBuilder. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
