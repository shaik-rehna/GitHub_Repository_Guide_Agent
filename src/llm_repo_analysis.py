import os
import sys
from typing import List

from github import Github
from github.GithubException import (
    GithubException,
    UnknownObjectException,
    BadCredentialsException,
    RateLimitExceededException,
)

from google import genai
from fetch_repo_readme import fetch_repo_readme

# ------------------------- Fetching paths of all files in the repo --------------------------
# def fetch_repo_tree(repo) -> List[str]:
#     """
#     Recursively fetch repository file/folder structure
#     Returns a list of paths
#     """
#     contents = repo.get_contents("")
#     paths = []

#     while contents:
#         item = contents.pop(0)
#         paths.append(item.path)
#         if item.type == "dir":
#             contents.extend(repo.get_contents(item.path))

#     return paths

# ----------------- Depth-limited version --------------------
def fetch_repo_tree(repo, max_depth=3) -> List[str]:
    contents = [(item, 0) for item in repo.get_contents("")]
    paths = []

    while contents:
        item, depth = contents.pop(0)
        paths.append(item.path)

        if item.type == "dir" and depth < max_depth:
            for sub in repo.get_contents(item.path):
                contents.append((sub, depth + 1))

    return paths


def summarize_repo_structure(paths: List[str]) -> str:
    """
    Convert raw file paths into a compact, LLM-friendly description.
    """
    summary = {
        "source_code": [],
        "code_files":[],
        "config": [],
        "docs": [],
        "tests": [],
        "other": []
    }

    for path in paths:
        if path.lower().startswith(("src/", "app/", "code/")):
            summary["source_code"].append(path)
        elif path.endswith((".ipynb", ".py")):
            summary["code_files"].append(path)
        elif path.endswith((".txt", ".yml", ".yaml", ".json", ".toml", ".env.example")):
            summary["config"].append(path)
        elif path.lower().startswith(("readme", "docs/")) or path.endswith((".pdf",".pptx")):
            summary["docs"].append(path)
        elif "tests" in path.lower() or "test" in path.lower():
            summary["tests"].append(path)
        else:
            summary["other"].append(path)

    def format_section(title, items):
        if not items:
            return f"- {title}: None"
        return f"- {title}:\n" + "\n".join(f"  • {i}" for i in items[:15])

    return "\n".join([
        format_section("Source Code", summary["source_code"]),
        format_section("Code Files", summary["code_files"]),
        format_section("Configuration Files", summary["config"]),
        format_section("Documentation", summary["docs"]),
        format_section("Tests", summary["tests"]),
        format_section("Other Files", summary["other"]),
    ])



# ---------------------------- Advanced Prompt Engineering (Agent Brain) -----------------------
def build_agent_prompt(repo_name: str, readme: str, structure_summary: str) -> str:
    return f"""

You are given about a GitHub repository:

1. The README file of the repository
2. The actual repository file/folder structure

Your task is to synthesize these into an accurate, insightful guided tour.

Repository: {repo_name}

----------------
README CONTENT
----------------
{readme}

----------------
REPOSITORY STRUCTURE
----------------
{structure_summary}

----------------
OUTPUT REQUIREMENTS
----------------
Produce a structured analysis with the following sections:

1. Repository 
    - Title 
    - Link

2. What is the repository about?
   
3. Core Components
   - Identify major modules or folders
   - Explain their responsibilities

4. How the Code is Organized
   - Entry points
   - Separation of concerns

5. How to Start
   - Suggested reading order
   - Where to begin exploring the code

Rules:
- Do NOT restate the README verbatim
- Base claims on actual file structure
- Be precise, not verbose
"""


# ---------------------- LLM Interaction -------------------------
def run_agent(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("" 
        "GEMINI_API_KEY not found"
        "Export it or load it via .env file")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    return response.text

# -------------------------------- Analysis of repo by llm ---------------------------


def analyze_repository(repo_full_name: str) -> str:
    try:
     
        repo, readme = fetch_repo_readme(repo_full_name)
        paths = fetch_repo_tree(repo)
        structure_summary = summarize_repo_structure(paths)

        prompt = build_agent_prompt(
            repo_full_name,
            readme,
            structure_summary
        )

        analysis = run_agent(prompt)

        return analysis

    except BadCredentialsException:
        print("Invalid GitHub credentials.", file=sys.stderr)

    except RateLimitExceededException:
        print("GitHub API rate limit exceeded.", file=sys.stderr)

    except UnknownObjectException:
        print("Repository or README not found.", file=sys.stderr)

    except GithubException as e:
        print(f"GitHub API error: {e}", file=sys.stderr)

    except RuntimeError as e:
        print(f"Configuration error: {e}", file=sys.stderr)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python agent.py <owner/repo>\n"
            "Example: python agent.py psf/requests",
            file=sys.stderr,
        )
        sys.exit(1)

    repo_full_name = sys.argv[1]
    analysis = analyze_repository(repo_full_name)
    print("\n" + "=" * 80)
    print(f"Guided Repository Analysis: {repo_full_name}")
    print("=" * 80 + "\n")
    print(analysis)
