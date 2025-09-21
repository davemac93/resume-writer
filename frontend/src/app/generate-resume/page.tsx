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
  const [pdfStorageUrl, setPdfStorageUrl] = useState<string | null>(null);

  const generateAiFlexibleCvMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/generate-ai-flexible-cv/", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to generate AI Flexible CV");
      }
      return res.json();
    },
    onSuccess: (data) => {
      setResume(data.resume);
      setResumeId(data.resume_id);
      setPdfStorageUrl(data.storage_url);
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      alert("Please select a JSON profile file");
      return;
    }

    const formData = new FormData();
    formData.append("job_offer_url", jobOfferUrl);
    formData.append("profile_json", file);

    generateAiFlexibleCvMutation.mutate(formData);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Resume Writer</h1>
          <p className="text-gray-600 mb-8">Please sign in to access the resume writer</p>
          <LoginButton user={user} onUserChange={() => {}} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <div className="p-3 bg-blue-100 rounded-full mr-4">
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
              <h1 className="text-4xl font-bold text-gray-900">AI Resume Writer</h1>
            </div>
            <p className="text-xl text-gray-600 mb-6">
              Generate professional resumes using AI with your JSON profile
            </p>
            <div className="bg-green-50 border-2 border-green-200 rounded-2xl p-6 shadow-lg">
              <h3 className="text-green-800 font-semibold text-lg mb-2">🚀 AI Flexible Method</h3>
              <p className="text-green-600 mb-3">
                <strong>Workflow:</strong> JSON profile → AI agent → markdown → flexible parser → PDF
              </p>
              <p className="text-green-600 text-sm">
                Upload your JSON profile and job offer URL, and our AI will generate a perfectly formatted resume!
              </p>
            </div>
          </div>

          {/* AI Flexible CV Form */}
          <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <div className="p-2 bg-green-100 rounded-full mr-3">
                <FileText className="w-5 h-5 text-green-600" />
              </div>
              AI Flexible CV Generator
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="jobOfferUrl" className="block text-sm font-medium text-gray-700 mb-2">
                  Job Offer URL (Optional)
                </label>
                <Input
                  id="jobOfferUrl"
                  type="url"
                  value={jobOfferUrl}
                  onChange={(e) => setJobOfferUrl(e.target.value)}
                  placeholder="https://example.com/job-posting"
                  className="w-full"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Provide a job posting URL to tailor your resume to specific requirements
                </p>
              </div>

              <div>
                <label htmlFor="profileFile" className="block text-sm font-medium text-gray-700 mb-2">
                  JSON Profile File *
                </label>
                <Input
                  id="profileFile"
                  type="file"
                  accept=".json"
                  onChange={handleFileChange}
                  className="w-full"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Upload your JSON profile file containing your professional information
                </p>
              </div>

              <Button 
                type="submit" 
                disabled={generateAiFlexibleCvMutation.isPending || !file}
                className="w-full h-12 text-base font-semibold bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
              >
                {generateAiFlexibleCvMutation.isPending ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Generating AI Flexible CV...
                  </div>
                ) : (
                  <div className="flex items-center">
                    <FileText className="w-4 h-4 mr-2" />
                    Generate AI Flexible CV
                  </div>
                )}
              </Button>
            </form>
          </div>

          {/* Output Section */}
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
                    {pdfStorageUrl ? (
                      <Button
                        onClick={() => window.open(pdfStorageUrl, '_blank')}
                        size="sm"
                        className="shadow-sm bg-green-600 hover:bg-green-700 text-white"
                      >
                        <Download className="w-4 h-4 mr-2" />
                        Download PDF
                      </Button>
                    ) : (
                      <div className="text-sm text-gray-500">PDF generating...</div>
                    )}
                  </div>
                </div>
                <Textarea 
                  value={resume} 
                  readOnly 
                  rows={20} 
                  className="w-full font-mono text-sm bg-gray-50 border-2 border-gray-200 rounded-lg p-4 resize-none"
                />
              </div>
            )}

            {/* Error Messages */}
            {generateAiFlexibleCvMutation.isError && (
              <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 shadow-lg">
                <h3 className="text-red-800 font-semibold text-lg mb-2">❌ AI Flexible CV Generation Error</h3>
                <p className="text-red-600">
                  An error occurred: {generateAiFlexibleCvMutation.error?.message}
                </p>
              </div>
            )}

            {/* Success Messages */}
            {generateAiFlexibleCvMutation.isSuccess && (
              <div className="bg-green-50 border-2 border-green-200 rounded-2xl p-6 shadow-lg">
                <h3 className="text-green-800 font-semibold text-lg mb-2">✅ AI Flexible CV Generated Successfully</h3>
                <p className="text-green-600 mb-3">
                  Your AI flexible CV has been generated using the improved workflow: JSON → AI agent → markdown → flexible parser → PDF
                </p>
                {pdfStorageUrl && (
                  <div className="mt-3 p-3 bg-green-100 rounded-lg">
                    <p className="text-green-700 text-sm font-medium mb-2">📄 PDF Ready for Download:</p>
                    <p className="text-green-600 text-xs break-all">{pdfStorageUrl}</p>
                    <Button
                      onClick={() => window.open(pdfStorageUrl, '_blank')}
                      size="sm"
                      className="mt-2 bg-green-600 hover:bg-green-700 text-white"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download PDF
                    </Button>
                  </div>
                )}
              </div>
            )}

            {/* Profile Editor */}
            {showProfileEditor && (
              <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20">
                <ProfileEditor onProfileSaved={() => setShowProfileEditor(false)} />
              </div>
            )}

            {/* Empty State */}
            {!resume && !generateAiFlexibleCvMutation.isError && (
              <div className="text-center py-12">
                <div className="p-4 bg-gray-100 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <FileText className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-600 mb-2">Ready to Generate Your Resume</h3>
                <p className="text-gray-500 mb-6">
                  Upload your JSON profile file and click "Generate AI Flexible CV" to get started
                </p>
                <Button
                  onClick={() => setShowProfileEditor(true)}
                  variant="outline"
                  className="mr-4"
                >
                  <User className="w-4 h-4 mr-2" />
                  Edit Profile
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}