import re

def parse_logs(raw_logs: str):
    logs = []
    lines = raw_logs.split("\n")

    for line in lines:
        match = re.match(r"(.*)\s+(ERROR|WARN|INFO)\s+(.*)", line)

        if match:
            logs.append({
                "timestamp": match.group(1),
                "level": match.group(2),
                "message": match.group(3)
            })
        else:
            logs.append({
                "timestamp": None,
                "level": "UNKNOWN",
                "message": line
            })

    return logs