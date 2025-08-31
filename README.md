# Discord Reminder Bot

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Any-lightgrey.svg)](https://github.com/username/discord-reminder-bot)

A lightweight Discord bot built with discord.py that provides a powerful reminder system through slash commands. Perfect for any hosting platform.

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Command Reference](#-command-reference)
- [Architecture](#️-architecture)
- [Deployment](#deployment)
- [Configuration](#️-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [GitHub Repository](#-github-repository)

## ✨ Features

### 🎯 Fun Commands
- `/hi` - Greet users with a personalized message
- `/bye` - Say goodbye to users
- `/about` - Learn about the bot and creator
- `/help` - Comprehensive help with all commands and examples

### ⏰ Reminder System (Main Feature)
- `/remind [time] [message] [delivery]` - Set custom reminders
- **Time Support:**
  - Simple units: `30s`, `5m`, `2h`, `1d`, `1w`, `1mo`, `1y`
  - Complex durations: `"1 year 2 months 3 weeks 4 days 5 hours 10 seconds"`
     - Mixed shorthand: `2h 30m 20s`
   - Absolute dates: `20-09-2025 14:30`

### 🔧 Reminder Management
- `/reminders` - View all active reminders
- `/reminder_edit [id] [new time] [new message] [delivery]` - Modify existing reminders
- `/reminder_delete [id]` - Remove reminders

### 📱 Delivery Options
- **DM**: Bot sends reminder directly to user
- **Server**: Bot posts reminder in channel and pings user

## 🤖 **Bot Permissions Required**

**Your Discord bot needs these permissions:**
- Send Messages
- Use Slash Commands  
- Send Messages in Threads
- Use External Emojis
- Add Reactions
- Read Message History

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Discord bot token
- Any hosting platform (optional)

### GitHub Setup
1. **Fork/Clone** this repository
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your Discord bot token
   ```
4. **Run the bot:**
   ```bash
   python main.py
   ```

### Local Development
1. **Clone/Download** the bot files
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your Discord bot token
   ```
4. **Run the bot:**
   ```bash
   python main.py
   ```

### Deployment
The bot can be deployed on any platform that supports Python 3.10+. Simply upload the files and run `python main.py`.

#### Production Deployment Options

**Option 1: VPS/Cloud Server**
1. Upload bot files to your server
2. Install Python 3.10+
3. Install dependencies: `pip install -r requirements.txt`
4. Create .env file with your token
5. Run: `python main.py`

**Option 2: Docker (Optional)**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**Option 3: Systemd Service (Linux)**
```ini
[Unit]
Description=Discord Reminder Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📋 **Complete Command Reference**

### 🎯 **All Available Commands (8 Total)**

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/hi` | Greet user | None | `/hi` |
| `/bye` | Say goodbye | None | `/bye` |
| `/about` | Bot information | None | `/about` |
| `/help` | Comprehensive help | None | `/help` |
| `/remind` | Set reminder | `[time] [message] [delivery]` | `/remind 1h "Meeting" server` |
| `/reminders` | List reminders | None | `/reminders` |
| `/reminder_edit` | Edit reminder | `[id] [time] [message] [delivery]` | `/reminder_edit 1 "2h" "Updated" dm` |
| `/reminder_delete` | Delete reminder | `[id]` | `/reminder_delete 1` |

### 📝 **Command Parameter Details**

**Time Parameters:**
- **Simple:** `30s`, `5m`, `2h`, `1d`, `1w`, `1mo`, `1y`
- **Complex:** `"1 year 2 months 3 weeks 4 days 5 hours 10 seconds"`
- **Mixed:** `2h 30m 20s`
- **Absolute:** `"20-09-2025 14:30"`

**Message Parameters:**
- Must be enclosed in quotes if containing spaces
- Maximum length: 2000 characters (Discord limit)

**Delivery Parameters:**
- `dm`: Bot sends reminder directly to user
- `server`: Bot posts in channel and pings user

## 📋 Command Reference

### Setting Reminders
```
/remind [time] [message] [delivery]
```

**Examples:**
- `/remind 30s "Check the oven" dm`
- `/remind 5m "Take a break" server`
- `/remind 2h "Team meeting" server`
- `/remind 1d "Pay bills" dm`
- `/remind 1w "Weekly review" server`
- `/remind 1mo "Monthly backup" dm`
- `/remind 1y "Annual checkup" server`
- `/remind "1 year 2 months 3 weeks 4 days 5 hours 10 seconds" "Long term goal" server`
- `/remind "2h 30m 20s" "Mixed time format" dm`
- `/remind "20-09-2025 14:30" "Important deadline" dm`

**Time Format Details:**
- **Simple units:** `30s`, `5m`, `2h`, `1d`, `1w`, `1mo`, `1y`
- **Complex durations:** Natural language like `"1 year 2 months 3 weeks 4 days 5 hours 10 seconds"`
- **Mixed shorthand:** `2h 30m 20s` (hours, minutes, seconds)
- **Absolute dates:** `DD-MM-YYYY HH:MM` format (e.g., `20-09-2025 14:30`)
- **Time parsing:** Supports both relative and absolute time formats

### Managing Reminders
```
/reminders - List all reminders
/reminder_edit [id] [new time] [new message] [new delivery] - Modify reminder
/reminder_delete [id] - Remove reminder
```

**Examples:**
- `/reminders` - View all active reminders with IDs, messages, delivery type, and time remaining
- `/reminder_edit 1 "1h" "Updated reminder message" dm` - Edit reminder ID 1 to trigger in 1 hour
- `/reminder_edit 2 "20-09-2025 15:00" "Meeting reminder" server` - Edit reminder ID 2 to specific date/time
- `/reminder_delete 1` - Delete reminder ID 1

**Reminder Management Features:**
- **List reminders:** Shows all active reminders with unique IDs
- **Edit reminders:** Modify time, message, and delivery method
- **Delete reminders:** Remove specific reminders by ID
- **User isolation:** Users can only manage their own reminders
- **Real-time updates:** Changes take effect immediately

## 🏗️ Architecture

### Core Components
- **main.py**: Bot entry point and slash command setup
- **cogs/fun.py**: Fun commands (/hi, /bye, /about, /help)
- **cogs/reminders.py**: Complete reminder system
- **SQLite Database**: Persistent storage for reminders

### Time Parsing Engine
The bot includes a sophisticated time parsing system that handles:
- **Simple units**: Direct conversion to seconds
- **Complex durations**: Natural language parsing with fallback
- **Absolute dates**: ISO format support
- **Mixed formats**: Combination of different time units

### Scheduler System
- Background task runs every 30 seconds
- Checks for due reminders
- Automatically sends notifications
- Cleans up completed reminders

## 🔒 Security Features

- User-specific reminder access (users can only manage their own reminders)
- Input validation and sanitization
- Error handling with user-friendly messages
- Logging for debugging and monitoring

## 📊 Database Schema

```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel_id INTEGER,
    message TEXT NOT NULL,
    delivery_type TEXT NOT NULL,
    reminder_time TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 🛠️ Configuration

### Environment Variables
```bash
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
BOT_PREFIX=!
```

### Bot Permissions
Your Discord bot needs these permissions:
- Send Messages
- Use Slash Commands
- Send Messages in Threads
- Use External Emojis
- Add Reactions
- Read Message History

## 📝 Logging

The bot includes comprehensive logging:
- Console output
- Error tracking and debugging
- Reminder execution logs

## 🔧 Customization

### Adding New Commands
1. Create a new cog in the `cogs/` directory
2. Follow the existing pattern
3. Add to the extensions list in `main.py`

### Modifying Time Parsing
The time parsing logic is in `cogs/reminders.py`:
- `parse_time()`: Main parsing function
- `_parse_simple_units()`: Handle simple formats
- `_parse_complex_duration()`: Handle complex durations

## 🎯 **Bot Status & Success Indicators**

### ✅ **Bot is Working Correctly When:**
- Bot shows as "Online" in your Discord server
- Slash commands appear when typing `/` in any channel
- Commands respond without errors
- Reminders are set and triggered at the correct time
- Database file (`reminders.db`) is created automatically
- Console shows "Synced X command(s)" message

### 📊 **Expected Console Output:**
```
2025-08-31 18:15:17,543 - __main__ - INFO - Loaded extension: cogs.fun
2025-08-31 18:15:17,596 - cogs.reminders - INFO - Database initialized successfully
2025-08-31 18:15:17,596 - __main__ - INFO - Loaded extension: cogs.reminders
2025-08-31 18:15:21,428 - __main__ - INFO - YourBot#1234 has connected to Discord!
2025-08-31 18:15:21,975 - __main__ - INFO - Synced 8 command(s)
```

## 🚨 Troubleshooting

### Common Issues

1. **Slash Commands Not Working**
   - Ensure bot has proper permissions
   - Check if commands are synced
   - Verify bot is in your server

2. **Reminders Not Triggering**
   - Check database file permissions
   - Verify bot has access to channels/users
   - Check console output for errors

3. **Time Parsing Errors**
   - Use supported time formats
   - Check for typos in duration strings
   - Verify date format for absolute dates (DD-MM-YYYY HH:MM)

### ⚠️ **Common Error Messages & Solutions:**
- **"Invalid time format"** → Use supported formats like `30s`, `5m`, `2h`, `1d`, `1w`, `1mo`, `1y`
- **"Invalid date format. Use DD-MM-YYYY HH:MM"** → Use format like `20-09-2025 14:30`
- **"Invalid delivery type. Use 'dm' or 'server'"** → Only `dm` and `server` are valid
- **"Reminder not found"** → Check reminder ID with `/reminders` command
- **"Cannot send DM to user"** → User has DMs disabled for the bot

### 📝 **Time Format Limitations:**
- **Months:** Approximated as 30 days (not calendar months)
- **Years:** Approximated as 365 days (not leap year aware)
- **Timezone:** Uses server's local timezone
- **Date range:** No future limit, but past dates will trigger immediately

### Debug Mode
Enable detailed logging by modifying the logging level in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Resource Usage
- **Memory**: ~50-100 MB typical usage
- **CPU**: Minimal during idle, spikes during reminder processing
- **Storage**: SQLite database + logs (~10-50 MB typical)

### Optimization Tips
- Use systemd service for production deployment
- Implement log rotation for long-term hosting
- Regular database cleanup of old reminders
- Monitor resource usage on your hosting platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📦 GitHub Repository

This bot is designed to be easily deployable from GitHub:

- **Clone:** `git clone https://github.com/username/discord-reminder-bot.git`
- **Install:** `pip install -r requirements.txt`
- **Configure:** Copy `env.example` to `.env` and add your bot token
- **Run:** `python main.py`

### Repository Structure
```
discord-reminder-bot/
├── main.py              # Bot entry point
├── cogs/                # Bot command modules
│   ├── fun.py          # Fun commands (/hi, /bye, /about, /help)
│   └── reminders.py    # Reminder system
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/license/mit).
