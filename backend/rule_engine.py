def analyze_with_rules(parsed_logs):
    results = []

    for log in parsed_logs:
        msg = log["message"].lower()
        original_message = log["message"]

        if "port 5432" in msg or "database" in msg or "postgres" in msg:
            results.append({
                "category": "Database",
                "root": "Database connection failure",
                "explanation": (
                    "The application attempted to connect to a database service, "
                    "but the connection was refused or the database was unreachable."
                ),
                "impact": (
                    "Application features depending on database access may fail, "
                    "including login, data fetching, and transaction processing."
                ),
                "fixes": [
                    "Verify that the database service is running.",
                    "Check database host, port, username, and password.",
                    "Confirm that port 5432 is open and reachable.",
                    "Check firewall, Docker network, or cloud security group rules."
                ],
                "severity": "High",
                "matched_evidence": original_message
            })

        elif "timeout" in msg:
            results.append({
                "category": "Network/API",
                "root": "Request timeout",
                "explanation": (
                    "A request took longer than expected to complete. "
                    "This may be caused by network latency, overloaded services, or slow external dependencies."
                ),
                "impact": (
                    "Users may experience slow responses, failed requests, or repeated retries."
                ),
                "fixes": [
                    "Check server response time and load.",
                    "Review timeout configuration.",
                    "Inspect network latency between services.",
                    "Add retry logic with exponential backoff if appropriate."
                ],
                "severity": "Medium",
                "matched_evidence": original_message
            })

        elif "permission denied" in msg or "access denied" in msg:
            results.append({
                "category": "Security/Permissions",
                "root": "Permission issue",
                "explanation": (
                    "The application tried to access a resource without having the required permission."
                ),
                "impact": (
                    "The application may fail to read files, write data, or access protected resources."
                ),
                "fixes": [
                    "Check user roles and access permissions.",
                    "Verify file or folder permissions.",
                    "Review service account privileges.",
                    "Avoid giving unnecessary admin access; apply least privilege."
                ],
                "severity": "High",
                "matched_evidence": original_message
            })

        elif "disk full" in msg or "no space left" in msg:
            results.append({
                "category": "Infrastructure",
                "root": "Disk space exhaustion",
                "explanation": (
                    "The system is unable to write new data because available disk space is exhausted."
                ),
                "impact": (
                    "Application logs, uploads, database writes, or temporary files may fail."
                ),
                "fixes": [
                    "Check disk usage.",
                    "Remove unnecessary files or old logs.",
                    "Increase storage capacity.",
                    "Set up log rotation to prevent future disk exhaustion."
                ],
                "severity": "High",
                "matched_evidence": original_message
            })

        elif "memory" in msg or "out of memory" in msg:
            results.append({
                "category": "Performance",
                "root": "Memory exhaustion",
                "explanation": (
                    "The application or system may be consuming more memory than available."
                ),
                "impact": (
                    "The service may become slow, crash, or restart unexpectedly."
                ),
                "fixes": [
                    "Check memory usage of the application.",
                    "Look for memory leaks.",
                    "Increase available memory if needed.",
                    "Optimize large data processing logic."
                ],
                "severity": "High",
                "matched_evidence": original_message
            })

    return results