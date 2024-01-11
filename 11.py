import discord
from discord.ext import commands
import mysql.connector

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

config = {
    'host': '93.115.101.23',
    'user': 'u521_FSfdz1guUF',
    'password': 'jg9sfLwntt@StfB+tNG^7QRR',
    'database': 's521_webProject',
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS testbot (id BIGINT, nume VARCHAR(50), puncte INT)")
cnx.commit()

@bot.event
async def on_ready():
    print(f'Conectat ca {bot.user.name}')

@bot.command()
async def register(ctx):
    user = ctx.author

    cursor.execute('SELECT nume FROM testbot WHERE nume = %s', (user.name,))
    rows = cursor.fetchall()
    
    for nume in rows:
        if ctx.author.name == nume[0]:
            await ctx.send(f'{user.name}, esti deja inregistrat! Nu este necesar sa te inregistrezi din nou.')
        else:
            cursor.execute('INSERT INTO testbot (id, nume, puncte) VALUES (%s, %s, 0)', (user.id, user.name))
            cnx.commit()
            await ctx.send(f'{user.name} a fost inregistrat cu succes!')

@bot.command()
async def points(ctx):
    user = ctx.author
    cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", (user.name,))
    rows = cursor.fetchall()

    for puncte in rows:
        await ctx.send(f'Jucatorul *{user.name}* are ```{puncte[0]}``` puncte!')

@bot.command()
async def give(ctx, user: discord.Member, points: int):
    cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", ( user.name,))
    row = cursor.fetchone()
    for puncte in row:
        punctenoi = puncte + points

        cursor.execute("UPDATE testbot SET puncte = %s WHERE nume = %s", (punctenoi, user.name))
        cnx.commit()
        await ctx.send(f'Punctele pentru {user.mention} au fost actualizate la `{punctenoi}`!')

@bot.event
async def on_bot_close():
    cursor.close()
    cnx.close()

bot.run('MTE5NDczOTE4MjU2ODk5NjkwNA.G2iUFc._YshhVl_MMSu_gn3W3TlqowfpVBzaDIN-XG2wU')
