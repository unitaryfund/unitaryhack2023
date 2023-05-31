import json
import os
import re

import frontmatter
import github

g = github.Github(os.getenv("GITHUB_TOKEN"))

PROJECT_PATH = "../projects"


def URL_to_repo_key(url: str) -> str:
    repo = re.match("^https:\/\/github\.com\/([\w-]*\/[^\/]*)\/?$", url)
    if repo:
        return repo[1]
    raise ValueError(f"did not find string match for {url}")


def get_project_info():
    for filename in os.listdir(PROJECT_PATH):
        if filename.endswith(".md"):
            yield frontmatter.load(os.path.join(PROJECT_PATH, filename))


projects = {}
for project in get_project_info():
    project_url = project["project_url"]
    main_project_repo_key = URL_to_repo_key(project_url)
    project_name = main_project_repo_key.split("/")[-1].lower()
    issue_list = []
    amount_available = 0
    total_bounty_amount = 0
    bounties = project.get("bounties", [])
    num_open_bounties = 0
    for bounty in bounties:
        total_bounty_amount += bounty["value"]
        repo_key = bounty.get("repo") or main_project_repo_key
        repo = g.get_repo(repo_key)

        issue_num = bounty["issue_num"]
        issue = repo.get_issue(number=issue_num)
        if issue.state == "open":
            amount_available += bounty["value"]
            num_open_bounties += 1
        issue_list.append(
            {
                "title": issue.title,
                "state": issue.state,
                "assignees": [hacker.login for hacker in issue.assignees],
                "value": bounty["value"],
                "url": f"https://github.com/{repo_key}/issues/{issue_num}",
            }
        )

    projects[project_name] = {
        "name": project["title"],
        "emoji": project.get("emoji", ""),
        "url": project["project_url"],
        "bounties": issue_list,
        "amount_available": amount_available,
        "total_amount": total_bounty_amount,
        "num_bounties": len(bounties),
        "num_open_bounties": num_open_bounties,
    }


with open("gh.json", "w") as f:
    json.dump(projects, f, indent=2)
