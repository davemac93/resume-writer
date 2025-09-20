"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { FileText, Download } from "lucide-react";

export default function SimpleResumeWriter() {
  const [jobOfferUrl, setJobOfferUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const mutation = useMutation({
    mutationFn: async (formData: FormData) => {
      const response = await fetch("http://localhost:8000/generate-resume/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response.text();
    },
    onSuccess: (data) => {
      console.log("Resume generated successfully:", data);
    },
  });

  const resume = mutation.data;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("job_offer_url", jobOfferUrl);
    formData.append("profile_json", file);
    mutation.mutate(formData);
  };

  return (
    <div className="min-h-screen bg-[#f8f4f0] font-['Faro',sans-serif] flex flex-col">
      {/* Header */}
      <header className="px-6 py-4 flex items-center">
        <div className="flex items-center">
          <span className="text-[#1e3a2b] text-5xl font-bold">Resume.</span>
        </div>
        <nav className="hidden md:flex space-x-8 flex-1 justify-center">
          <a href="#pricing" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">Pricing</a>
          <a href="#how-it-works" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">How it Works</a>
          <a href="#faq" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">FAQ</a>
        </nav>
        <a href="/" className="text-[#1e3a2b] hover:text-[#2d4a3b] transition-colors">
          ← Back to Home
        </a>
      </header>

      {/* Main Content */}
      <div className="flex-grow flex items-center justify-center px-6 py-16">
        <div className="max-w-4xl mx-auto w-full">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl font-bold text-[#1e3a2b] mb-6 max-w-4xl mx-auto leading-tight">
              Create your <span className="relative">
                professional
                <svg className="absolute -bottom-2 left-0 w-full h-3" viewBox="0 0 100 12" fill="none">
                  <path d="M2 10C15 8 35 6 50 8C65 10 85 8 98 10" stroke="#cfdcff" strokeWidth="3" strokeLinecap="round" fill="none"/>
                </svg>
              </span> resume
            </h1>
            <p className="text-xl text-[#1e3a2b] max-w-3xl mx-auto mb-8 leading-relaxed">
              Generate professional, tailored resumes with AI technology. No authentication required.
            </p>
          </div>

          {/* Form */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200 max-w-2xl mx-auto">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-[#1e3a2b]">
                  Job Offer URL
                </label>
                <input
                  type="url"
                  placeholder="https://example.com/job-offer"
                  value={jobOfferUrl}
                  onChange={e => setJobOfferUrl(e.target.value)}
                  required
                  className="w-full h-12 px-4 border-2 border-gray-300 rounded-full focus:outline-none focus:border-[#cfdcff] transition-colors"
                />
                <p className="text-xs text-gray-600">
                  Paste the URL of the job posting you're applying for
                </p>
              </div>
              
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-[#1e3a2b]">
                  Profile JSON File
                </label>
                <input
                  type="file"
                  accept="application/json"
                  onChange={e => setFile(e.target.files?.[0] || null)}
                  required
                  className="w-full h-12 px-4 border-2 border-gray-300 rounded-full focus:outline-none focus:border-[#cfdcff] transition-colors file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[#cfdcff] file:text-[#1e3a2b] hover:file:bg-[#b8ccff]"
                />
                <p className="text-xs text-gray-600">
                  Upload your candidate profile in JSON format. See example in backend folder.
                </p>
              </div>
              
              <button 
                type="submit" 
                disabled={mutation.isPending}
                className="w-full h-12 text-base font-semibold bg-[#cfdcff] text-[#1e3a2b] rounded-full hover:bg-[#b8ccff] disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg"
              >
                {mutation.isPending ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#1e3a2b] mr-2"></div>
                    Generating Resume...
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <FileText className="w-4 h-4 mr-2" />
                    Generate Resume
                  </div>
                )}
              </button>
            </form>
          </div>

          {/* Output */}
          {resume && (
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-200 max-w-4xl mx-auto mt-8">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-[#cfdcff] rounded-full mr-4 flex items-center justify-center">
                    <Download className="w-6 h-6 text-[#1e3a2b]" />
                  </div>
                  <h2 className="text-2xl font-bold text-[#1e3a2b]">Generated Resume</h2>
                </div>
                <button
                  onClick={() => {
                    const blob = new Blob([resume], { type: 'text/plain' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'generated-resume.txt';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                  }}
                  className="bg-[#1e3a2b] text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-[#0f2418] transition-colors"
                >
                  <Download className="w-4 h-4 mr-2 inline" />
                  Download
                </button>
              </div>
              <textarea 
                value={resume} 
                readOnly 
                rows={20} 
                className="w-full font-mono text-sm bg-gray-50 border-2 border-gray-200 rounded-lg p-4 resize-none"
              />
            </div>
          )}

          {/* Error */}
          {mutation.isError && (
            <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 shadow-lg max-w-2xl mx-auto mt-8">
              <h3 className="text-red-800 font-semibold text-lg mb-2">❌ Error</h3>
              <p className="text-red-600">
                {mutation.error?.message}
              </p>
              <p className="text-red-500 text-sm mt-2">
                Make sure your backend server is running on port 8000
              </p>
            </div>
          )}
        </div>
      </div>

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
          © 2024 Resume. All rights reserved.
        </div>
      </footer>
    </div>
  );
}