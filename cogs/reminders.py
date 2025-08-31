

import logging
import re
import sqlite3
from datetime import datetime, timedelta

import dateparser
import discord
from discord import app_commands
from discord.ext import commands, tasks

logger = logging.getLogger(__name__)

class ReminderSystem(commands.Cog):
    """Reminder system with slash commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db_path = 'reminders.db'
        self.init_database()
        self.check_reminders.start()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                channel_id INTEGER,
                message TEXT NOT NULL,
                delivery_type TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def parse_time(self, time_str: str) -> datetime:
        """
        Parse time string into datetime object
        Supports: seconds(s), minutes(m), hours(h), days(d), weeks(w), months(mo), years(y)
        Also supports absolute dates: DD-MM-YYYY HH:MM
        """
        # Handle absolute date/time format (DD-MM-YYYY HH:MM)
        if re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', time_str):
            try:
                return datetime.strptime(time_str, '%d-%m-%Y %H:%M')
            except ValueError:
                raise ValueError("Invalid date format. Use DD-MM-YYYY HH:MM")
        
        # Handle relative time formats
        current_time = datetime.now()
        
        # Simple units
        if time_str.endswith(('s', 'm', 'h', 'd', 'w', 'mo', 'y')):
            return self._parse_simple_units(time_str, current_time)
        
        # Complex durations like "1 year 2 months 3 weeks 4 days 5 hours 10 seconds"
        return self._parse_complex_duration(time_str, current_time)
    
    def _parse_simple_units(self, time_str: str, current_time: datetime) -> datetime:
        """Parse simple time units like 30s, 5m, 2h, 1d, 1w, 1mo, 1y"""
        unit = time_str[-1]
        try:
            value = int(time_str[:-1])
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}")
        
        if unit == 's':
            return current_time + timedelta(seconds=value)
        elif unit == 'm':
            return current_time + timedelta(minutes=value)
        elif unit == 'h':
            return current_time + timedelta(hours=value)
        elif unit == 'd':
            return current_time + timedelta(days=value)
        elif unit == 'w':
            return current_time + timedelta(weeks=value)
        elif unit == 'o':  # months
            # Approximate months as 30 days
            return current_time + timedelta(days=value * 30)
        elif unit == 'y':
            # Approximate years as 365 days
            return current_time + timedelta(days=value * 365)
        else:
            raise ValueError(f"Unknown time unit: {unit}")
    
    def _parse_complex_duration(self, time_str: str, current_time: datetime) -> datetime:
        """Parse complex durations like '1 year 2 months 3 weeks 4 days 5 hours 10 seconds'"""
        # Try using dateparser for natural language parsing
        try:
            parsed = dateparser.parse(time_str, settings={'RELATIVE_BASE': current_time})
            if parsed:
                return parsed
        except:
            pass
        
        # Fallback to manual parsing
        total_seconds = 0
        
        # Extract numbers and units
        pattern = r'(\d+)\s*(year|month|week|day|hour|minute|second)s?'
        matches = re.findall(pattern, time_str.lower())
        
        for value, unit in matches:
            value = int(value)
            if unit == 'second':
                total_seconds += value
            elif unit == 'minute':
                total_seconds += value * 60
            elif unit == 'hour':
                total_seconds += value * 3600
            elif unit == 'day':
                total_seconds += value * 86400
            elif unit == 'week':
                total_seconds += value * 604800
            elif unit == 'month':
                total_seconds += value * 2592000  # ~30 days
            elif unit == 'year':
                total_seconds += value * 31536000  # ~365 days
        
        if total_seconds == 0:
            raise ValueError("Could not parse time format. Please use valid units.")
        
        return current_time + timedelta(seconds=total_seconds)
    
    @app_commands.command(name="remind", description="Set a reminder")
    @app_commands.describe(
        time="Time until reminder (e.g., 30s, 5m, 2h, 1d, 1w, 1mo, 1y, or '1 year 2 months 3 weeks 4 days 5 hours 10 seconds', or absolute date like '20-09-2025 14:30')",
        message="What to remind you about",
        delivery="How to deliver the reminder: 'dm' or 'server'"
    )
    async def remind(
        self, 
        interaction: discord.Interaction, 
        time: str, 
        message: str, 
        delivery: str
    ):
        """Set a new reminder"""
        try:
            # Parse the time
            reminder_time = self.parse_time(time)
            
            # Validate delivery type
            if delivery.lower() not in ['dm', 'server']:
                await interaction.response.send_message(
                    "❌ Invalid delivery type. Use 'dm' or 'server'.",
                    ephemeral=True
                )
                return
            
            # Store reminder in database
            reminder_id = self._store_reminder(
                user_id=interaction.user.id,
                channel_id=interaction.channel.id if delivery.lower() == 'server' else None,
                message=message,
                delivery_type=delivery.lower(),
                reminder_time=reminder_time
            )
            
            # Format time for display
            time_until = reminder_time - datetime.now()
            if time_until.total_seconds() < 60:
                time_display = f"{int(time_until.total_seconds())} seconds"
            elif time_until.total_seconds() < 3600:
                time_display = f"{int(time_until.total_seconds() // 60)} minutes"
            elif time_until.total_seconds() < 86400:
                time_display = f"{int(time_until.total_seconds() // 3600)} hours"
            else:
                time_display = f"{int(time_until.total_seconds() // 86400)} days"
            
            await interaction.response.send_message(
                f"✅ Reminder set! I'll remind you about '{message}' in {time_display}.\n"
                f"Reminder ID: {reminder_id}",
                ephemeral=True
            )
            
        except ValueError as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error setting reminder: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while setting the reminder.",
                ephemeral=True
            )
    
    def _store_reminder(self, user_id: int, channel_id: int, message: str, 
                        delivery_type: str, reminder_time: datetime) -> int:
        """Store reminder in database and return the ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert datetime to ISO format string for SQLite storage
        reminder_time_str = reminder_time.isoformat()
        
        cursor.execute('''
            INSERT INTO reminders (user_id, channel_id, message, delivery_type, reminder_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, channel_id, message, delivery_type, reminder_time_str))
        
        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return reminder_id
    
    @app_commands.command(name="reminders", description="List all your active reminders")
    async def reminders_list(self, interaction: discord.Interaction):
        """List all active reminders for the user"""
        await self._list_reminders(interaction)
    
    @app_commands.command(name="reminder_edit", description="Edit an existing reminder")
    @app_commands.describe(
        reminder_id="ID of the reminder to edit",
        new_time="New time for the reminder",
        new_message="New message for the reminder",
        new_delivery="New delivery method: 'dm' or 'server'"
    )
    async def reminder_edit(
        self,
        interaction: discord.Interaction,
        reminder_id: int,
        new_time: str,
        new_message: str,
        new_delivery: str
    ):
        """Edit an existing reminder"""
        await self._edit_reminder(interaction, reminder_id, new_time, new_message, new_delivery)
    
    @app_commands.command(name="reminder_delete", description="Delete a reminder")
    @app_commands.describe(
        reminder_id="ID of the reminder to delete"
    )
    async def reminder_delete(
        self,
        interaction: discord.Interaction,
        reminder_id: int
    ):
        """Delete a reminder"""
        await self._delete_reminder(interaction, reminder_id)
    
    async def _list_reminders(self, interaction: discord.Interaction):
        """List all active reminders for the user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        
        cursor.execute('''
            SELECT id, message, delivery_type, reminder_time, created_at
            FROM reminders 
            WHERE user_id = ? AND reminder_time > ?
            ORDER BY reminder_time ASC
        ''', (interaction.user.id, current_time))
        
        reminders = cursor.fetchall()
        conn.close()
        
        if not reminders:
            await interaction.response.send_message(
                "📝 You have no active reminders.",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="📝 Your Active Reminders",
            color=discord.Color.blue()
        )
        
        for reminder_id, message, delivery_type, reminder_time, created_at in reminders:
            try:
                reminder_dt = datetime.fromisoformat(reminder_time)
                time_until = reminder_dt - datetime.now()
                
                if time_until.total_seconds() < 60:
                    time_display = f"{int(time_until.total_seconds())} seconds"
                elif time_until.total_seconds() < 3600:
                    time_display = f"{int(time_until.total_seconds() // 60)} minutes"
                elif time_until.total_seconds() < 86400:
                    time_display = f"{int(time_until.total_seconds() // 3600)} hours"
                else:
                    time_display = f"{int(time_until.total_seconds() // 86400)} days"
                
                embed.add_field(
                    name=f"ID: {reminder_id}",
                    value=f"**Message:** {message}\n"
                          f"**Delivery:** {delivery_type}\n"
                          f"**Time until:** {time_display}\n"
                          f"**Created:** {created_at}",
                    inline=False
                )
            except Exception as e:
                logger.error(f"Error processing reminder {reminder_id}: {e}")
                continue
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _edit_reminder(self, interaction: discord.Interaction, reminder_id: int, 
                            new_time: str, new_message: str, new_delivery: str):
        """Edit an existing reminder"""
        try:
            # Parse new time
            new_reminder_time = self.parse_time(new_time)
            
            # Validate delivery type
            if new_delivery.lower() not in ['dm', 'server']:
                await interaction.response.send_message(
                    "❌ Invalid delivery type. Use 'dm' or 'server'.",
                    ephemeral=True
                )
                return
            
            # Update reminder in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            new_reminder_time_str = new_reminder_time.isoformat()
            
            cursor.execute('''
                UPDATE reminders 
                SET message = ?, delivery_type = ?, reminder_time = ?, channel_id = ?
                WHERE id = ? AND user_id = ?
            ''', (
                new_message, 
                new_delivery.lower(), 
                new_reminder_time_str,
                interaction.channel.id if new_delivery.lower() == 'server' else None,
                reminder_id, 
                interaction.user.id
            ))
            
            if cursor.rowcount == 0:
                conn.close()
                await interaction.response.send_message(
                    "❌ Reminder not found or you don't have permission to edit it.",
                    ephemeral=True
                )
                return
            
            conn.commit()
            conn.close()
            
            await interaction.response.send_message(
                f"✅ Reminder {reminder_id} updated successfully!",
                ephemeral=True
            )
            
        except ValueError as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error editing reminder: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while editing the reminder.",
                ephemeral=True
            )
    
    async def _delete_reminder(self, interaction: discord.Interaction, reminder_id: int):
        """Delete a reminder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM reminders 
            WHERE id = ? AND user_id = ?
        ''', (reminder_id, interaction.user.id))
        
        if cursor.rowcount == 0:
            conn.close()
            await interaction.response.send_message(
                "❌ Reminder not found or you don't have permission to delete it.",
                ephemeral=True
            )
            return
        
        conn.commit()
        conn.close()
        
        await interaction.response.send_message(
            f"✅ Reminder {reminder_id} deleted successfully!",
            ephemeral=True
        )
    
    @tasks.loop(seconds=30)
    async def check_reminders(self):
        """Check for due reminders every 30 seconds"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            current_time = datetime.now().isoformat()
            
            # Get all due reminders
            cursor.execute('''
                SELECT id, user_id, channel_id, message, delivery_type
                FROM reminders 
                WHERE reminder_time <= ?
            ''', (current_time,))
            
            due_reminders = cursor.fetchall()
            
            for reminder_id, user_id, channel_id, message, delivery_type in due_reminders:
                await self._send_reminder(reminder_id, user_id, channel_id, message, delivery_type)
                
                # Delete the sent reminder
                cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking reminders: {e}")
    
    async def _send_reminder(self, reminder_id: int, user_id: int, channel_id: int, 
                            message: str, delivery_type: str):
        """Send a reminder to the user"""
        try:
            user = self.bot.get_user(user_id)
            if not user:
                logger.warning(f"User {user_id} not found for reminder {reminder_id}")
                return
            
            if delivery_type == "dm":
                # Send DM
                try:
                    embed = discord.Embed(
                        title="⏰ Reminder!",
                        description=message,
                        color=discord.Color.green(),
                        timestamp=datetime.now()
                    )
                    embed.set_footer(text=f"Reminder ID: {reminder_id}")
                    await user.send(embed=embed)
                except discord.Forbidden:
                    logger.warning(f"Cannot send DM to user {user_id}")
            
            elif delivery_type == "server":
                # Send in channel and ping user
                if channel_id:
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        embed = discord.Embed(
                            title="⏰ Reminder!",
                            description=message,
                            color=discord.Color.green(),
                            timestamp=datetime.now()
                        )
                        embed.set_footer(text=f"Reminder ID: {reminder_id}")
                        await channel.send(f"{user.mention}", embed=embed)
                    else:
                        logger.warning(f"Channel {channel_id} not found for reminder {reminder_id}")
            
        except Exception as e:
            logger.error(f"Error sending reminder {reminder_id}: {e}")
    
    @check_reminders.before_loop
    async def before_check_reminders(self):
        """Wait until bot is ready before starting the reminder checker"""
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(ReminderSystem(bot))
