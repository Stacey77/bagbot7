# bagbot7

A simple Telegram bot implementation.

## Features

- Basic command handling (/start, /help, /status)
- Message echoing
- Configurable responses
- Error handling and logging

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the bot:
   - Copy `config.yml` and update with your bot token, OR
   - Set the `BOT_TOKEN` environment variable

3. Run the bot:
```bash
python bot.py
```

## Configuration

Edit `config.yml` to customize:
- Bot token
- Bot name
- Command responses

Alternatively, set the `BOT_TOKEN` environment variable:
```bash
export BOT_TOKEN="your_telegram_bot_token"
python bot.py
```

## Commands

- `/start` - Start interaction with the bot
- `/help` - Show available commands
- `/status` - Check bot status

## Development

The bot uses the python-telegram-bot library for Telegram API integration.

### Project Structure

- `bot.py` - Main bot implementation
- `config.yml` - Configuration file
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules