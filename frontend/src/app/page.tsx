"use client";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Button } from "../components/ui/button";

export default function Home() {
  const router = useRouter();
  const [jobOfferUrl, setJobOfferUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [resume, setResume] = useState("");

  const mutation = useMutation({
    mutationFn: async (formData: FormData) => {
      const res = await fetch("http://localhost:8000/generate-resume/", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Failed to generate resume");
      return res.json();
    },
    onSuccess: (data) => {
      setResume(data.resume);
      // Store resume in localStorage and redirect to results page
      localStorage.setItem('generatedResume', data.resume);
      router.push('/results');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !jobOfferUrl) {
      alert("Please fill in both fields");
      return;
    }
    const formData = new FormData();
    formData.append("job_offer_url", jobOfferUrl);
    formData.append("profile_json", file);
    mutation.mutate(formData);
  };


  return (
    <div className="min-h-screen relative">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 header-blur">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="text-2xl font-bold text-white">soleil noir</div>
            <nav className="flex items-center space-x-1 glass-card rounded-full px-6 py-3">
              <a href="#" className="text-sm font-medium text-white hover:text-blue-400 transition-colors relative">
                <span className="w-2 h-2 bg-blue-500 rounded-full absolute -left-4 top-1/2 transform -translate-y-1/2"></span>
                home
              </a>
              <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                projects
              </a>
              <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                about us
              </a>
              <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                contact
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Hero Text */}
          <div className="mb-20">
            <h1 className="text-6xl md:text-8xl font-bold text-white mb-8 leading-tight">
              we craft
              <br />
              <span className="text-blue-400">imme</span>rsive
              <br />
              experiences
            </h1>
            <p className="text-xl text-white/70 max-w-2xl leading-relaxed">
              Transform your professional profile into a tailored resume that matches any job opportunity. 
              Powered by advanced AI technology.
            </p>
          </div>

          {/* Form Section */}
          <div className="max-w-4xl mx-auto">
            <div className="glass-card rounded-2xl p-8 md:p-12">
              <form onSubmit={handleSubmit} className="space-y-8">
                <div className="grid md:grid-cols-2 gap-8">
                  <div className="space-y-3">
                    <label className="text-sm font-medium text-white">Job Offer URL</label>
                    <Input
                      type="url"
                      placeholder="https://company.com/job-posting"
                      value={jobOfferUrl}
                      onChange={e => setJobOfferUrl(e.target.value)}
                      className="h-12 text-base bg-white/5 border-white/20 text-white placeholder:text-white/50 focus:border-blue-400 focus:ring-blue-400/20"
                      required
                    />
                    <p className="text-xs text-white/60">Paste the job posting URL to tailor your resume</p>
                  </div>
                  
                  <div className="space-y-3">
                    <label className="text-sm font-medium text-white">Profile JSON File</label>
                    <div className="relative">
                      <Input
                        type="file"
                        accept="application/json"
                        onChange={e => setFile(e.target.files?.[0] || null)}
                        className="h-12 text-base bg-white/5 border-white/20 text-white file:bg-white/10 file:border-white/20 file:text-white file:rounded-md file:px-4 file:py-2 file:mr-4 file:text-sm file:font-medium hover:file:bg-white/20"
                        required
                      />
                    </div>
                    <p className="text-xs text-white/60">Upload your profile data in JSON format</p>
                  </div>
                </div>

                <div className="flex justify-center">
                  <Button 
                    type="submit" 
                    disabled={mutation.isPending}
                    className="h-14 px-12 text-base font-medium bg-blue-600 hover:bg-blue-700 text-white rounded-full border-0"
                  >
                    {mutation.isPending ? (
                      <div className="flex items-center space-x-2">
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        <span>Generating Resume...</span>
                      </div>
                    ) : (
                      "Generate Resume"
                    )}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>


      {/* Error State */}
      {mutation.isError && (
        <div className="fixed bottom-6 right-6 max-w-md z-50">
          <div className="glass-card p-4 rounded-lg">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-500 rounded-full"></div>
              <span className="font-medium text-white">Error</span>
            </div>
            <p className="text-sm mt-1 text-white/80">
              {mutation.error?.message || "Failed to generate resume. Please check if the backend is running."}
            </p>
            <p className="text-xs mt-2 text-white/60">
              Make sure the backend is running on http://localhost:8000
            </p>
          </div>
        </div>
      )}

    </div>
  );
}
