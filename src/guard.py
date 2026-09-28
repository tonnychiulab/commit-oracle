import re

class SecurityGuard:
    def scan_diff(self, diff_text):
        issues = []

        # Define regex patterns
        api_key_patterns = [
            r'sk-[a-zA-Z0-9_-]{20,}',  # OpenAI
            r'ghp_[a-zA-Z0-9]{20,}',  # GitHub
            r'AKIA[0-9A-Z]{16}',       # AWS
        ]

        private_key_patterns = [
            r'-----BEGIN (RSA|OPENSSH|EC|PGP)? PRIVATE KEY-----'
        ]

        sensitive_password_pattern = r'(?i)(password|passwd|secret)\s*[:=]\s*["\'][^"\']+["\']'

        sensitive_file_extensions = ['.env', '.pem', 'id_rsa']

        # Scan for new lines in the diff
        for line in diff_text.split('\n'):
            if line.startswith('+'):
                # Check for API keys
                for pattern in api_key_patterns:
                    if re.search(pattern, line):
                        issues.append('Potential API key found: ' + line)

                # Check for private keys
                for pattern in private_key_patterns:
                    if re.search(pattern, line):
                        issues.append('Potential private key found: ' + line)

                # Check for hard-coded passwords
                if re.search(sensitive_password_pattern, line):
                    issues.append('Potential sensitive password found: ' + line)

                # Check for sensitive file extensions
                if any(ext in line for ext in sensitive_file_extensions):
                    issues.append('Sensitive file extension found: ' + line)

        return issues
