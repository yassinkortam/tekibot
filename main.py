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

#Initializes the db key and auth token for users

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
  if bal >= 50000:
    await ctx.send("You're alright, you have %s doge" % (bal))
  if bal > 0:
    await ctx.send("You're a normie, you have %s doge" % (bal))
  else:
    await ctx.send("You are broke, you have no money")
    await ctx.send(file=discord.File('reactions/sad_doge.gif'))

#XP statement feature

@bot.command()
async def xp(ctx):
  user_data = db[ctx.author.id]
  xp = user_data["xp"]
  await ctx.send("You have %s XP" % (xp))

#Robbery feature

@bot.command()
async def rob(ctx, victim):
  for x in db.keys():
    if db[x]['name'] == victim:
      await ctx.send("success")


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


#Keeps the bot active

keep_alive()

#Gives the script permission to run on discord

bot.run(os.getenv('TOKEN'))
