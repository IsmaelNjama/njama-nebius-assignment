# GitHub Repository Summarizer

A FastAPI service that analyzes GitHub repositories and generates AI-powered summaries of their structure and purpose.

## Prerequisites

- Python 3.8+
- Git
- Nebius API key
- GitHub token (optional, for higher rate limits)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/IsmaelNjama/njama-nebius-assignment.git
   cd njama-nebius-assignment

   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate

   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:

```bash
 NEBIUS_API_KEY=your-nebius-api-key
 GITHUB_TOKEN=your-github-token # Optional
```

## Running the Server

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

```

The server will be available at `http://localhost:8000`

## Usage

Send a POST request to the `/summarize` endpoint:

```bash
curl -X POST http://localhost:8000/summarize \
 -H "Content-Type: application/json" \
 -d '{"github_url": "https://github.com/psf/requests"}'

```

### Response Format

```bash
json
{
"summary": "A simple, yet elegant, HTTP library that allows users to send HTTP/1.1 requests extremely easily.",
"technologies": ["Python", "HTTP/1.1", "GitHub"],
"structure": "The project is organized into main directories such as 'docs', 'ext', 'src', and 'tests', with a README file providing an introduction and usage guide."
}
```

## Model Selection

I chose **Meta-Llama-3.1-8B-Instruct-fast** because it provides a good balance between speed and quality for summarization tasks, and it's cost-effective for this use case while being readily available through Nebius.

## Approach to Repository Analysis

The service gathers the following information from each repository:

- **Basic metadata**: Name, description, and primary language
- **README content**: First 3000 characters to understand the project's purpose
- **Repository structure**: Top-level directory tree (non-recursive) to identify organization
- **Languages used**: Programming language breakdown
- **Package files**: Dependencies from files like `requirements.txt`, `package.json`, `Cargo.toml`, etc.

**What's skipped**: Full file contents, deep recursive trees, and commit history. This keeps the context focused and prevents overwhelming the LLM while still providing enough information for meaningful summaries.

## Project Structure

```bash
.
├── app/
│ ├── main.py # FastAPI application entry point
│ ├── api/ # API route handlers
│ ├── services/ # Business logic (GitHub, LLM)
│ ├── schemas/ # Pydantic models
│ └── utils/ # Helper functions
├── requirements.txt # Python dependencies
├── .env # Environment variables
└── README.md

```
