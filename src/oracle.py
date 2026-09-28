import re

class CommitOracle:
    def analyze_diff(self, diff_text: str) -> dict:
        type_ = "chore"
        scope = ""
        subject = ""

        # Parse file path from diff header: diff --git a/(.*) b/(.*)
        file_match = re.search(r"diff --git a/(\S+) b/(\S+)", diff_text)
        file_path = file_match.group(1) if file_match else ""

        if file_path:
            # Extract scope from base file name (without extension)
            filename = file_path.split("/")[-1]
            scope = re.sub(r"\.[a-zA-Z0-9]+$", "", filename).lower()

            if file_path.startswith("tests/") or "test_" in file_path:
                type_ = "test"
            elif file_path.startswith("docs/") or file_path.endswith(".md"):
                type_ = "docs"

        has_code_def = False
        has_fix_keyword = False

        for line in diff_text.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                content = line[1:].strip()
                if re.search(r"\b(def|class)\s+", content):
                    has_code_def = True
                if re.search(r"\b(fix|bug|error|issue)\b", content, re.IGNORECASE):
                    has_fix_keyword = True
                if not subject and content:
                    subject = content[:50]

        if has_code_def:
            type_ = "feat"
        elif has_fix_keyword and type_ not in ("docs", "test"):
            type_ = "fix"

        if not subject:
            subject = f"update {scope}" if scope else "update code"

        message = f"{type_}({scope}): {subject}" if scope else f"{type_}: {subject}"

        return {
            "type": type_,
            "scope": scope,
            "subject": subject,
            "message": message
        }