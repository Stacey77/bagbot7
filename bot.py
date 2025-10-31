#!/usr/bin/env python3
"""
bagbot7 - A simple Telegram bot
"""
import os
import yaml
import logging
import random
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

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
        self.jokes = self.config.get('jokes', self.get_default_jokes())
        self.quotes = self.config.get('quotes', self.get_default_quotes())
        
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
    
    def get_default_jokes(self):
        """Get default jokes if not in config"""
        return [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
    
    def get_default_quotes(self):
        """Get default quotes if not in config"""
        return [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is 10% what happens to you and 90% how you react to it. - Charles R. Swindoll",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
        ]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        message = self.commands.get('start', 'Hello! I am bagbot7. Use /help to see what I can do!')
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton("📋 Help", callback_data='help'),
             InlineKeyboardButton("📊 Status", callback_data='status')],
            [InlineKeyboardButton("😄 Tell a Joke", callback_data='joke'),
             InlineKeyboardButton("💭 Get a Quote", callback_data='quote')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        message = self.commands.get('help', 
            'Available commands:\n'
            '/start - Start interaction with the bot\n'
            '/help - Show this help message\n'
            '/status - Check bot status\n'
            '/joke - Get a random joke\n'
            '/quote - Get an inspirational quote\n'
            '/calc <expression> - Calculate a math expression (e.g., /calc 2+2)')
        await update.message.reply_text(message)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        message = self.commands.get('status', '✅ Bot is running smoothly!')
        await update.message.reply_text(message)
    
    async def joke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /joke command"""
        joke = random.choice(self.jokes)
        await update.message.reply_text(f"😄 {joke}")
    
    async def quote_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote command"""
        quote = random.choice(self.quotes)
        await update.message.reply_text(f"💭 {quote}")
    
    async def calc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /calc command for basic calculations"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "Usage: /calc <expression>\n"
                    "Example: /calc 2+2 or /calc 10*5-3"
                )
                return
            
            expression = ' '.join(context.args)
            # Security: only allow numbers and basic operators
            if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', expression):
                await update.message.reply_text("Invalid expression. Only numbers and +, -, *, /, (, ) are allowed.")
                return
            
            result = eval(expression)
            await update.message.reply_text(f"🔢 {expression} = {result}")
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            await update.message.reply_text(f"Error calculating: {str(e)}")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'help':
            message = ('Available commands:\n'
                      '/start - Start interaction with the bot\n'
                      '/help - Show this help message\n'
                      '/status - Check bot status\n'
                      '/joke - Get a random joke\n'
                      '/quote - Get an inspirational quote\n'
                      '/calc <expression> - Calculate a math expression')
            await query.edit_message_text(text=message)
        elif query.data == 'status':
            await query.edit_message_text(text='✅ Bot is running smoothly!')
        elif query.data == 'joke':
            joke = random.choice(self.jokes)
            await query.edit_message_text(text=f"😄 {joke}")
        elif query.data == 'quote':
            quote = random.choice(self.quotes)
            await query.edit_message_text(text=f"💭 {quote}")
    
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
        application.add_handler(CommandHandler("joke", self.joke_command))
        application.add_handler(CommandHandler("quote", self.quote_command))
        application.add_handler(CommandHandler("calc", self.calc_command))
        
        # Register callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
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
