import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='🌵 Cactus Bot'))
    print(f'Conectado como {bot.user}')

# Comandos de Moderación
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} ha sido expulsado. Razón: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} ha sido baneado. Razón: {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Se han eliminado {amount} mensajes.', delete_after=5)

# Comandos de Economía
economy = {}

@bot.command()
async def balance(ctx):
    user = ctx.author.id
    economy.setdefault(user, 100)
    await ctx.send(f'{ctx.author.mention}, tu saldo es de {economy[user]} monedas.')

@bot.command()
async def work(ctx):
    user = ctx.author.id
    earnings = random.randint(10, 50)
    economy[user] = economy.get(user, 100) + earnings
    await ctx.send(f'{ctx.author.mention}, has trabajado y ganado {earnings} monedas.')

@bot.command()
async def bet(ctx, amount: int):
    user = ctx.author.id
    if amount > economy.get(user, 100):
        await ctx.send('No tienes suficientes monedas.')
        return
    if random.choice([True, False]):
        economy[user] += amount
        await ctx.send(f'{ctx.author.mention}, ganaste {amount} monedas!')
    else:
        economy[user] -= amount
        await ctx.send(f'{ctx.author.mention}, perdiste {amount} monedas.')

# Minijuego: Adivina el número
@bot.command()
async def adivina(ctx):
    numero = random.randint(1, 10)
    await ctx.send('He pensado en un número del 1 al 10, ¡adivina cuál es!')
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        while True:
            mensaje = await bot.wait_for('message', check=check, timeout=15)
            intento = int(mensaje.content)
            if intento == numero:
                await ctx.send(f'¡Correcto! Era el {numero}.')
                break
            else:
                await ctx.send('¡Incorrecto! Intenta de nuevo.')
    except asyncio.TimeoutError:
        await ctx.send(f'Se acabó el tiempo. El número era {numero}.')

bot.run('MTM1MDU1NTYzODg5MTE1MTQwMA.Gv7F40.YhcPb1HqnAdD_iT-I-mNBylBiauxQvsMhTfg-0')
