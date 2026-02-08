import os
from analyzer import analyze_python_file, analyze_generic_file

SUPPORTED_EXTENSIONS = (
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".cpp", ".c", ".h", ".hpp",
    ".java", ".cs", ".php", ".go", ".rs",
    ".html", ".css", ".scss",
    ".json", ".yaml", ".yml",
    ".sh", ".bat", ".sql"
)

def scan_repo(repo_path):
    results = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(SUPPORTED_EXTENSIONS):
                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code = f.read()

                    # Python analyzer
                    if file.endswith(".py"):
                        results[path] = analyze_python_file(code)
                    else:
                        results[path] = analyze_generic_file(code, file)

                except Exception as e:
                    results[path] = [f"Error reading file: {str(e)}"]

    return results


def scan_single_file(file_path):
    results = {}

    if not file_path.endswith(SUPPORTED_EXTENSIONS):
        results[file_path] = ["Unsupported file type."]
        return results

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        if file_path.endswith(".py"):
            results[file_path] = analyze_python_file(code)
        else:
            results[file_path] = analyze_generic_file(code, os.path.basename(file_path))

    except Exception as e:
        results[file_path] = [f"Error reading file: {str(e)}"]

    return results
