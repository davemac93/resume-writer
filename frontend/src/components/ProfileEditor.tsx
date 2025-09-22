"use client";
import { useState, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { getAccessToken } from "../lib/supabaseClient";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { User, Save, Loader2 } from "lucide-react";

interface ProfileEditorProps {
  onProfileSaved?: () => void;
}

export default function ProfileEditor({ onProfileSaved }: ProfileEditorProps) {
  const [profile, setProfile] = useState({
    personal_info: {
      full_name: "",
      email: "",
      phone: "",
      linkedin_url: "",
      location: ""
    },
    personal_summary: "",
    work_experience: [] as any[],
    education: [] as any[],
    skills: {
      technical_skills: [] as string[],
      process_project_skills: [] as string[],
      languages: [] as any[]
    },
    certifications: [] as any[],
    projects: [] as any[],
    interests: [] as string[]
  });

  const [isEditing, setIsEditing] = useState(false);

  // Fetch profile
  const fetchProfileMutation = useMutation({
    mutationFn: async () => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/profile", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
      if (!res.ok) {
        if (res.status === 404) {
          return null; // No profile found
        }
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to fetch profile");
      }
      return res.json();
    },
    onSuccess: (data) => {
      if (data && data.profile) {
        setProfile(data.profile);
      }
    },
  });

  // Save profile
  const saveProfileMutation = useMutation({
    mutationFn: async (profileData: any) => {
      const token = await getAccessToken();
      if (!token) throw new Error("Not authenticated");

      const res = await fetch("http://localhost:8000/profile", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profileData),
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to save profile");
      }
      return res.json();
    },
    onSuccess: () => {
      setIsEditing(false);
      onProfileSaved?.();
    },
  });

  useEffect(() => {
    fetchProfileMutation.mutate();
  }, []);

  const handleSave = () => {
    saveProfileMutation.mutate(profile);
  };

  const handleCancel = () => {
    fetchProfileMutation.mutate();
    setIsEditing(false);
  };

  const addExperience = () => {
    setProfile(prev => ({
      ...prev,
      work_experience: [...prev.work_experience, { 
        job_title: "", 
        company: "", 
        start_date: "", 
        end_date: "", 
        responsibilities: [], 
        achievements: [] 
      }]
    }));
  };

  const updateExperience = (index: number, field: string, value: any) => {
    setProfile(prev => ({
      ...prev,
      work_experience: prev.work_experience.map((exp, i) => 
        i === index ? { ...exp, [field]: value } : exp
      )
    }));
  };

  const removeExperience = (index: number) => {
    setProfile(prev => ({
      ...prev,
      work_experience: prev.work_experience.filter((_, i) => i !== index)
    }));
  };

  const addEducation = () => {
    setProfile(prev => ({
      ...prev,
      education: [...prev.education, { 
        degree: "", 
        institution: "", 
        start_date: "", 
        end_date: "" 
      }]
    }));
  };

  const updateEducation = (index: number, field: string, value: string) => {
    setProfile(prev => ({
      ...prev,
      education: prev.education.map((edu, i) => 
        i === index ? { ...edu, [field]: value } : edu
      )
    }));
  };

  const removeEducation = (index: number) => {
    setProfile(prev => ({
      ...prev,
      education: prev.education.filter((_, i) => i !== index)
    }));
  };

  const addTechnicalSkill = () => {
    setProfile(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        technical_skills: [...prev.skills.technical_skills, ""]
      }
    }));
  };

  const updateTechnicalSkill = (index: number, value: string) => {
    setProfile(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        technical_skills: prev.skills.technical_skills.map((skill, i) => i === index ? value : skill)
      }
    }));
  };

  const removeTechnicalSkill = (index: number) => {
    setProfile(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        technical_skills: prev.skills.technical_skills.filter((_, i) => i !== index)
      }
    }));
  };

  if (fetchProfileMutation.isPending) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-6 h-6 animate-spin mr-2" />
        Loading profile...
      </div>
    );
  }

  return (
    <div className="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <User className="w-6 h-6 mr-3 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900">Profile Editor</h2>
        </div>
        <div className="flex gap-2">
          {!isEditing ? (
            <Button onClick={() => setIsEditing(true)} variant="outline">
              Edit Profile
            </Button>
          ) : (
            <>
              <Button onClick={handleCancel} variant="outline">
                Cancel
              </Button>
              <Button 
                onClick={handleSave} 
                disabled={saveProfileMutation.isPending}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Save className="w-4 h-4 mr-2" />
                {saveProfileMutation.isPending ? "Saving..." : "Save Profile"}
              </Button>
            </>
          )}
        </div>
      </div>

      {fetchProfileMutation.isError && (
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-600">
            {fetchProfileMutation.error?.message}
          </p>
        </div>
      )}

      {saveProfileMutation.isError && (
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-600">
            {saveProfileMutation.error?.message}
          </p>
        </div>
      )}

      {saveProfileMutation.isSuccess && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4 mb-6">
          <p className="text-green-600">
            Profile saved successfully!
          </p>
        </div>
      )}

      <div className="space-y-6">
        {/* Personal Information */}
        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Personal Information</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Full Name *
              </label>
              <Input
                value={profile.personal_info.full_name}
                onChange={(e) => setProfile(prev => ({ 
                  ...prev, 
                  personal_info: { ...prev.personal_info, full_name: e.target.value }
                }))}
                disabled={!isEditing}
                placeholder="Your full name"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email *
              </label>
              <Input
                value={profile.personal_info.email}
                onChange={(e) => setProfile(prev => ({ 
                  ...prev, 
                  personal_info: { ...prev.personal_info, email: e.target.value }
                }))}
                disabled={!isEditing}
                type="email"
                placeholder="your.email@example.com"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mt-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Phone
              </label>
              <Input
                value={profile.personal_info.phone}
                onChange={(e) => setProfile(prev => ({ 
                  ...prev, 
                  personal_info: { ...prev.personal_info, phone: e.target.value }
                }))}
                disabled={!isEditing}
                placeholder="+1 (555) 123-4567"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Location
              </label>
              <Input
                value={profile.personal_info.location}
                onChange={(e) => setProfile(prev => ({ 
                  ...prev, 
                  personal_info: { ...prev.personal_info, location: e.target.value }
                }))}
                disabled={!isEditing}
                placeholder="City, State"
              />
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              LinkedIn URL
            </label>
            <Input
              value={profile.personal_info.linkedin_url}
              onChange={(e) => setProfile(prev => ({ 
                ...prev, 
                personal_info: { ...prev.personal_info, linkedin_url: e.target.value }
              }))}
              disabled={!isEditing}
              placeholder="https://www.linkedin.com/in/yourprofile"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Professional Summary
          </label>
          <Textarea
            value={profile.personal_summary}
            onChange={(e) => setProfile(prev => ({ ...prev, personal_summary: e.target.value }))}
            disabled={!isEditing}
            placeholder="Brief summary of your professional background, skills, and what you bring to the role..."
            rows={4}
          />
        </div>

        {/* Experience Section */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Work Experience</h3>
            {isEditing && (
              <Button onClick={addExperience} size="sm" variant="outline">
                Add Experience
              </Button>
            )}
          </div>
          <div className="space-y-4">
            {profile.work_experience.map((exp, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg">
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <Input
                    value={exp.job_title}
                    onChange={(e) => updateExperience(index, "job_title", e.target.value)}
                    disabled={!isEditing}
                    placeholder="Job Title"
                  />
                  <Input
                    value={exp.company}
                    onChange={(e) => updateExperience(index, "company", e.target.value)}
                    disabled={!isEditing}
                    placeholder="Company"
                  />
                </div>
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <Input
                    value={exp.start_date}
                    onChange={(e) => updateExperience(index, "start_date", e.target.value)}
                    disabled={!isEditing}
                    placeholder="Start Date (YYYY-MM)"
                  />
                  <div className="flex gap-2">
                    <Input
                      value={exp.end_date}
                      onChange={(e) => updateExperience(index, "end_date", e.target.value)}
                      disabled={!isEditing}
                      placeholder="End Date (YYYY-MM) or 'Present'"
                    />
                    {isEditing && (
                      <Button 
                        onClick={() => removeExperience(index)} 
                        size="sm" 
                        variant="outline"
                        className="text-red-600 hover:text-red-700"
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">Responsibilities</label>
                  <Textarea
                    value={Array.isArray(exp.responsibilities) ? exp.responsibilities.join('\n') : exp.responsibilities || ''}
                    onChange={(e) => updateExperience(index, "responsibilities", e.target.value.split('\n').filter(line => line.trim()))}
                    disabled={!isEditing}
                    placeholder="Enter each responsibility on a new line..."
                    rows={3}
                  />
                </div>
                <div className="space-y-2 mt-4">
                  <label className="block text-sm font-medium text-gray-700">Achievements</label>
                  <Textarea
                    value={Array.isArray(exp.achievements) ? exp.achievements.join('\n') : exp.achievements || ''}
                    onChange={(e) => updateExperience(index, "achievements", e.target.value.split('\n').filter(line => line.trim()))}
                    disabled={!isEditing}
                    placeholder="Enter each achievement on a new line..."
                    rows={3}
                  />
                </div>
              </div>
            ))}
            {profile.work_experience.length === 0 && (
              <p className="text-gray-500 text-center py-4">
                {isEditing ? "Add your work experience" : "No work experience added"}
              </p>
            )}
          </div>
        </div>

        {/* Education Section */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Education</h3>
            {isEditing && (
              <Button onClick={addEducation} size="sm" variant="outline">
                Add Education
              </Button>
            )}
          </div>
          <div className="space-y-4">
            {profile.education.map((edu, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg">
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <Input
                    value={edu.degree}
                    onChange={(e) => updateEducation(index, "degree", e.target.value)}
                    disabled={!isEditing}
                    placeholder="Degree / Field of Study"
                  />
                  <Input
                    value={edu.institution}
                    onChange={(e) => updateEducation(index, "institution", e.target.value)}
                    disabled={!isEditing}
                    placeholder="Institution Name"
                  />
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  <Input
                    value={edu.start_date}
                    onChange={(e) => updateEducation(index, "start_date", e.target.value)}
                    disabled={!isEditing}
                    placeholder="Start Date (YYYY-MM)"
                  />
                  <div className="flex gap-2">
                    <Input
                      value={edu.end_date}
                      onChange={(e) => updateEducation(index, "end_date", e.target.value)}
                      disabled={!isEditing}
                      placeholder="End Date (YYYY-MM) or 'Present'"
                    />
                    {isEditing && (
                      <Button 
                        onClick={() => removeEducation(index)} 
                        size="sm" 
                        variant="outline"
                        className="text-red-600 hover:text-red-700"
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            ))}
            {profile.education.length === 0 && (
              <p className="text-gray-500 text-center py-4">
                {isEditing ? "Add your education" : "No education added"}
              </p>
            )}
          </div>
        </div>

        {/* Skills Section */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Technical Skills</h3>
            {isEditing && (
              <Button onClick={addTechnicalSkill} size="sm" variant="outline">
                Add Technical Skill
              </Button>
            )}
          </div>
          <div className="space-y-2">
            {profile.skills.technical_skills.map((skill, index) => (
              <div key={index} className="flex gap-2">
                <Input
                  value={skill}
                  onChange={(e) => updateTechnicalSkill(index, e.target.value)}
                  disabled={!isEditing}
                  placeholder="Technical skill (e.g., Python, JavaScript, AWS)"
                />
                {isEditing && (
                  <Button 
                    onClick={() => removeTechnicalSkill(index)} 
                    size="sm" 
                    variant="outline"
                    className="text-red-600 hover:text-red-700"
                  >
                    Remove
                  </Button>
                )}
              </div>
            ))}
            {profile.skills.technical_skills.length === 0 && (
              <p className="text-gray-500 text-center py-4">
                {isEditing ? "Add your technical skills" : "No technical skills added"}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
