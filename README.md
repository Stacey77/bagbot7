# bagbot7

A simple Telegram bot implementation.

## Features

- Basic command handling (/start, /help, /status)
- Interactive dashboard with live statistics (/dashboard)
- Interactive inline keyboard buttons for quick actions
- Random joke generator (/joke)
- Inspirational quote generator (/quote)
- Basic calculator (/calc)
- Message echoing
- Real-time usage tracking and statistics
- Configurable responses, jokes, and quotes
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
- Custom jokes (add your own to the `jokes` list)
- Custom quotes (add your own to the `quotes` list)

Alternatively, set the `BOT_TOKEN` environment variable:
```bash
export BOT_TOKEN="your_telegram_bot_token"
python bot.py
```

## Commands

- `/start` - Start interaction with the bot (includes interactive buttons)
- `/help` - Show available commands
- `/status` - Check bot status
- `/dashboard` - Open interactive dashboard with statistics and quick actions
- `/joke` - Get a random joke
- `/quote` - Get an inspirational quote
- `/calc <expression>` - Calculate a math expression (e.g., `/calc 2+2` or `/calc 10*5-3`)

### Dashboard Features

The `/dashboard` command opens an interactive control panel that shows:
- **Real-time Statistics**: Track messages received, commands executed, jokes told, quotes shared, and calculations performed
- **Quick Action Buttons**: Instant access to jokes, quotes, status, and help
- **Refresh Capability**: Update statistics on demand with the refresh button

## Development

The bot uses the python-telegram-bot library for Telegram API integration.

### Project Structure

- `bot.py` - Main bot implementation
- `config.yml` - Configuration file
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules