import os
import discord
import requests
import json
import locale
import time
import datetime
from discord.ext import commands
from operator import itemgetter

k1 = os.environ['K1']
k2 = os.environ['K2']
k3 = os.environ['K3']

def format_odpowiedzi(tekst1=None, tekst2=None, tekst3=None, kolor=0xED4245):
    embed = discord.Embed(title = tekst1, colour=kolor)
    embed.add_field(name=tekst2, value=tekst3, inline=True)
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
    elif arg == "cena_skrzynki":
        link = 'https://api.torn.com/v2/market/'+str(arg1)+'/itemmarket?offset=4&key='+k1
    elif arg == "cena_pelna":
        link = 'https://api.torn.com/torn/?selections=items&key='+k1
    elif arg == "cena_przedmiot":
        link = 'https://api.torn.com/v2/market/'+str(arg1)+'/itemmarket?offset=4&key='+k1
    elif arg == "rw":
        link = 'https://api.torn.com/v2/faction/'+str(arg1)+'/rankedwars?key='+k1
    wynik = requests.get(link).json()
    return wynik

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "Command list:", colour=0xED4245)
    embed.add_field(name="!check_revive twr", value="Revive setting of TWR members.", inline=False)
    embed.add_field(name="!check_revive ID", value="Revive possibility of faction members, where ID is faction's ID", inline=False)
    embed.add_field(name="!check_price caches", value="Market price of RW caches", inline=False)
    embed.add_field(name="!check_price ItemName", value="Market price of any item. ItemName must match exactly name of item", inline=False)
    embed.add_field(name="!check_rw ID", value="History of last 20 Ranked Wars faction, where ID is faction's ID", inline=False)
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
async def check_price(ctx, zmienna):
    tresc = ""
    if zmienna == "caches":
        embed = discord.Embed(title = "Caches.", colour=0xED4245)
        for i in range(1118, 1123):
            wynik = zapytanie("cena_skrzynki", i)
            tresc = "Average price: " + str('${:,.0f}'.format(wynik['itemmarket']['item']['average_price'])) + "\nMarket price: " + str('${:,.0f}'.format(wynik['itemmarket']['listings'][int('0')]['price']))
            embed = dodaj_pole(embed, wynik['itemmarket']['item']['name'], tresc)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title = zmienna + ".", colour=0xED4245)
        wynik = zapytanie("cena_pelna")['items']
        for key in wynik:
            if wynik[key]['name']==zmienna:
                itemid = key
                pass
        if itemid != "":
            wynik = zapytanie("cena_przedmiot", itemid)
            tresc = "Average price: " + str('${:,.0f}'.format(wynik['itemmarket']['item']['average_price'])) + "\nMarket price: " + str('${:,.0f}'.format(wynik['itemmarket']['listings'][int('0')]['price']))
            embed = dodaj_pole(embed, "", tresc)
        else:
            embed = dodaj_pole(embed, "Error!", "Wrong item name")
        await ctx.send(embed=embed)

@bot.command()
async def check_rw(ctx, zmienna):
    i = 0
    wynik = zapytanie("frakcja_podstawowe", zmienna)
    embed = discord.Embed(title = wynik['basic']['name'] + "[" + str(wynik['basic']['id']) + "]", colour=0xED4245)
    wynik = zapytanie("rw", zmienna)['rankedwars']
    for poz in wynik:
        if i <= 20:
            
            start = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(poz['start']))
            end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(poz['end']))
            tresc = ""
            for key in poz['factions']:
                tresc = tresc + key['name']+"["+str(key['id'])+"] - "+str(key['score'])+"\n"
            embed = dodaj_pole(embed, start + " - " + end, tresc)
            i = i + 1
        else:
            pass
    await ctx.send(embed=embed)

@bot.command()
async def check_hosp(ctx, zmienna=None, zmienna2=None):
    iteracja = 0
    poprzednia = 0
    while iteracja < zmienna1:
        wynik = zapytanie("frakcja_zaawansowane", zmienna, zmienna1=1)
        czas = int(time.time())
        lista = []
        embedList = []
        for key in wynik['members']:
            if key['status']['state'] == "Hospital":
                nick = key['name'] + "[" + str(key['id']) + "]"
                status1 = key['status']['state']
                czas1 = key['status']['until']
                status2 = key['last_action']['status']
                czas2 = key['last_action']['timestamp']
                link = "https://www.torn.com/loader.php?sid=attack&user2ID=" + str(key['id'])
                level = key['level']
                if czas1-czas < 1200:
                    lista.append([nick, status1, czas1, status2, czas2, link, level])
        lista1 = sorted(lista, key=itemgetter(2), reverse=False)
        licznik = 0
        for poz in lista1:
            if licznik < 10:
                if poz[3] == "Offline":
                    kolor = 0xED4245
                elif poz[3] == "Idle":
                    kolor = 0x607d8b
                elif poz[3] == "Online":
                    kolor = 0x2ecc71
                embed = format_odpowiedzi(poz[0], str(datetime.timedelta(seconds=poz[2]-czas)), "Level " + str(poz[6]) + "\n[Attack page]("+poz[5]+")\n" + poz[3] + ", " + str(datetime.timedelta(seconds=czas-poz[4])), kolor)
                embedList.append(embed)
                licznik = licznik + 1
        try:
            await poprzednia.delete(delay = 0)
        except:
            pass
        poprzednia = await ctx.send(embeds=embedList)
        iteracja = iteracja + 1
        time.sleep(31)
bot.run(k3)

