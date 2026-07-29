import datetime
import json
import os
import sys

import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "Omerabdurrehman")
TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    print("Error: GITHUB_TOKEN environment variable is not set.")
    sys.exit(1)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_PATH = os.path.join(ROOT, "data", "contributions.json")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


def fetch_days():
    response = requests.post(
        "https://api.github.com/graphql",
        json={
            "query": QUERY,
            "variables": {
                "login": USERNAME
            }
        },
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "User-Agent": "Omer-GitHub-Profile"
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        print(result["errors"])
        sys.exit(1)

    calendar = (
        result["data"]["user"]
        ["contributionsCollection"]
        ["contributionCalendar"]
    )

    days = []

    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            days.append(
                {
                    "date": day["date"],
                    "count": day["contributionCount"],
                }
            )

    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    idx = len(days) - 1

    if days[idx]["count"] == 0:
        idx -= 1

    streak = 0
    end_idx = idx

    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1

    if streak == 0:
        return 0, None, None

    start_idx = idx + 1

    return (
        streak,
        days[start_idx]["date"],
        days[end_idx]["date"],
    )


def compute_longest_streak(days):
    longest = 0
    run = 0
    longest_start = None
    longest_end = None
    run_start = None

    for i, day in enumerate(days):
        if day["count"] > 0:
            if run == 0:
                run_start = i

            run += 1

            if run > longest:
                longest = run
                longest_start = days[run_start]["date"]
                longest_end = day["date"]
        else:
            run = 0

    return (
        longest,
        longest_start,
        longest_end,
    )


def build_data(days):
    total = sum(day["count"] for day in days)
    active_days = sum(1 for day in days if day["count"] > 0)

    best_day = max(days, key=lambda d: d["count"])

    current_length, current_start, current_end = compute_current_streak(days)

    longest_length, longest_start, longest_end = compute_longest_streak(days)

    monthly = {}

    for day in days:
        month = day["date"][:7]
        monthly[month] = monthly.get(month, 0) + day["count"]

    monthly = [
        {
            "month": k,
            "total": v,
        }
        for k, v in sorted(monthly.items())
    ]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(
            datetime.UTC
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {
            "start": days[0]["date"],
            "end": days[-1]["date"],
        },
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(
            total / active_days,
            1,
        )
        if active_days
        else 0,
        "current_streak": {
            "length": current_length,
            "start": current_start,
            "end": current_end,
        },
        "longest_streak": {
            "length": longest_length,
            "start": longest_start,
            "end": longest_end,
        },
        "best_day": {
            "date": best_day["date"],
            "count": best_day["count"],
        },
        "monthly": monthly,
        "days": days,
    }


def main():
    days = fetch_days()

    data = build_data(days)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(
        f"Wrote {OUT_PATH}\n"
        f"Total Contributions : {data['total_contributions']}\n"
        f"Current Streak      : {data['current_streak']['length']} days\n"
        f"Longest Streak      : {data['longest_streak']['length']} days\n"
        f"Best Day            : {data['best_day']['count']} contributions on {data['best_day']['date']}"
    )


if __name__ == "__main__":
    main()