import json
import csv

with open("hackers.json") as f:
    hackers = json.load(f)

username_email_map = {}
with open("signups.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for line in reader:
        if line["Email"]:
            username_email_map[line["GitHub Username"]] = line["Email"]

for hacker in hackers:
    username = hacker["username"]
    email = username_email_map[username]
    email_contents = f"""{email}\n\n\nHey {username}!\n\nCongrats on a succesful unitaryHACK event!"""
    if len(hacker["bounties"]) > 1:
        email_contents += f"""We're so happy to see you were able to close {len(hacker["bounties"])} issues across {hacker["num_projects"]} projects. Here are the bounties we believe you should be rewarded for:\n\n"""
        for bounty in hacker["bounties"]:
            email_contents += (
                f'- [{bounty["title"]}]({bounty["url"]}): ${bounty["value"]}\n'
            )
        email_contents += "\n"
    else:
        bounty = hacker["bounties"][0]
        email_contents += f' Our records indicate you were responsible for closing "[{bounty["title"]}]({bounty["url"]})" worth ${bounty["value"]}. '

    email_contents += f"Hence, your total payout is **${hacker['total_value']}USD**!"
    email_contents += """ It's now time to get you paid! We'll need to collect some information from you in order to make this happen. Would you please submit a response to [this form](https://airtable.com/shr0lDyvJxcXeANSB) at your earliest convenience? Once we have the necessary information, we can begin processing your payment.\n\nBest,\nNate Stemen\nunitaryHACK Director"""

    with open(f"emails/hackers/{username}.md", "w") as f:
        f.write(email_contents)
