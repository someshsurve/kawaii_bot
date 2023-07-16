import discord
import datetime
import sqlite3
from discord.ext import commands

# for storing data creating db name kawaii
conn = sqlite3.connect('kawaii.db')
cursor = conn.cursor()

# creating tables named users and referals with one-to-one relation
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    points INTEGER DEFAULT 0
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS referals (
                    username TEXT,
                    referred_by TEXT,
                    FOREIGN KEY (username) REFERENCES users(username)
                )''')
conn.commit()

# giving specific event permission to bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event  # syncing all the commands at the startup of the bot.
async def on_ready():
    print("bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.command()  # bot command for getting all members and their roles.
async def members_data(discord):
    discord_guild = discord.guild
    discord_members = discord_guild.members
    members_list = []

    for member in discord_members:
        roles = [role.name for role in member.roles]
        members_list.append(f"Name: {member.name}\nRoles: {', '.join(roles)}\n")

    members_data = '\n'.join(members_list)
    await discord.send(f"Here is the list of server members for {discord.guild.name}:\n\n{members_data}")


@bot.command()  # bot command for counting total messages in past 12 hours.
async def messages_counter(discord):
    discord_guild = discord.guild
    current_time = datetime.datetime.utcnow()
    duration = datetime.timedelta(hours=12)
    messages_count = 0

    # including only messages from real users not the ones from bot.
    for channel in discord_guild.text_channels:
        async for message in channel.history(limit=None, after=current_time - duration):
            if message.author.bot:
                continue
            messages_count += 1

    await discord.send(f"Hey {discord.author.name}! \nTotal messages sent in the last 12 hours are: {messages_count}")


@bot.tree.command(name="help", description="get help related to commands")
async def help(interaction: discord.Interaction):
    commands = bot.tree.get_commands()
    response = "Prefix based commands:\n" \
               "1. $members_data : to get all members names and their roles.\n" \
               "2. $messages_counter : to get total count of messages sent in last 12 hours.\n\n" \
               "Available slash commands:\n"

    for command in commands:
        response += f"/{command.name}: {command.description}\n"

    await interaction.response.send_message(f"hi {interaction.user.mention}!, how are you? \n"
                                            f"{response}", ephemeral=True)


@bot.tree.command(name="thanks", description="say thanks to someone")
async def thanks(interaction: discord.Interaction, user: discord.User, *, message: str):
    username = user.name
    cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
    cursor.execute('UPDATE users SET points = points + 1 WHERE username = ?', (username,))
    cursor.execute('INSERT OR IGNORE INTO referals (referred_by, username) VALUES (?,?)',
                   (interaction.user.name, username,))

    conn.commit()
    await interaction.response.send_message(f"Hey {interaction.user.mention}! "
                                            f"your endorsement for {user.mention} is recorded.", ephemeral=True)
    channel = interaction.channel
    await channel.send(f"Congrats {user.mention},"
                       f"\nyou have received greetings from {interaction.user.mention}"
                       f"\n\nmessage:```{message}```")


@bot.tree.command(name="endorsement_points", description="Get endorsement points of a specific user")
async def endorsement_points(interaction: discord.Interaction, user: discord.User):
    # Get the mentioned user's username
    username = user.name

    # Retrieve the points for the mentioned user from the database
    cursor.execute('SELECT points FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    cursor.execute('SELECT DISTINCT referred_by FROM referals WHERE username = ?', (username,))
    all_referals = cursor.fetchall()

    if result:
        points = result[0]
        referals = ', '.join([n[0] for n in all_referals])
        await interaction.response.send_message(f'{username} has received {points} endorsement points from users below.'
                                                f' \n {str(referals)}', ephemeral=True)
    else:
        await interaction.response.send_message(f'{username} has no points yet.', ephemeral=True)


@bot.tree.command(name="endorsements", description="Get all endorsement data")
async def endorsements(interaction: discord.Interaction):
    cursor.execute('SELECT username, points FROM users ORDER BY points DESC')
    results = cursor.fetchall()

    if results:
        list = "here is all endorsement data" \
               "```Users                Points\n\n"
        for row in results:
            username, points = row
            list += f"{username:<20} {points}\n"
        list += "```"
        await interaction.response.send_message(list, ephemeral=True)

    else:
        await interaction.response.send_message(f'no endorsement present', ephemeral=True)


bot.run('MTEyOTI5OTIwMDA4MTkyODI4Mg.GW2V5Z.njBau_i_0U2L4l36L0OuYOmJSoGePhaOkGOvHA')
