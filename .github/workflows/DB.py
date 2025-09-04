import os
import discord
import requests
import json
import locale
from discord.ext import commands

k1 = os.environ['K1']
k2 = os.environ['K2']
k3 = os.environ['K3']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

@bot.command()
async def help(arg):
    text = "!check_revives own  -  check revive settings of our members \n"
    text = text + "!check_revives 'ID'  -  check who is revivable by faction id without ' '\n"
    text = text + "!check_price caches  -  check average and lowest prices of caches on market \n"
    text = text + "!check_price 'Item Name'  -  check average and lowest prices of 'Item Name', name must match in game name of item \n"
    await arg.send(text)

@bot.command()
async def check_revives(ctx, arg):
    if arg == "own":
        lista1 = "Everyone:" + "\n\n"
        lista2 = "Friends & faction:" + "\n\n"
        link = 'https://api.torn.com/v2/faction/members?striptags=true&key='+k1
        zapytanie = requests.get(link)
        wynik = zapytanie.json()
        for pozycja in wynik['members']:
            if pozycja['revive_setting']=="Everyone":
                lista1 = lista1 + pozycja['name'] + "[" + str(pozycja['id']) + "]" + "\n"
        for pozycja in wynik['members']:
            if pozycja['revive_setting']=="Friends & faction":
                lista2 = lista2 + pozycja['name'] + "[" + str(pozycja['id']) + "]" + "\n"
        await ctx.send(lista1 + "\n" + lista2)
    else:
        link = 'https://api.torn.com/v2/faction/'+str(arg)+'/basic?key='+k1
        zapytanie = requests.get(link)
        wynik = zapytanie.json()
        lista1 = "Revivable members of " + wynik['basic']['name'] + "[" + str(wynik['basic']['id']) + "]: \n\n"
        link = 'https://api.torn.com/v2/faction/'+str(arg)+'/members?striptags=true&key='+k2
        zapytanie = requests.get(link)
        wynik = zapytanie.json()
        for pozycja in wynik['members']:
            if str(pozycja['is_revivable'])=="True":
                lista1 = lista1 + pozycja['name'] + "[" + str(pozycja['id']) + "]" + "\n"
        await ctx.send(lista1)

@bot.command()
async def check_price(ctx, arg):
    if arg == "caches":
        lista1 = "Cache prices: "
        lista2 = "Friends & faction:"
        for i in range(1118, 1123):
            zapytanie = requests.get('https://api.torn.com/v2/market/'+str(i)+'/itemmarket?offset=4&key='+k1)
            wynik = zapytanie.json()
            lista1 = lista1 + "\n\n" + wynik['itemmarket']['item']['name'] + " average price is: " + str('${:,.0f}'.format(wynik['itemmarket']['item']['average_price'])) + "\nCheapest on itemmarket is: " + str('${:,.0f}'.format(wynik['itemmarket']['listings'][int('0')]['price']))
        await ctx.send(lista1)
    else:
        lista1 = ""
        itemid = ""
        zapytanie = requests.get('https://api.torn.com/torn/?selections=items&key='+k1)
        wynik = zapytanie.json()
        wynik = wynik['items']
        for key in wynik:
            wynik[key]['name']
            if wynik[key]['name']==arg:
                itemid = key
                pass
        if itemid != "":
            zapytanie = requests.get('https://api.torn.com/v2/market/'+str(itemid)+'/itemmarket?offset=4&key='+k1)
            wynik = zapytanie.json()
            lista1 = wynik['itemmarket']['item']['name'] + " average price is: " + str('${:,.0f}'.format(wynik['itemmarket']['item']['average_price'])) + "\nCheapest on itemmarket is: " + str('${:,.0f}'.format(wynik['itemmarket']['listings'][int('0')]['price']))
        else:
            lista1 = "Wrong item name"
        await ctx.send(lista1)

@bot.command()
async def check_rw(ctx, arg):
    link = 'https://api.torn.com/v2/faction/'+str(arg)+'/basic?key='+k1
    zapytanie = requests.get(link)
    wynik = zapytanie.json()
    lista1 = wynik['basic']['name'] + "[" + str(wynik['basic']['id']) + "] \n\n"
    zapytanie = requests.get('https://api.torn.com/v2/faction/'+str(arg)+'/rankedwars?key='+k1)
    wynik = zapytanie.json()
    wynik = wynik['rankedwars']
    for poz in wynik:
        pass
    retStr = str("""```css\nblablabla```""")
    embed = discord.Embed(title=lista1)
    embed.add_field(name="Ranked wars history:",value=retStr)
    await ctx.send(embed=embed)

@bot.command()
async def check_health(ctx, arg1=None, arg2=None):
    zapytanie = requests.get('https://api.torn.com/v2/faction/'+str(arg1)+'/basic?key='+k1)
    wynik = zapytanie.json()
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    await ctx.send()
    
bot.run(k3)
