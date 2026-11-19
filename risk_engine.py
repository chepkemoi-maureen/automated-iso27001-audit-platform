
from datetime import datetime, timezone

SEVERITY_WEIGHT = {
    "critical": 10,
    "high": 5,
    "medium": 2,
    "low": 1,
}


def score_results(results):
    """
    Takes the list of rule results from compliance_engine.run_compliance_check()
    and returns a risk summary dict.
    """
    auto_results = [r for r in results if r["status"] in ("pass", "fail")]
    manual_results = [r for r in results if r["status"] == "manual"]

    total_auto = len(auto_results)
    passed = [r for r in auto_results if r["status"] == "pass"]
    failed = [r for r in auto_results if r["status"] == "fail"]

    compliance_score = round((len(passed) / total_auto) * 100, 1) if total_auto else 0

    risk_score = sum(SEVERITY_WEIGHT.get(r["severity"], 1) for r in failed)

    failures_by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for r in failed:
        sev = r["severity"]
        if sev in failures_by_severity:
            failures_by_severity[sev] += 1

    if failures_by_severity["critical"] > 0:
        risk_level = "Critical"
    elif failures_by_severity["high"] > 0:
        risk_level = "High"
    elif failures_by_severity["medium"] > 0:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "host": results[0]["host"] if results else None,
        "total_checks": len(results),
        "automated_checks": total_auto,
        "manual_checks": len(manual_results),
        "passed": len(passed),
        "failed": len(failed),
        "compliance_score_pct": compliance_score,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "failures_by_severity": failures_by_severity,
        "failed_rules": [
            {"rule_id": r["rule_id"], "iso_control": r["iso_control"],
             "title": r["title"], "severity": r["severity"]}
            for r in failed
        ],
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    import json
    from compliance_engine import run_compliance_check

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()

    results = run_compliance_check(args.ip, args.user, args.key)
    summary = score_results(results)

    print(f"\n=== Risk Summary for {summary['host']} ===")
    print(f"Compliance score: {summary['compliance_score_pct']}%")
    print(f"Risk level: {summary['risk_level']} (weighted risk score: {summary['risk_score']})")
    print(f"Checks: {summary['passed']} pass / {summary['failed']} fail / "
          f"{summary['manual_checks']} manual — out of {summary['total_checks']}")
    print(f"Failures by severity: {summary['failures_by_severity']}")

    if summary["failed_rules"]:
        print("\nFailed rules:")
        for f in summary["failed_rules"]:
            print(f"  [{f['severity']:8}] {f['rule_id']:10} {f['iso_control']:7} {f['title']}")