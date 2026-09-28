import argparse
import subprocess
import sys
from src.guard import SecurityGuard
from src.oracle import CommitOracle

def get_git_diff() -> str:
    try:
        res = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout
    except Exception:
        return ""

def run_security_check(diff_text: str) -> bool:
    guard = SecurityGuard()
    issues = guard.scan_diff(diff_text)
    if issues:
        print("[!] Security Alert: Potential secrets detected in diff:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    print("[+] Security check passed: No secrets detected.")
    return True

def run_commit_generation(diff_text: str) -> str:
    if not diff_text.strip():
        print("[*] No diff detected in working directory.")
        return ""
    oracle = CommitOracle()
    res = oracle.analyze_diff(diff_text)
    print("\nSuggested Commit Message:")
    print("----------------------------------------")
    print(res["message"])
    print("----------------------------------------")
    return res["message"]

def main(args=None):
    parser = argparse.ArgumentParser(description="commit-oracle: Git smart commit and security scanner")
    parser.add_argument("--check", action="store_true", help="Run security check on diff only")
    parser.add_argument("--generate", action="store_true", help="Generate suggested commit message only")
    parser.add_argument("--version", action="version", version="commit-oracle 1.0.0")

    parsed = parser.parse_args(args)
    diff_text = get_git_diff()

    if parsed.check:
        passed = run_security_check(diff_text)
        return 0 if passed else 1

    if parsed.generate:
        run_commit_generation(diff_text)
        return 0

    # Default: run check and generate
    passed = run_security_check(diff_text)
    if not passed:
        return 1
    run_commit_generation(diff_text)
    return 0

if __name__ == "__main__":
    sys.exit(main())
