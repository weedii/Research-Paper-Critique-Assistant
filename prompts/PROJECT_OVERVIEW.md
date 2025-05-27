# 🧠 Research Paper Critique Assistant

You are my assistant throughout a full-stack AI project.

I'm building a web application called **"Research Paper Critique Assistant"**.  
The purpose is to help users analyze academic research papers by extracting key sections, summarizing the paper, critiquing its methodology or logic, and generating smart reviewer-like questions.

This tool solves a real-world problem by helping students, researchers, and reviewers save time understanding large, complex documents.

---

## 🎯 Project Goal

Create an AI-powered assistant that can:

- Read and process long research papers (PDFs up to 300 pages).
- Extract parts like Abstract, Methods, Results, and Conclusion.
- Summarize the overall paper clearly.
- Identify flaws or weak arguments.
- Suggest reviewer-style questions for critique and evaluation.

---

## 🧱 Tech Stack Overview

**Frontend:** `Next.js 14`

- Handles file upload and displays the critique output.

**Backend:** `FastAPI`

- Handles file parsing, text chunking, and communication with AI.

**AI Layer:** `DSPy` (Declarative Self-improving Python)

- Used to define structured LLM pipelines (Signatures) for summarization, critique, and question generation.

**PDF Parsing:** `PyMuPDF` or `pdfplumber`

**Language Model:** `GPT-4 via DSPy` (can be replaced later)

---

## 🔁 Architecture Flow

1. User uploads PDF via the frontend.
2. FastAPI receives and extracts the text.
3. Text is split into sections or chunks.
4. Each chunk is passed into DSPy modules:
   - `ExtractResearchParts`
   - `CritiqueResearchPaper`
   - `SuggestReviewerQuestions`
5. Results are aggregated and returned to the frontend for display.

---

## 🧠 DSPy Module Plan (Signatures)

```python
class ExtractResearchParts(dspy.Signature):
    input = dspy.InputField(desc="Text from a research paper")
    goal = dspy.OutputField()
    hypothesis = dspy.OutputField()
    methods = dspy.OutputField()
    results = dspy.OutputField()
    conclusion = dspy.OutputField()

class CritiqueResearchPaper(dspy.Signature):
    input = dspy.InputField()
    critique = dspy.OutputField(desc="Flaws, gaps, or reasoning problems")

class SuggestReviewerQuestions(dspy.Signature):
    input = dspy.InputField()
    questions = dspy.OutputField(desc="Smart, critical follow-up questions")
```

---

## ⚠️ Token Limit Note

Research papers can be long (over 100K tokens). To handle this:

- The document is split into smaller chunks.
- Each chunk is processed individually through DSPy.
- Final output is aggregated into a complete summary and critique.
- Optional: Use retrieval-based methods to target only specific sections if needed.

---

## 🛠 Development Plan Summary

1. Set up Next.js frontend with a file upload form.
2. Set up FastAPI backend with endpoints to:
   - Accept PDF
   - Extract and split content
   - Run DSPy modules
3. Implement DSPy module logic and connect with backend.
4. Display extracted summary, critique, and questions on frontend.

---

## 🧪 Example Output Format

```json
{
  "goal": "...",
  "hypothesis": "...",
  "methods": "...",
  "results": "...",
  "conclusion": "...",
  "critique": "...",
  "reviewer_questions": ["...", "...", "..."]
}
```

---

## 🧠📣 INSTRUCTIONS

Please follow this roadmap and start implementing the full-stack system step by step:

1. Start with setting up a FastAPI backend with a `/upload` endpoint to accept PDF files.
2. Parse the uploaded PDF using `PyMuPDF` or `pdfplumber`.
3. Split the extracted text into chunks.
4. Set up DSPy and implement the three defined Signatures.
5. Process each chunk using DSPy and aggregate the results.
6. Create a simple Next.js frontend that allows PDF upload and displays the results.
7. Connect the frontend to the backend using API calls.
8. Add basic error handling and loading states.
9. Improve UI with Tailwind or a UI library like ShadCN.
10. Start your implementation from the existing project which is separated into 2 main folders `/backend` and `/frontend`

Proceed with building the project now.

---

## 🏗️ Backend Architecture

The backend follows a structured and modular architecture to ensure separation of concerns:

### Folder Structure

```
backend/
├── main.py             # Entry point of the application
└── src/
    ├── controllers/    # Request/response handling
    ├── services/       # Business logic implementation
    ├── repositories/   # Database interactions
    ├── crud/           # CRUD operations
    ├── models/         # Data models
    ├── schemas/        # Pydantic schemas for validation
    ├── constants/      # Application constants
    └── utils/          # Helper functions and utilities
```

### Component Responsibilities

1. **Controllers**

   - Handle HTTP requests and responses only
   - Route requests to appropriate services
   - No business logic implementation
   - Input validation and response formatting

2. **Services**

   - Contain core business logic
   - Orchestrate data flow between controllers and repositories
   - Implement the main functionality of the application (paper analysis, critique generation)
   - Processing of DSPy operations and AI interactions

3. **CRUD**

   - Structured as classes/objects
   - Provide standardized Create, Read, Update, Delete operations
   - Abstract database operations with a consistent interface

4. **Repositories**
   - Handle direct database interactions only
   - Execute queries and data retrieval
   - No business logic
   - Return raw data to services for processing

This architecture ensures clean separation of concerns, making the codebase maintainable, testable, and scalable.
