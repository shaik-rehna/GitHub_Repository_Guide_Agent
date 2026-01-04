import streamlit as st
import sys
from pathlib import Path

# ---------------- Path setup ----------------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR / "src"))

from llm_repo_analysis import analyze_repository

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Github Repository Guide Agent",
    page_icon="📘",
    layout="centered",
)

# ---------------- Session State ----------------
if "input_version" not in st.session_state:
    st.session_state.input_version = 0

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "is_running" not in st.session_state:
    st.session_state.is_running = False

# ---------------- Header ----------------
st.title("📘 Github Repository Guide Agent")
st.markdown(
    """
Paste a **public Github repository** (in `owner/repo` format)
and get a **guided walkthrough** of the repository.
"""
)

# ---------------- Input ----------------
repo_name = st.text_input(
    "Github Repository",
    placeholder="psf/requests",
    key=f"repo_name_{st.session_state.input_version}",
)

# ---------------- Cache ----------------
@st.cache_data(show_spinner=False)
def cached_analysis(repo: str) -> str:
    return analyze_repository(repo)

# ---------------- Buttons ----------------
col1, col2 = st.columns([4, 1])

with col1:
    analyze_clicked = st.button(
        "Analyzing..." if st.session_state.is_running else "Analyze Repository",
        use_container_width=True,
        disabled=st.session_state.is_running,
    )

with col2:
    clear_clicked = st.button("Clear", use_container_width=True)

# ---------------- Clear Action (INPUT ONLY) ----------------
if clear_clicked:
    st.session_state.input_version += 1
    st.rerun()

# ---------------- Start Analysis ----------------
if analyze_clicked and not st.session_state.is_running:
    if not repo_name.strip():
        st.warning("Please enter a repository name in 'owner/repo' format")
    else:
        st.session_state.is_running = True
        st.rerun()

# ---------------- Run Analysis ----------------
if st.session_state.is_running:
    with st.spinner("Analyzing repository..."):
        try:
            st.session_state.analysis = cached_analysis(repo_name.strip())
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        finally:
            st.session_state.is_running = False
            st.rerun()

# ---------------- Output ----------------
if st.session_state.analysis:
    st.success("Analysis complete!")
    st.markdown("---")
    st.markdown(st.session_state.analysis)

# ---------------- Footer ----------------
st.markdown("---")
st.caption(
    "Built using PyGithub, Gemini-3-flash, and Streamlit. "
    "Agentic Github Repository Analysis"
)
