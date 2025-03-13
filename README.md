Sure! Here’s a **less formal, more natural version** of your README that still explains everything clearly but in a way that doesn’t feel overly polished. This makes it **sound more like a student project** rather than a corporate-level project.

---

# **GitHub Actions - Discord Role Assignment and PR Notifications**  

## **Overview**  
This project automates two things using **GitHub Actions** and **Discord API**:
1. When a **pull request (PR) is merged**, the contributor gets a **role in Discord**.
2. Whenever a **PR is opened or closed**, a notification is sent to a Discord channel.  

This setup makes it easier to **track contributors** and keep Discord members updated about GitHub activity.

---

## **Features**  
- **Automatically assigns a Discord role** to contributors when their PR is merged.  
- **Sends a notification** in Discord whenever a PR is opened or closed.  
- **Runs entirely on GitHub Actions**—no need to host a separate bot.  

---

## **Setup**  

### **1. Set Up a Discord Webhook**  
1. Open Discord and go to your **server settings**.  
2. Choose a **text channel** for notifications.  
3. Go to **"Integrations"** → **"Create Webhook"**.  
4. Copy the webhook URL.  

---

### **2. Create a Discord Bot (For Role Assignment)**  
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).  
2. Click **"New Application"**, give it a name, and go to the **"Bot"** tab.  
3. Click **"Add Bot"** and copy the bot token (you’ll need it later).  
4. Under **OAuth2** → **URL Generator**, select:
   - `bot`
   - `Manage Roles`
   - `Send Messages`  
5. Copy the generated invite link and add the bot to your Discord server.  
6. **Important:** In **Server Settings → Roles**, make sure:
   - The bot has **"Manage Roles"** permission.  
   - The bot’s role is **above** the role it needs to assign.  

---

### **3. Add GitHub Secrets**  
Go to your repo’s **Settings → Secrets and variables → Actions** and add these secrets:

- `DISCORD_BOT_TOKEN` → The bot token from the Developer Portal.  
- `DISCORD_WEBHOOK_URL` → The Discord webhook URL.  
- `DISCORD_GUILD_ID` → Your Discord server ID.  
- `CONTRIBUTOR_ROLE_ID` → The ID of the role you want to assign.  

To find the **guild and role IDs**, enable **Developer Mode** in Discord (User Settings → Advanced), then **right-click** the server/role → "Copy ID".

---

### **4. Create a GitHub → Discord Username Mapping**  
Since GitHub and Discord usernames are different, we need a file to **map GitHub users to their Discord IDs**.  

Create `users.json` in your repo:  

```json
{
  "Ahmed-Tahan7": "632388701204381705"
}
```
Replace `"Ahmed-Tahan7"` with a **GitHub username**, and `"632388701204381705"` with the **Discord user ID**.

---

## **GitHub Actions Workflow**  
The workflow is located in `.github/workflows/discord-integration.yml`.  

### **What It Does:**
1. **Sends a notification** to Discord when a PR is opened or closed.  
2. **Assigns a role** to the PR author when the PR is merged.  

### **Workflow File (`.github/workflows/discord-integration.yml`)**  

```yaml
name: Discord Integration

on:
  pull_request:
    types: [opened, closed]

jobs:
  discord_integration:
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: pip install requests

      - name: Assign Discord role when PR is merged
        if: ${{ github.event.action == 'closed' && github.event.pull_request.merged == true }}
        run: python discord_bot.py
        env:
          GITHUB_ACTOR: ${{ github.actor }}
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          DISCORD_GUILD_ID: ${{ secrets.DISCORD_GUILD_ID }}
          CONTRIBUTOR_ROLE_ID: ${{ secrets.CONTRIBUTOR_ROLE_ID }}

      - name: Notify Discord channel
        if: ${{ always() }}
        run: |
          curl -H "Content-Type: application/json" \
          -X POST \
          -d '{
            "username": "GitHub Bot",
            "content": "**PR Event**: \"${{ github.event.action }}\"\n**User**: \"${{ github.actor }}\"\n**PR**: \"${{ github.event.pull_request.title }}\"\n**Link**: \"${{ github.event.pull_request.html_url }}\""
          }' \
          ${{ secrets.DISCORD_WEBHOOK_URL }}
```

---

## **Python Script for Role Assignment (`discord_bot.py`)**  

```python
import os
import json
import requests

github_actor = os.getenv("GITHUB_ACTOR")

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
discord_guild_id = os.getenv("DISCORD_GUILD_ID")
contributor_role_id = os.getenv("CONTRIBUTOR_ROLE_ID")

# Load GitHub → Discord user mapping
with open("users.json", "r") as f:
    mapping = json.load(f)

discord_user_id = mapping.get(github_actor)
if discord_user_id is None:
    print(f"Skipping: No Discord user found for GitHub user '{github_actor}'.")
    exit(0)

# Assign the role
url = f"https://discord.com/api/guilds/{discord_guild_id}/members/{discord_user_id}/roles/{contributor_role_id}"

headers = {
    "Authorization": f"Bot {discord_bot_token}",
    "Content-Type": "application/json"
}

response = requests.put(url, headers=headers)

if response.status_code == 204:
    print(f"Role assigned to {github_actor} (Discord ID {discord_user_id}).")
else:
    print(f"Error: {response.status_code}, {response.text}")
```

---

## **Testing**
1. Open a **test pull request**.  
2. Check if a **Discord notification** appears.  
3. Merge the PR and verify that the **role is assigned**.  
4. If something doesn’t work, **check GitHub Actions logs** for errors.  

---

## **Troubleshooting**
### **Role is not assigned**
- Check if the **GitHub username is mapped correctly** in `users.json`.  
- Make sure the **bot has "Manage Roles" permission**.  
- The bot’s role **must be above the Contributor role** in the role list.

### **Webhook notifications are not working**
- Verify that **`DISCORD_WEBHOOK_URL` is set in GitHub secrets**.  
- Check if the **webhook is still valid** in Discord settings.

### **GitHub Actions fails**
- Open **GitHub Actions → Failed Workflow** and check the logs.  
- Make sure all **GitHub secrets** are set correctly.  

---

## **Next Steps**
- Track **other contributions** (like issues, commits, discussions).  
- Add a **leaderboard** to show top contributors.  
- Allow users to **link their Discord and GitHub accounts automatically** instead of using `users.json`.  
