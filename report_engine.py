
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from datetime import datetime

RISK_COLOR = {
    "Critical": colors.HexColor("#B00020"),
    "High": colors.HexColor("#E65100"),
    "Medium": colors.HexColor("#F9A825"),
    "Low": colors.HexColor("#2E7D32"),
}


def generate_report(results, summary, output_path="audit_report.pdf"):
    """
    results: full list of rule results from compliance_engine.run_compliance_check()
    summary: risk summary dict from risk_engine.score_results()
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("ISO 27001 Internal Audit Report", styles["Title"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elements.append(Paragraph(f"Host audited: {summary['host']}", styles["Normal"]))
    if results:
        elements.append(Paragraph(f"Rule source: {results[0]['source']}", styles["Normal"]))
    elements.append(Spacer(1, 0.6 * cm))

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Paragraph(
        f"Compliance score: {summary['compliance_score_pct']}% "
        f"({summary['passed']}/{summary['automated_checks']} automated checks passed)",
        styles["Normal"]
    ))
    risk_style = styles["Normal"]
    elements.append(Paragraph(
        f"Overall risk level: <font color='{RISK_COLOR.get(summary['risk_level'], colors.black).hexval()}'>"
        f"<b>{summary['risk_level']}</b></font> (weighted risk score: {summary['risk_score']})",
        risk_style
    ))
    elements.append(Paragraph(
        f"Manual review required: {summary['manual_checks']} check(s)",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 0.4 * cm))

    sev = summary["failures_by_severity"]
    elements.append(Paragraph(
        f"Failures by severity — Critical: {sev['critical']}, High: {sev['high']}, "
        f"Medium: {sev['medium']}, Low: {sev['low']}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 0.8 * cm))

    elements.append(Paragraph("Detailed Findings", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    table_data = [["Rule ID", "ISO Control", "Title", "Severity", "Result"]]
    for r in results:
        table_data.append([
            r["rule_id"], r["iso_control"], r["title"][:45],
            r["severity"], r["status"].upper()
        ])

    table = Table(table_data, colWidths=[2.2 * cm, 2.2 * cm, 7.5 * cm, 2.2 * cm, 2.2 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))

    for i, r in enumerate(results, start=1):
        if r["status"] == "fail":
            table.setStyle(TableStyle([("TEXTCOLOR", (4, i), (4, i), colors.red)]))
        elif r["status"] == "manual":
            table.setStyle(TableStyle([("TEXTCOLOR", (4, i), (4, i), colors.orange)]))

    elements.append(table)
    elements.append(Spacer(1, 0.8 * cm))

    if summary["failed_rules"]:
        elements.append(Paragraph("Recommendations", styles["Heading2"]))
        for f in summary["failed_rules"]:
            elements.append(Paragraph(
                f"<b>{f['rule_id']} ({f['iso_control']})</b> — {f['title']}. "
                f"Severity: {f['severity']}. Remediate per CIS Ubuntu Linux 24.04 LTS "
                f"Benchmark recommendation {f['rule_id']}.",
                styles["Normal"]
            ))
            elements.append(Spacer(1, 0.15 * cm))

    doc.build(elements)
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    import argparse
    from compliance_engine import run_compliance_check
    from risk_engine import score_results

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--out", default="audit_report.pdf")
    args = parser.parse_args()

    results = run_compliance_check(args.ip, args.user, args.key)
    summary = score_results(results)
    generate_report(results, summary, output_path=args.out)