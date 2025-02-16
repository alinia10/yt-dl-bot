from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot_handlers import start, handle_link
from config import load_config
from log import simple_logger, LoggingLevel

def main():
    simple_logger("Starting yt-dl-bot core...", LoggingLevel.INFO)
    
    # Load configuration from conf.toml.
    config = load_config()
    telegram_token = config["telegram"]["token"]
    simple_logger("Configuration loaded successfully.", LoggingLevel.INFO)
    
    # Build the Telegram application.
    app = ApplicationBuilder().token(telegram_token).build()
    simple_logger("Telegram application built.", LoggingLevel.INFO)
    
    # Add command and message handlers.
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    simple_logger("Handlers added: /start and message handler.", LoggingLevel.INFO)
    
    # Start polling for updates.
    simple_logger("Starting polling...", LoggingLevel.INFO)
    app.run_polling()
    simple_logger("Bot polling has stopped.", LoggingLevel.INFO)

if __name__ == "__main__":
    simple_logger("Running core.py", LoggingLevel.INFO)
    main()
