# Drug Repurposing Platform - Replit Project

## Project Overview
This is a full-stack pharmaceutical research web application built with FastAPI (backend) and HTML/Tailwind/Vanilla JS (frontend). The application allows researchers to submit natural language queries about drug repurposing and receive AI-generated pharmaceutical research reports.

## Current State
- **Status**: MVP Complete and Running
- **Last Updated**: November 24, 2025
- **Version**: 1.0.0

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Authentication**: JWT tokens with bcrypt password hashing
- **Frontend**: HTML5, Jinja2 templates, Tailwind CSS, Vanilla JavaScript
- **Database**: PostgreSQL (Replit-provided)

## Project Architecture

### Backend Structure
```
app/
├── main.py                 # FastAPI app with lifespan events
├── database.py             # PostgreSQL configuration
├── auth/                   # Authentication system
│   ├── routes.py          # Login, register, logout endpoints
│   ├── hashing.py         # Bcrypt password utilities
│   └── jwt_handler.py     # JWT token creation/validation
├── users/                  # User management
│   ├── models.py          # User SQLAlchemy model
│   └── routes.py          # User profile endpoints
├── queries/                # Query handling
│   ├── models.py          # Query SQLAlchemy model
│   └── routes.py          # Query submission, dummy report generation
└── results/                # Report management
    ├── models.py          # Report SQLAlchemy model
    └── routes.py          # Report retrieval, history endpoints
```

### Frontend Structure
```
templates/
├── base.html              # Base template with Tailwind CDN
├── landing.html           # Landing page
├── signup.html            # User registration
├── login.html             # User login
├── query.html             # Query/chat interface
├── results.html           # Report display
└── history.html           # Report history

static/
├── css/styles.css         # Custom CSS (beige/coral/pink theme)
└── js/                    # Vanilla JavaScript
    ├── main.js           # Common utilities (logout)
    ├── auth.js           # Authentication forms
    ├── query.js          # Query submission
    ├── results.js        # Report loading
    └── history.js        # History page
```

## Database Schema

### Users Table
- Stores user credentials and profile
- Relationships: One-to-many with Queries and Reports

### Queries Table  
- Stores pharmaceutical research questions
- Relationships: Many-to-one with Users, One-to-one with Reports

### Reports Table
- Stores generated pharmaceutical analysis reports
- Relationships: Many-to-one with Users, One-to-one with Queries

## Key Features Implemented

1. **User Authentication**
   - Secure registration with password confirmation
   - Login with email/password
   - JWT-based session management
   - HTTPOnly cookies for security

2. **Query System**
   - Natural language question input
   - File upload support (UI ready)
   - Dummy pharmaceutical report generation
   - Instant report generation

3. **Report Management**
   - Persistent storage of all reports
   - Report history with timestamps
   - Individual report viewing
   - Markdown-formatted reports

4. **UI/UX**
   - Custom color theme: beige (#F5F1E8), coral (#F08080), pink inputs
   - Responsive design with Tailwind CSS
   - Clean, professional pharmaceutical branding
   - Loading states and error handling

## Environment Variables

Required:
- `DATABASE_URL`: PostgreSQL connection (auto-provided by Replit)
- `SESSION_SECRET`: JWT secret key (auto-provided by Replit)
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`: Database credentials

## Workflow Configuration

**Workflow Name**: Start application  
**Command**: `uvicorn app.main:app --host 0.0.0.0 --port 5000`  
**Output**: webview on port 5000  
**Status**: Running

## Recent Changes

### November 24, 2025
- Implemented complete FastAPI backend with all routes
- Created all database models with proper relationships
- Built JWT authentication system with bcrypt
- Developed all frontend templates with custom styling
- Integrated Tailwind CSS with beige/coral/pink color scheme
- Added vanilla JavaScript for all interactions
- Configured workflow and verified application runs successfully
- Improved database error handling and logging
- Moved table creation to FastAPI lifespan events for better startup management

## Future Enhancements

1. **AI Integration**
   - Real pharmaceutical data API integration
   - AI agents for intelligent data retrieval
   - Advanced analysis algorithms

2. **Features**
   - PDF export functionality
   - Data visualizations and charts
   - Report sharing
   - Advanced search and filtering

3. **Production Readiness**
   - Replace Tailwind CDN with build process
   - Add comprehensive error handling
   - Implement rate limiting
   - Add automated testing

## User Preferences

None documented yet.

## Known Issues

- LSP type warnings on Pydantic models (cosmetic only, doesn't affect runtime)
- Tailwind CDN warning (expected for development, will be replaced in production)

## Notes for Future Development

- The current report generation uses placeholder/dummy data
- File upload UI exists but backend processing not yet implemented
- Google OAuth button present but not functional
- PDF export shows placeholder alert
- Data visualization sections show placeholders
