#!/usr/bin/env python3
"""
bagbot7 - A simple Telegram bot
"""
import os
import yaml
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class BagBot:
    """Main bot class"""
    
    def __init__(self, config_path='config.yml'):
        """Initialize bot with configuration"""
        self.config = self.load_config(config_path)
        self.token = self.config.get('bot', {}).get('token', os.getenv('BOT_TOKEN'))
        self.commands = self.config.get('commands', {})
        
        if not self.token or self.token == "YOUR_BOT_TOKEN_HERE":
            raise ValueError("Bot token not configured. Set BOT_TOKEN env variable or update config.yml")
    
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        message = self.commands.get('start', 'Hello! I am bagbot7.')
        await update.message.reply_text(message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        message = self.commands.get('help', 'Available commands: /start, /help, /status')
        await update.message.reply_text(message)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        message = self.commands.get('status', 'Bot is running!')
        await update.message.reply_text(message)
    
    async def echo_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Echo received messages"""
        user_message = update.message.text
        logger.info(f"Received message: {user_message}")
        await update.message.reply_text(f"You said: {user_message}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting bagbot7...")
        
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("status", self.status_command))
        
        # Register message handler for echoing
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo_message))
        
        # Register error handler
        application.add_error_handler(self.error_handler)
        
        # Start the bot
        logger.info("Bot is ready!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""
    try:
        bot = BagBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise


if __name__ == '__main__':
    main()
