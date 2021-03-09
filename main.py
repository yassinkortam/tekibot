import discord
import os
import random
from datetime import datetime
from replit import db
from discord.ext import commands, tasks
from keep_alive import keep_alive
bot = commands.Bot(command_prefix='pls ')
now = datetime.now()
month = now.month
day = now.day
admins = [588483247256895500]


#Lets us know the bot is active

@bot.event
async def on_ready():
  print("%s has entered the chat" % (bot.user))

#________MAINTENANCE FEATURES________

#Makes me rich

@bot.command()
async def make_rich(ctx):
  user_data = db[ctx.author.id]
  money = user_data['money']
  xp = user_data['xp']
  if ctx.author.id in admins:
    money += 1000000000000
    xp += 1000000
    user_data['money'] = money
    user_data['xp'] = xp
    db[ctx.author.id] = user_data
    await ctx.send("Aight boss, you richer than Elon Musk now.")
  else:
    await ctx.send("Go away normie you trippin.")

#Initializes the necessary database entries 

@bot.command()
async def join_teki(ctx):
  user_data = {}
  if ctx.author.id not in db:
    user_data["name"] = ctx.author.name
    user_data["confirm_token"] = 0
    user_data["money"] = 0
    user_data["xp"] = 100
    user_data["items"] = []
    db[ctx.author.id] = user_data
    await ctx.send("Your account is all set")
    await ctx.send(file=discord.File('reactions/doge_happy.jpeg'))
  else:
    await ctx.send("You already have an account set up.")

#Prints all the data in the database (ADMIN ONLY)

@bot.command()
async def print_db(ctx):
  if ctx.author.id in admins:
    db_ref = {}
    for x in db:
      db_ref[x] = db[x]
    await ctx.send(db_ref)
  else:
    await ctx.send("You don't have permission to see everyone's birthday, thats creepy.")
    await ctx.send(file=discord.File('reactions/creepy.gif'))

#Allows the admin to clear things from the database

@bot.command()
async def clear_db(ctx):
  user_data = db[ctx.author.id]
  if ctx.author.id in admins and user_data["confirm_token"] == 1:
    user_data["confirm_token"] = 0
    for x in db:
      del db[x]
    await ctx.send("Database cleared")
  elif ctx.author.id in admins:
    user_data["confirm_token"] = 1
    db[ctx.author.id] = user_data
    await ctx.send("Ask again to comnfirm boss.")
  else:
    await ctx.send("Permission Denied")
    await ctx.send(file=discord.File('reactions/creepy.gif'))


#Allows users to delete their account

@bot.command()
async def del_account(ctx):
  if ctx.author.id in db:
    del db[ctx.author.id]
    await ctx.send(file=discord.File('reactions/sad_doge.gif'))
    await ctx.send("I deleted your account and now you are a normie.")
  else:
    await ctx.send("You don't even have an account")

#Flexes robotics

@bot.command()
async def clubs_to_join(ctx):
  await ctx.send("Robotics")

#________BIRTHDAY FEATURES________

#Allows user to add their birthdate

@bot.command()
async def new_bday(ctx, mm: int, dd: int, yyyy: int):
  user_data = db[ctx.author.id]
  user_data["xp"] += 5
  if "Birthdate" not in user_data:
    bdate = []
    bdate.append(mm)
    bdate.append(dd)
    bdate.append(yyyy)
    user_data["Birthdate"] = bdate
    db[ctx.author.id] = user_data
    await ctx.send("%s's birthday on %02d/%02d/%04d has been saved." % (ctx.author.name, mm, dd, yyyy))
  else:
    await ctx.send("You already told me your birthday silly goose.")
    await ctx.send(file=discord.File('reactions/silly.gif'))


#Changes user's birthdate

@bot.command()
async def change_bday(ctx, mm: int, dd: int, yyyy: int):
  user_data = db[ctx.author.id]
  user_data["xp"] += 5
  if "Birthdate" in user_data:
    bdate = []
    bdate.append(mm)
    bdate.append(dd)
    bdate.append(yyyy)
    user_data["Birthdate"] = bdate
    db[ctx.author.id] = user_data
    await ctx.send("Your birthday has been changed to %02d/%02d/%04d" % (mm, dd, yyyy))
  else:
    await ctx.send("SMH. You never added your birthday to begin with.")
    await ctx.send(file=discord.File('reactions/silly.gif'))


#Prints user bday

