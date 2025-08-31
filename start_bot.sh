#!/bin/bash

# Discord Bot Startup Script
# Use this script to easily start the bot on Oracle Cloud VM

echo "🚀 Starting Discord Reminder Bot..."

# Check if virtual environment exists
if [ ! -d "botenv" ]; then
    echo "📦 Creating virtual environment..."
    python3.10 -m venv botenv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source botenv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please create .env file with your Discord bot token:"
    echo "   DISCORD_TOKEN=your_bot_token_here"
    echo "   DISCORD_GUILD_ID=your_guild_id_here"
    exit 1
fi

# Start the bot
echo "🤖 Starting bot..."
python main.py
