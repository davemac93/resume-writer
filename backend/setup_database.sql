-- Complete Supabase Database Setup for CV Builder
-- Run these commands in your Supabase SQL editor

-- =============================================
-- 1. CREATE TABLES
-- =============================================

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

-- =============================================
-- 2. ENABLE ROW LEVEL SECURITY (RLS)
-- =============================================

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE resume_metadata ENABLE ROW LEVEL SECURITY;

-- =============================================
-- 3. CREATE RLS POLICIES FOR TABLES
-- =============================================

-- RLS policies for profiles table
CREATE POLICY "Users can view own profiles" ON profiles
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own profiles" ON profiles
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own profiles" ON profiles
    FOR UPDATE USING (auth.uid()::text = user_id);

-- RLS policies for resume_metadata table
CREATE POLICY "Users can view own resume metadata" ON resume_metadata
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own resume metadata" ON resume_metadata
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own resume metadata" ON resume_metadata
    FOR UPDATE USING (auth.uid()::text = user_id);

CREATE POLICY "Users can delete own resume metadata" ON resume_metadata
    FOR DELETE USING (auth.uid()::text = user_id);

-- =============================================
-- 4. CREATE STORAGE BUCKET
-- =============================================

-- Create storage bucket for resumes
INSERT INTO storage.buckets (id, name, public) 
VALUES ('resumes', 'resumes', true)
ON CONFLICT (id) DO NOTHING;

-- =============================================
-- 5. CREATE STORAGE POLICIES
-- =============================================

-- Storage policies for the resumes bucket
CREATE POLICY "Users can upload own resumes" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'resumes' 
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can view own resumes" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'resumes' 
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can delete own resumes" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'resumes' 
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

-- Allow service role to manage all files (for backend operations)
CREATE POLICY "Service role can manage all resumes" ON storage.objects
    FOR ALL USING (auth.role() = 'service_role');

-- =============================================
-- 6. VERIFICATION QUERIES
-- =============================================

-- Verify tables were created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('profiles', 'resume_metadata');

-- Verify storage bucket was created
SELECT * FROM storage.buckets WHERE id = 'resumes';

-- Verify RLS is enabled
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename IN ('profiles', 'resume_metadata');

-- =============================================
-- SETUP COMPLETE! 🎉
-- =============================================
-- Your CV Builder database is now ready to use!
-- 
-- Next steps:
-- 1. Set up your environment variables (.env file)
-- 2. Start the backend server
-- 3. Test the AI Flexible CV generation
