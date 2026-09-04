from pathlib import Path
import sys
import yaml

DATA_FILE = Path("risk/sample-data.yml")
RULES_FILE = Path("risk/risk-rules.yml")
REPORT_FILE = Path("dashboard/risk-report.md")


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def level(score, thresholds):
    if score <= thresholds["low_max"]:
        return "🟢 LOW"
    if score <= thresholds["medium_max"]:
        return "🟡 MEDIUM"
    return "🔴 HIGH"


def calculate(service, weights):
    # Lab normalization: these reference points deliberately make the exercise easy to explain.
    ci = clamp(service["failed_workflows"] / 10 * 100)
    pr_size = clamp(service["large_prs"] / 6 * 100)
    rework = clamp(service["rework_rate"] / 0.35 * 100)
    review = clamp(service["average_review_hours"] / 20 * 100)
    component = clamp(service["component_risk"])

    contributions = {
        "CI instability": ci * weights["ci_instability"],
        "PR size": pr_size * weights["pr_size"],
        "Rework": rework * weights["rework"],
        "Review friction": review * weights["review_friction"],
        "Component risk": component * weights["component_risk"],
    }

    score = round(sum(contributions.values()))
    return {
        "score": score,
        "signals": {
            "CI instability": round(ci),
            "PR size": round(pr_size),
            "Rework": round(rework),
            "Review friction": round(review),
            "Component risk": round(component),
        },
        "contributions": {k: round(v) for k, v in contributions.items()},
    }


def main():
    data = yaml.safe_load(DATA_FILE.read_text())
    rules = yaml.safe_load(RULES_FILE.read_text())
    weights = rules["weights"]
    thresholds = rules["thresholds"]

    results = {}
    for service_name, service in data["services"].items():
        result = calculate(service, weights)
        results[service_name] = {**service, **result}

    teams = {}
    for service_name, result in results.items():
        teams.setdefault(result["team"], []).append((service_name, result))

    team_results = {}
    for team, services in teams.items():
        total_prs = sum(item[1]["pull_requests"] for item in services)
        weighted_score = sum(item[1]["score"] * item[1]["pull_requests"] for item in services) / total_prs
        team_results[team] = round(weighted_score)

    org_prs = sum(result["pull_requests"] for result in results.values())
    org_score = round(sum(result["score"] * result["pull_requests"] for result in results.values()) / org_prs)

    lines = []
    lines.append("# Engineering Risk Heatmap")
    lines.append("")
    lines.append(f"**Organization Risk:** {org_score}/100 {level(org_score, thresholds)}")
    lines.append("")
    lines.append("## Organization Heatmap")
    lines.append("")
    lines.append("| Team | Risk Score | Status |")
    lines.append("|---|---:|---|")
    for team, score in sorted(team_results.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {team.title()} | {score} | {level(score, thresholds)} |")

    lines.append("")
    lines.append("## Service Drill-down")
    lines.append("")
    lines.append("| Team | Service | Risk | Status | PRs |")
    lines.append("|---|---|---:|---|---:|")
    for service_name, result in sorted(results.items(), key=lambda x: x[1]["score"], reverse=True):
        lines.append(f"| {result['team'].title()} | {service_name.title()} | {result['score']} | {level(result['score'], thresholds)} | {result['pull_requests']} |")

    lines.append("")
    lines.append("## Top Risk Drivers")
    lines.append("")
    for service_name, result in sorted(results.items(), key=lambda x: x[1]["score"], reverse=True):
        top = sorted(result["contributions"].items(), key=lambda x: x[1], reverse=True)[:3]
        drivers = ", ".join(f"{name} +{value}" for name, value in top)
        lines.append(f"### {service_name.title()} — {result['score']}/100 {level(result['score'], thresholds)}")
        lines.append("")
        lines.append(f"Top drivers: **{drivers}**")
        lines.append("")

    lines.append("## Management View")
    lines.append("")
    highest_team = max(team_results, key=team_results.get)
    highest_service = max(results, key=lambda name: results[name]["score"])
    highest_result = results[highest_service]
    top_driver = max(highest_result["contributions"], key=highest_result["contributions"].get)
    lines.append(f"- Highest-risk team: **{highest_team.title()} ({team_results[highest_team]}/100)**")
    lines.append(f"- Highest-risk service: **{highest_service.title()} ({highest_result['score']}/100)**")
    lines.append(f"- Main driver of the highest-risk service: **{top_driver}**")
    lines.append("- Suggested discussion: reduce the dominant engineering signal and rerun the workflow to observe the score change.")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines) + "\n")

    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
