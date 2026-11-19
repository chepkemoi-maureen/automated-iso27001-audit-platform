
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "audit_engine"))

from compliance_engine import run_compliance_check
from risk_engine import score_results
from report_engine import generate_report
from storage import save_run
from config import VMS


def main():
    os.makedirs("reports", exist_ok=True)

    for label, vm in VMS.items():
        print(f"\nAuditing {label} ({vm['ip']})...")
        try:
            results = run_compliance_check(vm["ip"], vm["username"], vm["key_path"])
        except Exception as e:
            print(f"  Failed to audit {label}: {e}")
            continue

        summary = score_results(results)
        print(f"  Compliance: {summary['compliance_score_pct']}% | Risk: {summary['risk_level']}")

        save_run(label, results, summary)

        pdf_path = os.path.join("reports", f"{label}_audit_report.pdf")
        generate_report(results, summary, output_path=pdf_path)

    print("\nDone. Run 'python app.py' to view the dashboard.")


if __name__ == "__main__":
    main()