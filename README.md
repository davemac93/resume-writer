# CV Builder - AI-Powered Resume Generator

A full-stack web application that generates professional, tailored resumes from candidate profile JSON files and job offer links using AI technology. Features a modern React frontend and a robust Python backend with OpenAI integration.

## 🚀 Technology Stack

### Frontend
- **Framework**: Next.js 15.5.3 (React-based)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4.x
- **UI Components**: 
  - Radix UI (headless components)
  - Lucide React (icons)
  - Custom shadcn/ui components
- **State Management**: TanStack React Query 5.x
- **Build Tools**: 
  - ESLint 9.x (code linting)
  - PostCSS (CSS processing)
- **Development**: React 19.1.0 with React DOM

### Backend
- **Framework**: FastAPI (Python web framework)
- **Language**: Python 3.10+
- **AI Integration**: OpenAI SDK with OpenRouter API
- **Database**: PostgreSQL with AsyncPG
- **Authentication**: Supabase Auth with JWT tokens
- **Data Validation**: Pydantic
- **Environment Management**: python-dotenv
- **Async Support**: asyncio
- **CORS**: FastAPI CORS middleware
- **PDF Generation**: ReportLab

### Development Tools
- **Package Management**: npm (frontend), pip (backend)
- **Version Control**: Git
- **Code Quality**: ESLint, TypeScript strict mode
- **Styling**: Tailwind CSS with PostCSS
- **Build System**: Next.js build system

## 🎯 Features
- **Modern Web Interface**: Clean, responsive React frontend
- **AI-Powered Generation**: Leverages OpenRouter's AI models
- **Flexible Input**: Parses candidate profile JSON (flexible structure)
- **Smart Mapping**: Maps data to standard resume sections
- **Job-Specific Tailoring**: Prioritizes relevant experience and skills
- **Professional Formatting**: Follows industry best practices
- **Real-time Processing**: FastAPI backend with async support
- **File Upload**: Secure JSON file upload handling

## How It Works
1. **Data Extraction & Mapping:**
   - Extracts personal info, education, work experience, skills, certifications, achievements, and more from JSON.
   - Maps fields to resume sections (e.g., Education, Professional Experience).
2. **Prioritization:**
   - Highlights achievements and skills most relevant to the job offer.
3. **Structure & Formatting:**
   - Generates a clean, professional resume (chronological, functional, or hybrid).
   - Uses bullet points, clear headers, and consistent formatting.
4. **Customization:**
   - Tailors resume for the job offer and industry.
   - Emphasizes transferable skills if needed.

## 🛠️ Installation & Setup

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend)
- **npm** or **yarn** (package manager)
- **OpenRouter API Key** (for AI functionality)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

3. Create a `.env` file in the backend directory:
   ```env
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

4. Start the FastAPI server:
   ```bash
   python main.py
   ```
   The backend will be available at `http://localhost:8000`

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

## 🚀 Usage

### Web Interface (Recommended)
1. Open your browser and navigate to `http://localhost:3000`
2. Upload your candidate profile JSON file
3. Enter the job offer URL
4. Click "Generate Resume" to create your tailored CV

### Programmatic Usage (Backend Only)
```python
import json
import asyncio
from lib.agent import run_agent

# Load your profile JSON
with open('dawid_maciejewski_profile.json') as f:
    profile_json = f.read()

job_offer_url = "https://example.com/job-offer"

# Generate resume
result = asyncio.run(run_agent(profile_json, job_offer_url))
print(result)
```

## Resume Generation Guide
- Chronological, functional, or hybrid formats supported
- Recommended sections: Header, Professional Summary, Skills, Experience, Education, Certifications, Projects, Languages/Interests
- Professional style: clean fonts, consistent formatting, action verbs, quantified achievements
- Content tailored to job offer and candidate background

