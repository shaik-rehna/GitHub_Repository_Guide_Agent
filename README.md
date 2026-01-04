# 📘 GitHub Repository Guide Agent

* Winter in Data Science(WiDS), IIT Bombay, 2025
* An **agentic AI-powered tool** that analyzes a public GitHub repository and generates a **clear, guided walkthrough** to help understand the repository.

---

##  Overview

Understanding an unfamiliar GitHub repository can be overwhelming.  
This project solves that problem by combining:

- GitHub repository analysis
- Intelligent prompt engineering
- Large Language Models (LLMs)
- A clean Streamlit web interface

---

## Features

- Fetches and analyzes the repository README
- Summarizes repository structure and key files
- Generates a structured, human-readable project overview
- Uses an LLM to explain purpose, features, and audience
- Interactive Streamlit UI
- Prevents duplicate analysis runs with smart state handling
- Clear input without losing previous output

---

## How It Works

1. **User Input**  
   Enter a public GitHub repository in `owner/repo` format.

2. **GitHub API Analysis**  
   - Fetches README
   - Inspects repository structure

3. **Prompt Engineering**  
   A carefully designed prompt guides the LLM to:
   - Be concise
   - Avoid raw text repetition

4. **LLM Reasoning**  
   The model generates a structured walkthrough:
   - Project purpose
   - Key features
   - Technologies used
   - Repository layout
   - Intended audience

5. **UI Rendering**  
   Results are displayed in a clean, readable format via Streamlit.

---

## Project Structure

```

github-repo-guide-agent/
├── app/
│   └── streamlit_app.py
├── src/
│   ├── fetch_repo_readme.py
│   └── llm_repo_analysis.py
├── requirements.txt
├── environment.yml
├── .env.example
├── .gitignore
└── README.md

````

---

## Setup & Installation

### Clone the repository
```bash
git clone https://github.com/shaik-rehna/GitHub_Repository_Guide_Agent.git
cd GitHub_Repository_Guide_Agent
````

---

### Create environment (recommended: Conda)

```bash
conda env create -f environment.yml
conda activate github-agent-py312
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

### Set environment variables

```bash
export GITHUB_TOKEN=your_github_token
export GEMINI_API_KEY=your_gemini_api_key
```
---

### Run the app

```bash
streamlit run app/streamlit_app.py
```

---

## Usage

1. Paste a repository name (e.g. `psf/requests`)
2. Click **Analyze Repository**
3. Read the generated guided walkthrough
4. Click **Clear** to analyze a new repository

---

## Example Use Cases

* Exploring unfamiliar open-source projects
* Educational demos for GitHub & LLM integration
* Teaching agentic AI system design

---

## Error Handling

* Invalid repo names are gracefully handled
* GitHub authentication errors are reported clearly
* API rate limits are detected
* UI prevents accidental double submissions

---

## Technologies Used

* **Python 3.12**
* **PyGithub** – GitHub API access
* **Gemini LLM** – Intelligent summarization
* **Streamlit** – Web interface
* **Prompt Engineering** – Structured LLM outputs






