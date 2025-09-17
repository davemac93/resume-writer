"use client";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Button } from "../components/ui/button";

export default function ResumeWriter() {
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
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !jobOfferUrl) return;
    const formData = new FormData();
    formData.append("job_offer_url", jobOfferUrl);
    formData.append("profile_json", file);
    mutation.mutate(formData);
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-4">Resume Writer</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="url"
          placeholder="Job Offer URL"
          value={jobOfferUrl}
          onChange={e => setJobOfferUrl(e.target.value)}
          required
        />
        <Input
          type="file"
          accept="application/json"
          onChange={e => setFile(e.target.files?.[0] || null)}
          required
        />
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Generating..." : "Generate Resume"}
        </Button>
      </form>
      {resume && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-2">Generated Resume</h2>
          <Textarea value={resume} readOnly rows={20} className="w-full" />
        </div>
      )}
      {mutation.isError && (
        <div className="text-red-500 mt-4">Error: {mutation.error?.message}</div>
      )}
    </div>
  );
}
