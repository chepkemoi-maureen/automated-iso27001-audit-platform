import json
from datetime import datetime, timezone
from ssh_manager import SSHManager


def load_knowledge_base(path="rules/knowledge_base.json"):
    with open(path) as f:
        data = json.load(f)
    return data["source"], data["rules"]


def evaluate_rule(rule, output, error):
   
    
    if rule["level"] == "Manual":
        return "manual"

    if error and not output:
        return "fail"

    stripped_output = output.strip()
    expected = rule["expected_contains"]

    status_words = {"active", "inactive", "enabled", "disabled"}
    if expected in status_words:
       tokens = stripped_output.split()
       return "pass" if tokens and all(t == expected for t in tokens) else "fail"

    return "pass" if expected in output else "fail"


def run_compliance_check(ip, username, key_path, rules_path="rules/knowledge_base.json"):
   
    source, rules = load_knowledge_base(rules_path)
    results = []

    with SSHManager(ip, username, key_path) as ssh:
        for rule in rules:
            output, error = ssh.run_command(rule["command"])
            status = evaluate_rule(rule, output, error)

            results.append({
                "rule_id": rule["rule_id"],
                "iso_control": rule["iso_control"],
                "title": rule["title"],
                "command": rule["command"],
                "expected_contains": rule["expected_contains"],
                "actual_output": output,
                "error": error,
                "status": status,          # "pass" | "fail" | "manual"
                "severity": rule["severity"],
                "explanation": rule.get("explanation", ""),
                "recommendation": rule.get("recommendation", ""),
                "source": source,
                "host": ip,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            })

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()

    results = run_compliance_check(args.ip, args.user, args.key)

    print(f"\n=== Compliance Results for {args.ip} ===\n")
    for r in results:
        print(f"[{r['status'].upper():6}] {r['rule_id']:10} {r['iso_control']:7} {r['title']}")

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    manual = sum(1 for r in results if r["status"] == "manual")
    print(f"\nSummary: {passed} pass, {failed} fail, {manual} manual review — out of {total}")