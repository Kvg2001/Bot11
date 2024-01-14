import discord
from discord.ext import commands
import mysql.connector
from datetime import datetime, timedelta
import humanize

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

config = {
    'host': '93.115.101.23',
    'user': 'u521_FSfdz1guUF',
    'password': 'jg9sfLwntt@StfB+tNG^7QRR',
    'database': 's521_webProject',
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS testbot (
        nume VARCHAR(50) UNIQUE,
        puncte INT
    )
""")
cnx.commit()

giveaway_data = {}


@bot.event
async def on_ready():
    print(f'Connected as {bot.user.name}')


@bot.command()
async def register(ctx):
    user = ctx.author

    cursor.execute('SELECT nume FROM testbot WHERE nume = %s', (user.name,))
    existing_rows = cursor.fetchall()

    if existing_rows:
        await ctx.send(f'{user.name}, you are already registered! No need to register again.')
    else:
        cursor.execute('INSERT INTO testbot (nume, puncte) VALUES (%s, 0)', (user.name,))
        cnx.commit()
        await ctx.send(f'{user.name} has been registered successfully!')


@bot.command()
async def points(ctx):
    user = ctx.author
    cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", (user.name,))
    row = cursor.fetchone()

    if row is not None:
        await ctx.send(f'Player *{user.name}* has ```{row[0]}``` points!')
    else:
        await ctx.send(f'Couldn\'t find the player {user.mention} in the database.')


@bot.command()
@commands.has_permissions(administrator=True)
async def setpoints(ctx, user: discord.Member, points: int):
    cursor.execute("UPDATE testbot SET puncte = %s WHERE nume = %s", (points, user.name))
    cnx.commit()
    await ctx.send(f'Points for {user.mention} have been set to `{points}`!')


@bot.command()
@commands.has_permissions(administrator=True)
async def give(ctx, user: discord.Member, points: int):
    cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", (user.name,))
    row = cursor.fetchone()

    if row is not None:
        old_points = row[0]
        new_points = old_points + points

        cursor.execute("UPDATE testbot SET puncte = %s WHERE nume = %s", (new_points, user.name))
        cnx.commit()
        await ctx.send(f'Points for {user.mention} have been updated to `{new_points}`!')
    else:
        await ctx.send(f'Couldn\'t find the player {user.mention} in the database.')


@bot.command()
async def giveaway(ctx, duration: str, winners: int, entry_fee: int, prize: int, description: str):
    user = ctx.author

    if duration[-1] == 'm':
       duration_seconds = int(duration[:-1]) * 60
    elif duration[-1] == 'h':
       duration_seconds = int(duration[:-1]) * 3600
    else:
       await ctx.send("Invalid duration format. Use 'm' for minutes or 'h' for hours.")
    return

    end_time = datetime.utcnow() + timedelta(seconds=duration_seconds)

    embed = discord.Embed(
        title="Giveaway",
        description=f"{description}\n\nReact with :tada: to enter!\n\n**Prize:** {prize} points\n**Winners:** {winners}\n**Entry Fee:** {entry_fee} points\n**Ends In:** {humanize.naturaltime(end_time)}",
        color=0x00FF00
    )
    embed.set_footer(text=f"Hosted by {user.name}")

    message = await ctx.send(embed=embed)
    await message.add_reaction(":tada:")

    giveaway_data[message.id] = {
        'host': user.id,
        'winners': winners,
        'entry_fee': entry_fee,
        'prize': prize,
        'end_time': end_time,
        'participants': []
    }


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message_id = reaction.message.id
    if message_id in giveaway_data:
        giveaway_info = giveaway_data[message_id]

        if user.id != giveaway_info['host']:
            entry_fee = giveaway_info['entry_fee']
            prize = giveaway_info['prize']

            cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", (user.name,))
            row = cursor.fetchone()

            if row is not None and row[0] >= entry_fee:
                new_points = row[0] - entry_fee
                cursor.execute("UPDATE testbot SET puncte = %s WHERE nume = %s", (new_points, user.name))
                cnx.commit()

                giveaway_info['participants'].append(user.id)

                await user.send(f"You've successfully entered the giveaway! You paid {entry_fee} points as an entry fee.")
            else:
                await user.send(f"Insufficient points to enter the giveaway. You need {entry_fee} points.")

            await reaction.remove(user)

@bot.event
async def on_bot_close():
    cursor.close()
    cnx.close()


bot.run('MTE5NTA5MjAwNjM2NDUzMjc5Ng.GsoX4T.ClBOLWX7YhXHFjRNcfHYyrALfyySvr2C8DXbo4')