## 📁 Project Structure
```
cv-builder/
├── backend/                 # Python FastAPI backend
│   ├── lib/                # Core application logic
│   │   ├── agent.py        # AI resume generation agent
│   │   ├── files.py        # File handling utilities
│   │   └── tools.py        # Helper tools and functions
│   ├── main.py             # FastAPI application entry point
│   └── dawid_maciejewski_profile.json  # Example profile
├── frontend/               # Next.js React frontend
│   ├── src/
│   │   ├── app/           # Next.js app directory
│   │   ├── components/    # React components
│   │   │   └── ui/       # shadcn/ui components
│   │   ├── lib/          # Utility functions
│   │   └── styles/       # Global styles
│   ├── components.json   # shadcn/ui configuration
│   ├── package.json     # Frontend dependencies
│   └── tsconfig.json    # TypeScript configuration
├── requirements.txt      # Python dependencies
└── README.md           # This file
```

## 📋 Dependencies

### Backend Dependencies (requirements.txt)
- `openai` - OpenAI SDK for AI integration
- `fastapi` - Modern Python web framework
- `asyncpg` - PostgreSQL async driver
- `httpx` - HTTP client for Supabase auth verification
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation and serialization
- `uvicorn` - ASGI server for FastAPI
- `python-multipart` - File upload support
- `supabase` - Supabase Python client
- `reportlab` - PDF generation library

### Frontend Dependencies (package.json)
- `next` - React framework
- `react` & `react-dom` - React library
- `typescript` - TypeScript support
- `tailwindcss` - Utility-first CSS framework
- `@supabase/supabase-js` - Supabase client for auth and database
- `@radix-ui/react-slot` - Headless UI components
- `@tanstack/react-query` - Data fetching and state management
- `lucide-react` - Icon library
- `class-variance-authority` - Component variant management
- `jspdf` - PDF generation in browser

## 📄 Example Candidate Profile JSON
See `backend/dawid_maciejewski_profile.json` for a sample structure showing the expected JSON format for candidate profiles.

## 🔧 Development

### Prerequisites
- **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
- **Google OAuth**: Set up Google OAuth for authentication (optional)
- **OpenRouter API Key**: Get your API key from [openrouter.ai](https://openrouter.ai)

### Initial Setup

1. **Set up Supabase** (Required):
   - Follow the detailed guide in [`SUPABASE_SETUP.md`](./SUPABASE_SETUP.md)
   - Create database tables and configure authentication
   - Set up environment variables

2. **Install Dependencies**:
   ```bash
   # Backend dependencies
   cd backend
   pip install -r ../requirements.txt
   
   # Frontend dependencies
   cd ../frontend
   npm install
   ```

3. **Configure Environment Variables**:
   - Copy `backend/env.example` to `backend/.env`
   - Copy `frontend/env.example` to `frontend/.env.local`
   - Fill in your Supabase and OpenRouter credentials

### Running in Development Mode

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs (FastAPI auto-generated)

### Available Scripts

**Frontend** (`cd frontend`):
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

**Backend** (`cd backend`):
- `python main.py` - Start FastAPI server
- `uvicorn main:app --reload` - Start with auto-reload

## 📡 API Endpoints

### POST `/generate-resume/`
Generates a tailored resume based on profile JSON and job offer URL.

**Request**:
- `job_offer_url` (form data): URL of the job offer
- `profile_json` (file upload): JSON file containing candidate profile

**Response**:
```json
{
  "resume": "Generated resume content..."
}
```

## 🚀 Deployment

### Frontend Deployment
- **Vercel** (Recommended): Connect your GitHub repo to Vercel
- **Netlify**: Deploy the `frontend` directory
- **Docker**: Build and deploy the Next.js application

### Backend Deployment
- **Railway**: Deploy Python FastAPI application
- **Heroku**: Deploy with Procfile
- **Docker**: Containerize the FastAPI application

## 🔒 Environment Variables

Create a `.env` file in the backend directory:
```env
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

## 📝 License
MIT

## 👨‍💻 Author
Dawid Maciejewski
