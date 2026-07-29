import os
import requests

TOKEN = os.environ["GITHUB_TOKEN"]

query = """
query {
  viewer {
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

r = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers={
        "Authorization": f"Bearer {TOKEN}"
    },
)

print(r.status_code)
print(r.json())
