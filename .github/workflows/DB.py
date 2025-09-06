import os
import discord
import requests
import json
import locale
from discord.ext import commands

k1 = os.environ['K1']
k2 = os.environ['K2']
k3 = os.environ['K3']

def format_odpowiedzi(tekst1=None, tekst2=None, tekst3=None):
    retStr = str(tekst3)
    embed = discord.Embed(title = tekst1, colour=0xED4245)
    embed.add_field(name=tekst2, value=retStr, inline=True)
    return embed

def dodaj_pole(embed=None, tekst2=None, tekst3=None):
    retStr = str(tekst3)
    embed.add_field(name=tekst2, value=retStr, inline=True)
    return embed

def zapytanie(arg, arg1=None):
    if arg == "frakcja_zaawansowane":
        link = 'https://api.torn.com/v2/faction/'+str(arg1)+'/members?striptags=true&key='+k2
    elif arg == "frakcja_podstawowe":
        link = 'https://api.torn.com/v2/faction/'+str(arg1)+'/basic?key='+k1
    wynik = requests.get(link).json()
    return wynik

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "Command list:", colour=0xED4245)
    embed.add_field(name="!check_revive twr", value="Revive setting of TWR members.", inline=True)
    embed.add_field(name="!check_revive ID", value="Revive setting of other faction members, where ID is faction's ID", inline=True)
    embed.add_field(name="!check_price caches", value="Market price of RW caches", inline=True)
    embed.add_field(name="!check_price ItemName", value="Market price of any item. ItemName must match exactly name of item", inline=True)
    embed.add_field(name="!check_rw ID", value="History of last Ranked Wars of other faction, where ID is faction's ID", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def check_revive(ctx, zmienna=None):
    tresc = ''
    if zmienna == None:
        tresc = "Please provide argument, it can be either faction ID or word 'twr'. Use !help for more commands."
        embed = format_odpowiedzi("Error !", "No argument specified.", tresc)
        await ctx.send(embed=embed)
    elif zmienna.isnumeric() != True and zmienna != "twr":
        nazwa = "Error !"
        naglowek = "Wrong argument."
        tresc = "Please provide proper argument, it can be either faction ID or word 'twr'. Use !help for more commands."
        embed = format_odpowiedzi(nazwa, naglowek, tresc)
        await ctx.send(embed=embed)
    elif zmienna == "twr":
        wynik = zapytanie("frakcja_zaawansowane", "13737")
        for pozycja in wynik['members']:
            if pozycja['revive_setting']=="Everyone":
                tresc = tresc + pozycja['name'] + "[" + str(pozycja['id']) + "]" + "\n"
        embed = format_odpowiedzi("Revivable members of TWR", "Everyone:", tresc)
        tresc = ''
        for pozycja in wynik['members']:
            if pozycja['revive_setting']=="Friends & faction":
                tresc = tresc + pozycja['name'] + "[" + str(pozycja['id']) + "]" + "\n"
        embed = dodaj_pole(embed, "Friends & faction:", tresc)
        await ctx.send(embed=embed)
    else:
        wynik_podst = zapytanie("frakcja_podstawowe", zmienna)
        wynik = zapytanie("frakcja_zaawansowane", zmienna)
        for pozycja in wynik['members']:
            if str(pozycja['is_revivable'])=="True":
                tresc = tresc + pozycja['name'] + "[" + str(pozycja['id']) + "]\n"
        embed = format_odpowiedzi("Revivable members of " + wynik_podst['basic']['name'] + "[" + str(wynik_podst['basic']['id']) + "]", "List:", tresc)
        await ctx.send(embed=embed)

@bot.command()
async def check_price(ctx, arg):
    if arg == "caches":
        lista1 = "Cache prices: "
        lista2 = "Friends & faction:"
        for i in range(1118, 1123):
            apytanie = requests.get('https://api.torn.com/v2/market/'+str(i)+'/itemmarket?offset=4&key='+k1)
            wynik = apytanie.json()
            lista1 = lista1 + "\n\n" + wynik['itemmarket']['item']['name'] + " average price is: " + str('${:,.0f}'.format(wynik['itemmarket']['item']['average_price'])) + "\nCheapest on itemmarket is: " + str('${:,.0f}'.format(wynik['itemmarket']['listings'][int('0')]['price']))
        await ctx.send(lista1)
    else:
        lista1 = ""
        itemid = ""
        apytanie = requests.get('https://api.torn.com/torn/?selections=items&key='+k1)
        wynik = apytanie.json()
        wynik = wynik['items']
        for key in wynik:
            wynik[key]['name']
            if wynik[key]['name']==arg:
                itemid = key
                pass
        if itemid != "":
            apytanie = requests.get('https://api.torn.com/v2/market/'+str(itemid)+'/itemmarket?offset=4&key='+k1)
            wynik = apytanie.json()
            lista1 = wynik['itemmarket']['item']['name'] + " average price is: " + str('${:,.0f}'.format(wynik['itemmarket']['item']['average_price'])) + "\nCheapest on itemmarket is: " + str('${:,.0f}'.format(wynik['itemmarket']['listings'][int('0')]['price']))
        else:
            lista1 = "Wrong item name"
        await ctx.send(lista1)

@bot.command()
async def check_rw(ctx, arg):
    link = 'https://api.torn.com/v2/faction/'+str(arg)+'/basic?key='+k1
    apytanie = requests.get(link)
    wynik = apytanie.json()
    lista1 = wynik['basic']['name'] + "[" + str(wynik['basic']['id']) + "] \n\n"
    apytanie = requests.get('https://api.torn.com/v2/faction/'+str(arg)+'/rankedwars?key='+k1)
    wynik = apytanie.json()
    wynik = wynik['rankedwars']
    for poz in wynik:
        pass
    retStr = str("""```css\nblablabla```""")
    embed = discord.Embed(title=lista1)
    embed.add_field(name="Ranked wars history:",value=retStr)
    await ctx.send(embed=embed)

@bot.command()
async def check_health(ctx, arg1=None, arg2=None):
    apytanie = requests.get('https://api.torn.com/v2/faction/'+str(arg1)+'/basic?key='+k1)
    wynik = apytanie.json()
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    await ctx.send()
    
bot.run(k3)
