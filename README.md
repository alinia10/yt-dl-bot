# yt-dl-bot

yt-dl-bot is a Telegram bot that downloads YouTube videos (or entire playlists) and then uploads them either directly to Telegram or, if the file exceeds Telegram’s file size limits, to a Nextcloud server (via WebDAV). After processing each video, it removes the local file to manage server disk space.

# Configuration

Create or update the conf.toml file in the root directory with your settings. For example:
```toml
[telegram]
token = "YOUR_TELEGRAM_BOT_TOKEN"

[nextcloud]
url = "https://iutbox.iut.ac.ir/remote.php/dav/files/your_username"
share_api_url = "https://iutbox.iut.ac.ir/ocs/v2.php/apps/files_sharing/api/v1/shares"
username = "your_username"
token = "your_app_token"  # Use your Nextcloud app token (or password if you prefer)
```
Additionally, ensure you have a valid cookies.txt file in the project root (exported from your browser) for yt-dlp to access YouTube.

# Running the Bot

Start the bot by running the main entry point:
```bash
poetry run python src/core.py
```