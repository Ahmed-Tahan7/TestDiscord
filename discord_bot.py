import os
import json
import requests

github_actor = os.getenv("GITHUB_ACTOR")
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
discord_guild_id = os.getenv("DISCORD_GUILD_ID")
contributor_role_id = os.getenv("CONTRIBUTOR_ROLE_ID")

with open("users.json", "r") as f:
    mapping = json.load(f)

discord_user_id = mapping.get(github_actor)
if discord_user_id is None:
    print(f"Warning: No Discord user mapped for GitHub user '{github_actor}'.")
    exit(0)

url = f"https://discord.com/api/guilds/{discord_guild_id}/members/{discord_user_id}/roles/{contributor_role_id}"

headers = {
    "Authorization": f"Bot {discord_bot_token}",
    "Content-Type": "application/json"
}
response = requests.put(url, headers=headers)

if response.status_code == 204:
    print(f"Successfully assigned role to {github_actor} (Discord ID {discord_user_id}).")
else:
    print(f"Failed to assign role. Status: {response.status_code}, {response.text}")
