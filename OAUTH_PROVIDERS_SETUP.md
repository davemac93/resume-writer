# OAuth Providers Setup Guide

This guide explains how to set up additional OAuth providers (Apple, GitHub, Facebook) in your Supabase project to enable multi-provider authentication.

## Current Status
- ✅ **Google** - Already configured and working
- ⚠️ **Apple** - Needs setup in Supabase
- ⚠️ **GitHub** - Needs setup in Supabase  
- ⚠️ **Facebook** - Needs setup in Supabase

## How to Test Current Implementation

1. **Visit the sign-in page**: `http://localhost:3000/signin`
2. **Test OAuth providers**: `http://localhost:3000/test-auth`
3. **Check browser console** for detailed logs

## Setting Up Additional Providers

### 1. Apple (Sign in with Apple)

1. **Apple Developer Account**:
   - Go to [Apple Developer Console](https://developer.apple.com/account/)
   - Create a new App ID with "Sign In with Apple" capability
   - Create a Service ID for web authentication

2. **Supabase Configuration**:
   - Go to Authentication → Providers in Supabase dashboard
   - Enable Apple provider
   - Add your Apple Service ID and Team ID
   - Set redirect URL: `https://your-project.supabase.co/auth/v1/callback`

### 2. GitHub

1. **GitHub OAuth App**:
   - Go to GitHub Settings → Developer settings → OAuth Apps
   - Create a new OAuth App
   - Set Authorization callback URL: `https://your-project.supabase.co/auth/v1/callback`

2. **Supabase Configuration**:
   - Go to Authentication → Providers in Supabase dashboard
   - Enable GitHub provider
   - Add your GitHub Client ID and Client Secret

### 3. Facebook

1. **Facebook Developer Account**:
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Create a new app
   - Add Facebook Login product
   - Set Valid OAuth Redirect URIs: `https://your-project.supabase.co/auth/v1/callback`

2. **Supabase Configuration**:
   - Go to Authentication → Providers in Supabase dashboard
   - Enable Facebook provider
   - Add your Facebook App ID and App Secret

## Testing the Implementation

### Frontend Testing
- Visit `/test-auth` to test each provider individually
- Check browser console for detailed error messages
- Each provider will show specific error messages if not configured

### Expected Behavior
- **Google**: Should redirect to Google OAuth (working)
- **Apple/GitHub/Facebook**: Will show configuration errors until set up
- **All providers**: Will show loading states and proper error handling

## Troubleshooting

### Common Issues
1. **"Provider not enabled"** - Enable the provider in Supabase dashboard
2. **"Invalid redirect URI"** - Check redirect URLs match exactly
3. **"Invalid client credentials"** - Verify Client ID and Secret are correct
4. **CORS errors** - Ensure your domain is added to allowed origins

### Debug Steps
1. Check browser console for detailed error messages
2. Verify Supabase project settings
3. Test with `/test-auth` page for individual provider testing
4. Check Supabase logs in the dashboard

## Current Implementation Features

✅ **Multi-Provider UI** - Clean grid layout with provider-specific styling
✅ **Error Handling** - Detailed error messages and loading states  
✅ **Provider Icons** - Official SVG icons for each provider
✅ **Responsive Design** - Works on mobile and desktop
✅ **Debug Tools** - Test page for individual provider testing
✅ **Fallback Options** - Create resume without account

The frontend is fully ready - you just need to configure the additional providers in Supabase!
