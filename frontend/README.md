# TalentHub - Recruiting Dashboard

A modern Next.js dashboard for recruiting teams, featuring AI-powered resume screening and tailoring capabilities.

## Features

- **Candidate Upload**: Drag-and-drop interface for uploading candidate resumes (PDF)
- **Resume Screener**: Compare candidate resumes against job descriptions
- **AI Resume Tailor**: Generate customized resumes optimized for specific job postings
- **Professional UI**: Clean, corporate design with Tailwind CSS
- **Real-time Feedback**: Toast notifications for all actions

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **UI Components**: Lucide React Icons
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

## Prerequisites

- Node.js 18+ installed
- FastAPI backend running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/
│   ├── layout.js          # Root layout with sidebar
│   ├── page.js            # Home page (Candidate Upload)
│   ├── screener/
│   │   └── page.js        # Resume Screener page
│   ├── tailor/
│   │   └── page.js        # AI Resume Tailor page
│   └── globals.css        # Global styles
├── components/
│   └── Sidebar.js         # Sidebar navigation component
├── lib/
│   └── api.js             # API utility functions
├── package.json
├── tailwind.config.js
└── next.config.js
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`:

### Endpoints Used:

1. **POST /upload** - Upload PDF resumes
2. **POST /screen_candidate** - Screen candidates against job descriptions
3. **POST /tailor_resume** - Generate tailored resume PDFs

Configuration in `lib/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000'
```

## Features Details

### 1. Candidate Upload
- Drag-and-drop file upload
- File validation (PDF only)
- Progress indicators
- Success/error notifications
- Shows chunk count after processing

### 2. Resume Screener
- Two-column layout for input and results
- Real-time screening
- Formatted results display
- Loading states

### 3. AI Resume Tailor
- Dual text areas for job description and resume
- AI-powered content optimization
- Automatic PDF download
- Feature highlights

## Styling

The dashboard uses a professional "Corporate Clean" color scheme:

- **Primary**: Blue (#3b82f6 and variations)
- **Background**: Light gray (#f8fafc)
- **Text**: Slate gray (#0f172a)
- **Accents**: White, subtle shadows

## Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### CORS Issues
Make sure the FastAPI backend has CORS middleware configured to allow `http://localhost:3000`

### API Connection Failed
1. Verify backend is running on port 8000
2. Check `lib/api.js` for correct API_BASE_URL
3. Ensure no firewall blocking localhost connections

### PDF Download Issues
- Check browser settings allow automatic downloads
- Verify the backend `/tailor_resume` endpoint is working
- Ensure OpenAI API key is configured in backend `.env`

## Development Tips

- Hot reload is enabled - changes reflect immediately
- Use browser DevTools to debug API calls
- Check backend logs for API errors
- Toast notifications show in top-right corner

## Production Deployment

For production deployment:

1. Update `API_BASE_URL` in `lib/api.js` to your production API URL
2. Build the application:
```bash
npm run build
```
3. Start the production server:
```bash
npm start
```

Or deploy to Vercel:
```bash
vercel deploy
```

## License

This project is part of the RAG and MCP Project.
