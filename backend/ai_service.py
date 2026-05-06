import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def analyze_logs(logs: str):
    prompt = f"""
You are an expert system engineer.

Analyze the logs and STRICTLY respond in this format:

Root Cause: <one line>
Explanation: <one or two lines>
Fix: <one or two lines>
Severity: <Low/Medium/High>

Logs:
{logs}
"""

    try:
        response = requests.post(API_URL, json={"inputs": prompt}, timeout=5)

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]

    except:
        pass  # Ignore AI failure

    # 🔥 FALLBACK LOGIC

    logs_lower = logs.lower()

    if "database" in logs_lower or "port 5432" in logs_lower:
        return """Root Cause: Database connection failure
Explanation: Application failed to connect to database server
Fix: Check DB server, credentials, and port availability
Severity: High"""

    elif "timeout" in logs_lower:
        return """Root Cause: Network timeout
Explanation: Request took too long to respond
Fix: Check network latency, server load, and retry logic
Severity: Medium"""

    elif "permission denied" in logs_lower:
        return """Root Cause: Permission issue
Explanation: Application does not have required access rights
Fix: Check file permissions or user roles
Severity: High"""

    elif "disk full" in logs_lower:
        return """Root Cause: Disk space exhaustion
Explanation: System ran out of storage space
Fix: Clean up disk or increase storage capacity
Severity: High"""

    else:
        return """Root Cause: Unknown issue
Explanation: Unable to determine exact cause
Fix: Check logs manually or enable detailed logging
Severity: Low"""