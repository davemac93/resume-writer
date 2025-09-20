# Supabase Setup Guide

This guide will help you set up Supabase for authentication, database, and storage in your CV Builder application.

## 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - Name: `cv-builder` (or your preferred name)
   - Database Password: Generate a strong password
   - Region: Choose the closest region
5. Click "Create new project"

## 2. Database Schema Setup

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor** in the left sidebar
3. Click "New Query"
4. Copy and paste the contents of `backend/database_schema.sql`
5. Click "Run" to execute the schema

This will create:
- `profiles` table for storing user profiles
- `resume_metadata` table for tracking resume generations
- Row Level Security (RLS) policies
- Proper indexes

## 3. Storage Bucket Setup

1. Navigate to **Storage** in the left sidebar
2. Click "Create a new bucket"
3. Enter bucket details:
   - Name: `resumes`
   - Public: **No** (keep private)
   - File size limit: 50 MB
   - Allowed MIME types: `application/pdf`
4. Click "Create bucket"

## 4. Authentication Setup

1. Navigate to **Authentication** → **Providers** in the left sidebar
2. Enable **Google** provider:
   - Toggle "Enable sign in with Google"
   - Add your Google OAuth credentials:
     - Client ID (from Google Cloud Console)
     - Client Secret (from Google Cloud Console)
   - Set redirect URL to: `http://localhost:3000/auth/callback` (for development)
3. Save the configuration

### Google OAuth Setup (if needed)

If you don't have Google OAuth credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:3000/auth/callback` (development)
   - `https://yourdomain.com/auth/callback` (production)
7. Copy Client ID and Client Secret to Supabase

## 5. Environment Variables

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Environment Variables

Create `backend/.env`:

```env
# OpenAI/OpenRouter Configuration
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Supabase Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database Configuration
DATABASE_URL=postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres

# Optional: Supabase Storage
SUPABASE_STORAGE_BUCKET=resumes
```

## 6. Getting Your Supabase Credentials

1. Go to **Settings** → **API** in your Supabase dashboard
2. Copy the following values:
   - **Project URL** → `SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_URL`
   - **anon public** key → `SUPABASE_ANON_KEY` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role** key → `SUPABASE_SERVICE_ROLE_KEY`
   - **Database URL** → `DATABASE_URL`

## 7. Storage Policies (Optional)

If you want to enable file storage for generated PDFs:

1. Go to **Storage** → **Policies** in your Supabase dashboard
2. Create policies for the `resumes` bucket:

```sql
-- Allow users to upload their own resumes
CREATE POLICY "Users can upload own resumes" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'resumes' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Allow users to view their own resumes
CREATE POLICY "Users can view own resumes" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'resumes' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Allow users to delete their own resumes
CREATE POLICY "Users can delete own resumes" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'resumes' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );
```

## 8. Testing the Setup

1. Start your backend server:
   ```bash
   cd backend
   python main.py
   ```

2. Start your frontend server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open `http://localhost:3000/resume-writer`
4. Try signing in with Google
5. Test uploading a profile JSON and generating a resume

## 9. Production Deployment

For production deployment:

1. Update your Google OAuth redirect URLs to include your production domain
2. Update environment variables with production URLs
3. Ensure your Supabase project is configured for production (check rate limits, etc.)

## Troubleshooting

### Common Issues

1. **Authentication not working**: Check that Google OAuth is properly configured and redirect URLs are correct
2. **Database connection errors**: Verify your `DATABASE_URL` is correct and includes the right password
3. **CORS errors**: Ensure your Supabase project allows your domain in the allowed origins
4. **Storage upload errors**: Check that the storage bucket exists and policies are set correctly

### Getting Help

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Community](https://github.com/supabase/supabase/discussions)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
