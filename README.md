# Research Paper Critique Assistant

An AI-powered assistant that helps analyze and critique academic research papers.

## Overview

This application helps users analyze academic research papers by:

- Extracting key sections (Goal, Hypothesis, Methods, Results, Conclusion)
- Providing a critical evaluation of the paper's methodology and arguments
- Generating insightful reviewer-style questions

## Tech Stack

- **Frontend**: Next.js 14 with Tailwind CSS
- **Backend**: FastAPI
- **AI Layer**: DSPy (Declarative Self-improving Python)
- **PDF Processing**: PyMuPDF and pdfplumber
- **Language Model**: GPT-4 (via DSPy)

## Features

- PDF file upload and processing
- Text extraction and chunking
- AI-powered analysis of research papers
- Clean, responsive UI with tabbed results

## Setup

### Prerequisites

- Node.js (v16+)
- Python (v3.9+)
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd backend
   ```

2. Create a virtual environment:

   ```
   python -m venv .venv
   ```

3. Activate the virtual environment:

   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

### Method 1: Run both services separately

1. Start the backend server:

   ```
   cd backend
   uvicorn main:app --reload
   ```

2. In a new terminal, start the frontend server:
   ```
   cd frontend
   npm run dev
   ```

### Method 2: Using concurrently (from root directory)

Install concurrently first:

```
npm install
```

Then run both services with a single command:

```
npm run dev
```

Access the application at [http://localhost:3000](http://localhost:3000)

## Usage

1. Upload your research paper (PDF format)
2. Wait for the analysis to complete
3. View the results in three tabs:
   - Summary (Goal, Hypothesis, Methods, Results, Conclusion)
   - Critique (Analysis of strengths and weaknesses)
   - Questions (Insightful reviewer-style questions)

## License

MIT
