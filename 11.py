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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS testbot (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nume VARCHAR(50) UNIQUE,
        puncte INT
    )
""")
cnx.commit()

@bot.event
async def on_ready():
    print(f'Conectat ca {bot.user.name}')

@bot.command()
async def register(ctx):
    user = ctx.author

    if user.id is not None:
        cursor.execute('SELECT id FROM testbot WHERE id = %s', (user.id,))
        existing_rows = cursor.fetchall()

        if existing_rows:
            await ctx.send(f'{user.name}, esti deja inregistrat! Nu este necesar sa te inregistrezi din nou.')
        else:
            cursor.execute('INSERT INTO testbot (puncte) VALUES (0)')
            cnx.commit()
            await ctx.send(f'{user.name} a fost inregistrat cu succes!')
    else:
        await ctx.send('ID-ul utilizatorului este invalid.')
@bot.command()
async def points(ctx):
    user = ctx.author
    cursor.execute("SELECT puncte FROM testbot WHERE id = %s", (user.id,))
    row = cursor.fetchone()

    if row is not None:
        await ctx.send(f'Jucatorul *{user.name}* are ```{row[0]}``` puncte!')
    else:
        await ctx.send(f'Nu am putut gasi jucatorul {user.mention} in baza de date.')
        
@bot.command()
async def give(ctx, user: discord.Member, points: int):
    cursor.execute("SELECT id FROM testbot WHERE id = %s", (user.id,))
    row = cursor.fetchone()

    if row is not None:
        cursor.execute("SELECT puncte FROM testbot WHERE id = %s", (user.id,))
        puncte_vechi = cursor.fetchone()[0]
        puncte_noi = puncte_vechi + points

        cursor.execute("UPDATE testbot SET puncte = %s WHERE id = %s", (puncte_noi, user.id))
        cnx.commit()
        await ctx.send(f'Punctele pentru {user.mention} au fost actualizate la `{puncte_noi}`!')
    else:
        await ctx.send(f'Nu am putut gasi jucatorul {user.mention} in baza de date.')
        

@bot.event
async def on_bot_close():
    cursor.close()
    cnx.close()
    
bot.run('MTE5NTA5MjAwNjM2NDUzMjc5Ng.GsoX4T.ClBOLWX7YhXHFjRNcfHYyrALfyySvr2C8DXbo4')
