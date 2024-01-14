import discord
from discord.ext import commands
import mysql.connector


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

cursor.execute("CREATE TABLE IF NOT EXISTS testbot (id BIGINT, nume VARCHAR(50), puncte INT)")
cnx.commit()

@bot.event
async def on_ready():
    print(f'Conectat ca {bot.user.name}')

    
@bot.command()
async def register(ctx):
    user = ctx.author

    cursor.execute('SELECT nume FROM testbot WHERE nume = %s', (user.name,))
    existing_rows = cursor.fetchall()

    if existing_rows:
        await ctx.send(f'{user.name}, esti deja inregistrat! Nu este necesar sa te inregistrezi din nou.')
    else:
        cursor.execute('INSERT INTO testbot (id, nume, puncte) VALUES (%s, %s, 0)', (user.id, user.name))
        cnx.commit()
        await ctx.send(f'{user.name} a fost inregistrat cu succes!')
        
@bot.command()
async def points(ctx):
    user = ctx.author
    cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", (user.name,))
    row = cursor.fetchone()

    if row is not None:
        await ctx.send(f'Jucatorul *{user.name}* are ```{row[0]}``` puncte!')
    else:
        await ctx.send(f'Nu am putut gasi jucatorul {user.mention} in baza de date.')

@bot.command()
async def give(ctx, user: discord.Member, points: int):
    cursor.execute("SELECT puncte FROM testbot WHERE nume = %s", (user.name,))
    row = cursor.fetchone()

    if row is not None:
        puncte_vechi = row[0]
        puncte_noi = puncte_vechi + points

        cursor.execute("UPDATE testbot SET puncte = %s WHERE nume = %s", (puncte_noi, user.name))
        cnx.commit()
        await ctx.send(f'Punctele pentru {user.mention} au fost actualizate la `{puncte_noi}`!')
    else:
        await ctx.send(f'Nu am putut gasi jucatorul {user.mention} in baza de date.')
        
@bot.event
async def on_bot_close():
    cursor.close()
    cnx.close()

bot.run('MTE5NTA5MjAwNjM2NDUzMjc5Ng.GsoX4T.ClBOLWX7YhXHFjRNcfHYyrALfyySvr2C8DXbo4')
