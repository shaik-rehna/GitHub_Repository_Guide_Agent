import os
import sys
from github import Github
from github.GithubException import(
    GithubException,
    UnknownObjectException,
    BadCredentialsException,
    RateLimitExceededException,
)
from github.Repository import Repository

def fetch_repo_readme(repo_full_name: str) -> tuple[Repository, str]:
    """
    Fetch and print README.md from a Github repository
    Args:
        repo_full_name (str): Repository in 'owner/repo' format
    """

    # in terminal: export GITHUB_TOKEN=$(gh auth token) 
    #                   or
    # add GITHUB_TOKEN=actual_token inside .env file
    # from dotenv import load_dotenv    
    # load_dotenv()  (loads .env into environment)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN not found"
            "Export it or load it via a .env file"
        )
    try:
        github = Github(token)
        repo = github.get_repo(repo_full_name)
        readme = repo.get_readme()
        readme_content = readme.decoded_content.decode("utf-8")
        return repo, readme_content
      

    except BadCredentialsException:
        print(" Authentication failed. Check your GITHUB_TOKEN", file=sys.stderr)
    except RateLimitExceededException:
        print("Github API rate limit exceeded")
    except UnknownObjectException:
        print(
            f"Repository or README not found: {repo_full_name}",
            file=sys.stderr,
        )    
    except GithubException as e:
        print(f"Github API error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)      

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python fetch_readme.py <owner/repo>\n"
            "Example: python fetch_readme.py psf/requests",
            file=sys.stderr,
        )
        sys.exit(1)
    repo_full_name = sys.argv[1]
    repo, readme_content = fetch_repo_readme(repo_full_name)
    print("\n" + "=" * 80)
    print(f"README.md for {repo_full_name}")
    print("=" * 80 + "\n")
    print(readme_content)