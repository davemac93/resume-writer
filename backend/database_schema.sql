-- Supabase Database Schema for CV Builder
-- Run these commands in your Supabase SQL editor

-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    profile JSONB NOT NULL,
    role_family TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create unique index on user_id
CREATE UNIQUE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);

-- Create resume_metadata table
CREATE TABLE IF NOT EXISTS resume_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    resume_id TEXT NOT NULL,
    job_url TEXT,
    status TEXT DEFAULT 'generated',
    storage_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on user_id for resume_metadata
CREATE INDEX IF NOT EXISTS idx_resume_metadata_user_id ON resume_metadata(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE resume_metadata ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for profiles table
CREATE POLICY "Users can view own profiles" ON profiles
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own profiles" ON profiles
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own profiles" ON profiles
    FOR UPDATE USING (auth.uid()::text = user_id);

-- Create RLS policies for resume_metadata table
CREATE POLICY "Users can view own resume metadata" ON resume_metadata
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own resume metadata" ON resume_metadata
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

-- Create storage bucket for resumes (run this in Supabase dashboard or via API)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('resumes', 'resumes', false);

-- Create storage policies (run these after creating the bucket)
-- CREATE POLICY "Users can upload own resumes" ON storage.objects
--     FOR INSERT WITH CHECK (bucket_id = 'resumes' AND auth.uid()::text = (storage.foldername(name))[1]);

-- CREATE POLICY "Users can view own resumes" ON storage.objects
--     FOR SELECT USING (bucket_id = 'resumes' AND auth.uid()::text = (storage.foldername(name))[1]);

-- CREATE POLICY "Users can delete own resumes" ON storage.objects
--     FOR DELETE USING (bucket_id = 'resumes' AND auth.uid()::text = (storage.foldername(name))[1]);
