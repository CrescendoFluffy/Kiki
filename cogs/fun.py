import discord
from discord import app_commands
from discord.ext import commands


class FunCommands(commands.Cog):
    """Fun commands for the bot"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="hi", description="Greet the user")
    async def hi(self, interaction: discord.Interaction):
        """Reply with a greeting"""
        await interaction.response.send_message(f"Hi {interaction.user.mention}!")
    
    @app_commands.command(name="bye", description="Say goodbye to the user")
    async def bye(self, interaction: discord.Interaction):
        """Reply with a goodbye message"""
        await interaction.response.send_message(f"Goodbye {interaction.user.mention}!")
    
    @app_commands.command(name="about", description="Learn about the bot")
    async def about(self, interaction: discord.Interaction):
        """Show information about the bot"""
        embed = discord.Embed(
            title="🤖 Discord Reminder Bot",
            description="A powerful and lightweight Discord bot built with discord.py that provides an advanced reminder system through slash commands.",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="✨ Features",
            value="• Advanced reminder system with complex time parsing\n"
                  "• Fun interaction commands\n"
                  "• SQLite database for persistence\n"
                  "• Slash command support\n"
                  "• Lightweight and efficient",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Technical Details",
            value="• Built with discord.py\n"
                  "• Python 3.10+\n"
                  "• SQLite database\n"
                  "• Background task scheduler",
            inline=False
        )
        
        embed.add_field(
            name="👨‍💻 Creator",
            value="**CrescendoFluffy**",
            inline=False
        )
        
        embed.set_footer(text="Use /help to see all available commands")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="Show help information and command examples")
    async def help(self, interaction: discord.Interaction):
        """Show comprehensive help with all commands and examples"""
        embed = discord.Embed(
            title="📚 Bot Commands & Help",
            description="Here are all the available commands with examples:",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        
        # Fun Commands
        embed.add_field(
            name="🎯 Fun Commands",
            value="**`/hi`** - Greet users\n"
                  "**`/bye`** - Say goodbye\n"
                  "**`/about`** - Learn about the bot\n"
                  "**`/help`** - Show this help message",
            inline=False
        )
        
        # Reminder Commands
        embed.add_field(
            name="⏰ Reminder System",
            value="**`/remind [time] [message] [delivery]`**\n"
                  "Set custom reminders with flexible time formats\n\n"
                  "**Examples:**\n"
                  "• `/remind 30s \"Check the oven\" dm`\n"
                  "• `/remind 2h \"Team meeting\" server`\n"
                  "• `/remind 1d \"Pay bills\" dm`\n"
                  "• `/remind \"1 year 2 months 3 weeks 4 days 5 hours 10 seconds\" \"Long term goal\" server`\n"
                  "• `/remind \"20-09-2025 14:30\" \"Important deadline\" dm`",
            inline=False
        )
        
        # Time Format Support
        embed.add_field(
            name="🕐 Time Format Support",
            value="**Simple units:** `30s`, `5m`, `2h`, `1d`, `1w`, `1mo`, `1y`\n"
                  "**Complex durations:** `\"1 year 2 months 3 weeks 4 days 5 hours 10 seconds\"`\n"
                  "**Mixed shorthand:** `2h 30m 20s`\n"
                  "**Absolute dates:** `20-09-2025 14:30`",
            inline=False
        )
        
        # Reminder Management
        embed.add_field(
            name="🔧 Reminder Management",
            value="**`/reminders`** - View all active reminders\n"
                  "**`/reminder_edit [id] [new time] [new message] [new delivery]`** - Modify existing reminders\n"
                  "**`/reminder_delete [id]`** - Remove reminders\n\n"
                  "**Examples:**\n"
                  "• `/reminders`\n"
                  "• `/reminder_edit 1 \"1h\" \"Updated reminder\" dm`\n"
                  "• `/reminder_delete 1`",
            inline=False
        )
        
        # Delivery Options
        embed.add_field(
            name="📱 Delivery Options",
            value="**`dm`** - Bot sends reminder directly to user\n"
                  "**`server`** - Bot posts reminder in channel and pings user",
            inline=False
        )
        
        embed.set_footer(text="Bot created by CrescendoFluffy • Use /about for more info")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(FunCommands(bot))
