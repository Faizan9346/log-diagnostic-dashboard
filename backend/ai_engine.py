import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def analyze_with_ai(logs: str, rule_output: dict):
    prompt = f"""
You are a system debugging assistant.

A rule-based diagnostic engine found this issue:

Category: {rule_output.get("category")}
Root Cause: {rule_output.get("root")}
Explanation: {rule_output.get("explanation")}
Severity: {rule_output.get("severity")}
Confidence: {rule_output.get("confidence")}

Logs:
{logs}

Improve the explanation in 2 lines and suggest one additional practical debugging step.
"""

    try:
        response = requests.post(API_URL, json={"inputs": prompt}, timeout=5)

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, list) and data and "generated_text" in data[0]:
                generated_text = data[0]["generated_text"].strip()

                if generated_text:
                    return generated_text

    except Exception:
        pass

    return None