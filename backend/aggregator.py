def aggregate_results(results):
    if not results:
        return {
            "category": "Unknown",
            "root": "No known issue detected",
            "explanation": "The current rules did not match any known failure pattern.",
            "impact": "Impact cannot be determined from the provided logs.",
            "fixes": [
                "Check complete logs around the failure time.",
                "Look for ERROR, WARN, timeout, denied, failed, or exception messages.",
                "Enable detailed logging if the issue is not visible."
            ],
            "severity": "Low",
            "confidence": "Low",
            "matched_evidence": "No matching evidence found"
        }

    severity_order = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    best = max(results, key=lambda item: severity_order.get(item["severity"], 1))

    evidence_count = len(results)

    if best["severity"] == "High" and evidence_count >= 1:
        best["confidence"] = "High"
    elif best["severity"] == "Medium":
        best["confidence"] = "Medium"
    else:
        best["confidence"] = "Low"

    best["total_matches"] = evidence_count

    return best