@bot.command()
async def my_bday(ctx):
  user_data = db[ctx.author.id]
  user_data["xp"] += 5
  bdate = user_data["Birthdate"]
  simple_date = "Your birthday is on %02d/%02d/%02d. Its kinda sad that you need a bot to remind you when you were born." % (bdate[0],bdate[1],bdate[2])
  await ctx.send(simple_date)

#________DOGE MONEY FEATURES________

#Begging feature

@bot.command()
async def beg(ctx):
  user_data = db[ctx.author.id]
  xp = user_data["xp"]
  money = user_data["money"]
  if xp >= 5:
    add_doge = random.randint(0,1000)
    xp = xp - 5
    money = money + add_doge
    user_data["xp"] = xp
    user_data["money"] = money
    db[ctx.author.id] = user_data
    await ctx.send("Doge has generously donated %s doges" % (add_doge))
  else:
    await ctx.send("Stop begging, you don't have enough XP.")

#Balance statement feature

@bot.command()
async def bal(ctx):
  user_data = db[ctx.author.id]
  bal = user_data["money"]
  if bal >= 100000:
    await ctx.send("You're pretty rich, you have %s doge" % (bal))
    return
  if bal >= 50000:
    await ctx.send("You're alright, you have %s doge" % (bal))
    return
  if bal > 0:
    await ctx.send("You're a normie, you have %s doge" % (bal))
    return
  else:
    await ctx.send("You are broke, you have no money")
    await ctx.send(file=discord.File('reactions/sad_doge.gif'))

#XP statement feature

@bot.command()
async def xp(ctx):
  user_data = db[ctx.author.id]
  xp = user_data["xp"]
  await ctx.send("You have %s XP" % (xp))

#Rich list feature (WORK IN PROGRESS)

@bot.command()
async def rich(ctx):
  rich_dict = {}
  for id in db:
    data = db[id]
    name = data["name"]
    money = data["money"]
    rich_dict[name] = money
  await ctx.send(rich_dict)

#Robbery feature (WORK IN PROGRESS)

@bot.command()
async def rob(ctx, victim):
  names = []
  name_id = {}
  user_data = db[ctx.author.id]
  user_items = user_data['items']
  if "disguise" in user_items:
    user_items.remove("disguise")
    for x in db:
      names.append(db[x]['name'])
      named = db[x]['name']
      name_id[named] = x
    if victim in names:
      rich_dict = {}
      for id in db:
        data = db[id]
        name = data["name"]
        money = data["money"]
        rich_dict[name] = money
      person_bal = (rich_dict[victim])
      to_steal = int(person_bal/10)
      victimid = name_id[victim]
      victim_data = db[victimid]
      stolen = random.randint(0,(to_steal))
      person_bal -= stolen
      user_data['money'] += stolen
      victim_data['money'] -= stolen
      db[ctx.author.id] = user_data
      db[victimid] = victim_data
      if person_bal > 0:
        await ctx.send("You have stolen %s from %s but your disguise tore while you were getting away" % (stolen, victim))
        return
      else:
        await ctx.send("HAHA LMAO you tried robbing a broke person and you lost your disguise.")
        return
    else:
      await ctx.send("I don't know anyone with that name normie. Btw you lost ur disguise because you tripping.")
      return
  else:
    await ctx.send("SMH you need to buy a disguise to rob people genius.")
    




#________STORE ITEMS_________

store = {"disguise":1000,"doge_statue":10000,"starship_ticket":100000}

#Marketplace feature
@bot.command()
async def for_sale(ctx):
  global store
  await ctx.send(store) 
@bot.command()
async def buy(ctx, item: str):
  global store
  if item in store.keys():
    user_data = db[ctx.author.id]
    items = user_data["items"]
    price = store[item]
    bal = user_data["money"]
    if item in items:
      await ctx.send("You already own this.")
      return
    if (bal >= price):
      bal = bal - price
      items.append(item)
      user_data["money"] = bal
      user_data["items"] = items
      db[ctx.author.id] = user_data
      await ctx.send("You bought a %s for %s doge" % (item, price))
    else:
      await ctx.send("You cant afford a %s" % (item))
  else: 
    await ctx.send("This item isn't for sale")

#Random Memes
@bot.command()
async def plsmch(ctx):
  await ctx.send("PLSMCH stop.")
  await ctx.send(file=discord.File('reactions/plsmch.gif'))

#Keeps the bot active

keep_alive()

#Gives the script permission to run on discord

bot.run(os.getenv('TOKEN'))