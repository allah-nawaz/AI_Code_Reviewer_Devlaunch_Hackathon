import streamlit as st
import os
import zipfile
import tempfile

from reviewer import review_with_llm
from scanner import scan_repo, scan_single_file

st.set_page_config(page_title="AI Code Reviewer", layout="wide")

st.title("AI Code Reviewer (Offline with Remote LLM)")

st.markdown("## 📌 Upload Options")

upload_mode = st.radio(
    "Choose Upload Mode",
    ["Upload Repo ZIP", "Upload Single File"],
    horizontal=True
)

repo_path = None
single_file_path = None

# ----------------- UPLOAD REPO ZIP -----------------
if upload_mode == "Upload Repo ZIP":
    uploaded_zip = st.file_uploader("Upload your repository as ZIP", type=["zip"])

    if uploaded_zip:
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, uploaded_zip.name)

        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.getbuffer())

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # detect extracted repo folder
        extracted_folders = [
            os.path.join(temp_dir, name)
            for name in os.listdir(temp_dir)
            if os.path.isdir(os.path.join(temp_dir, name))
        ]

        repo_path = extracted_folders[0] if extracted_folders else temp_dir
        st.success(f"Repo extracted successfully at: {repo_path}")

# ----------------- UPLOAD SINGLE FILE -----------------
elif upload_mode == "Upload Single File":
    uploaded_file = st.file_uploader(
        "Upload any coding file",
        type=[
            "py", "js", "ts", "jsx", "tsx",
            "cpp", "c", "h", "hpp",
            "java", "cs", "php", "go", "rs",
            "html", "css", "scss",
            "json", "yaml", "yml",
            "sh", "bat", "sql"
        ]
    )

    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        single_file_path = os.path.join(temp_dir, uploaded_file.name)

        with open(single_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File uploaded successfully: {single_file_path}")


# Reviewer Mode
level = st.selectbox(
    "Reviewer Mode",
    ["junior", "senior"],
    help="Choose the strictness level of code review"
)

# Provider selection
provider = st.selectbox(
    "LLM Provider",
    ["auto", "grok", "ollama"],
    help="Auto selects Grok if API key exists, otherwise Ollama"
)

if provider == "auto":
    provider = None


# ---------------- REVIEW BUTTON ----------------
if st.button("Review Code"):

    if upload_mode == "Upload Repo ZIP":
        if not repo_path:
            st.error("❌ Please upload a ZIP repository first.")
        else:
            st.write("🔍 Scanning repository...")
            results = scan_repo(repo_path)

            if not results:
                st.warning("No supported code files found in this repo.")
            else:
                st.success(f"Found {len(results)} code files.")

            for file, issues in results.items():
                st.divider()
                st.subheader(f"📄 File: {file}")

                if issues:
                    st.warning("⚠️ Static Issues Found:")
                    for issue in issues:
                        st.write(f"- {issue}")
                else:
                    st.info("✅ No static issues found.")

                try:
                    with open(file, "r", encoding="utf-8") as f:
                        code = f.read()
                except Exception as e:
                    st.error(f"Could not read file: {e}")
                    continue

                st.code(code)

                with st.spinner("🤖 Getting LLM review..."):
                    review = review_with_llm(code, issues, level, provider=provider)

                st.markdown("### 🧠 LLM Review")
                st.markdown(review)

    elif upload_mode == "Upload Single File":
        if not single_file_path:
            st.error("❌ Please upload a file first.")
        else:
            st.write("🔍 Scanning uploaded file...")
            results = scan_single_file(single_file_path)

            for file, issues in results.items():
                st.divider()
                st.subheader(f"📄 File: {file}")

                if issues:
                    st.warning("⚠️ Static Issues Found:")
                    for issue in issues:
                        st.write(f"- {issue}")
                else:
                    st.info("✅ No static issues found.")

                try:
                    with open(file, "r", encoding="utf-8") as f:
                        code = f.read()
                except Exception as e:
                    st.error(f"Could not read file: {e}")
                    continue

                st.code(code)

                with st.spinner("🤖 Getting LLM review..."):
                    review = review_with_llm(code, issues, level, provider=provider)

                st.markdown("### 🧠 LLM Review")
                st.markdown(review)
