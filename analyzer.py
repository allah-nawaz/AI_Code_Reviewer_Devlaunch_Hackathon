import ast
import re

def analyze_python_file(code):
    issues = []
    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            # Check for long functions
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 50:
                    issues.append(f"Function '{node.name}' is too long. Consider refactoring.")

            # Check for wildcard imports
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == '*':
                        issues.append("Avoid wildcard imports (from module import *).")

            # Security checks: eval() and exec()
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec']:
                        issues.append(f"Avoid using '{node.func.id}()' for security reasons.")

        # Hardcoded password check
        password_pattern = re.compile(
            r'password\s*=\s*["\'][\w\d!@#$%^&*]+["\']',
            re.IGNORECASE
        )

        for match in password_pattern.finditer(code):
            issues.append("Avoid hardcoded passwords or secrets in code.")

    except SyntaxError as e:
        issues.append(f"Syntax error: {e}")

    return issues


def analyze_generic_file(code, filename="file"):
    """
    Generic analyzer for non-python code files.
    Basic checks only (security + quality).
    """

    issues = []

    # very long file check
    lines = code.splitlines()
    if len(lines) > 500:
        issues.append(f"File '{filename}' is too long ({len(lines)} lines). Consider splitting it.")

    # check for hardcoded secrets
    secret_patterns = [
        r"api[_-]?key\s*=\s*['\"].+['\"]",
        r"secret\s*=\s*['\"].+['\"]",
        r"token\s*=\s*['\"].+['\"]",
        r"password\s*=\s*['\"].+['\"]",
    ]

    for pattern in secret_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            issues.append("Possible hardcoded secret detected (API key / password / token).")

    # check for console logs
    if "console.log" in code:
        issues.append("Remove console.log statements before production.")

    # check for TODO / FIXME
    if "TODO" in code or "FIXME" in code:
        issues.append("TODO/FIXME found. Make sure unfinished code is completed.")

    return issues
