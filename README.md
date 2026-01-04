# 📘 GitHub Repository Guide Agent

* Winter in Data Science(WiDS), IIT Bombay, 2025
An **agentic AI-powered tool** that analyzes a public GitHub repository and generates a **clear, guided walkthrough** to help understand the repository.

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







