import discord
import os
import random
import asyncio
import logging
from replit import db
from discord.ext import commands, tasks


bot = commands.Bot(command_prefix='pls ')
admins = [588483247256895500]
client = discord.Client()

#________MASTER DOGE/ MAINTENANCE FEATURES________


master_color = 0xff0000
#Makes me rich
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def make_rich(ctx):
  global master_color
  user_data = {}
  if ctx.author.id not in db.keys():
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "xp" not in user_data.keys():
    user_data["xp"] = 0
    db[ctx.author.id] = user_data
  if "money" not in user_data.keys():
    user_data["money"] = 0
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  user_data["xp"] += 5
  user_data = db[ctx.author.id]
  money = user_data['money']
  xp = user_data['xp']
  if ctx.author.id in admins:
    money += 1000000000000
    xp += 1000000
    user_data['money'] = money
    user_data['xp'] = xp
    db[ctx.author.id] = user_data
    reply = """ "Aight boss, you richer than Elon Musk now." """
    p_reply = discord.Embed(description= reply, color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply)
  else:
    reply = """ "Go away normie you trippin." """
    p_reply = discord.Embed(description= reply, color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply)


#Prints all the data in the database (ADMIN ONLY)
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command()
async def print_db(ctx):
  global master_color
  if ctx.author.id in admins:
    db_ref = {}
    for x in db:
      db_ref[x] = db[x]
    s_db = ("```%s```" %(db_ref))
    p_db = discord.Embed(description= s_db, color = master_color)
    p_db.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_db)
  else:
    p_reply = discord.Embed(description= "You don't have permission to see everyone's data, thats creepy.", color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply, file=discord.File('reactions/creepy.gif'))

#Allows the admin to clear things from the database
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def clear_db(ctx):
  global master_color
  if ctx.author.id not in db.keys():
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "confirm_token" not in user_data.keys():
    user_data["confirm_token"] = 0
    db[ctx.author.id] = user_data
  if (ctx.author.id in admins) and (user_data["confirm_token"] == 1):
    user_data["confirm_token"] = 0
    for x in db:
      del db[x]
    p_reply = discord.Embed(description= "Database cleared", color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply)
    return
  elif ctx.author.id in admins:
    user_data["confirm_token"] = 1
    db[ctx.author.id] = user_data
    p_reply = discord.Embed(description= "Ask again to confirm boss.", color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply)
    return
  else:
    p_reply = discord.Embed(description= "Permission denied", color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply, file=discord.File('reactions/creepy.gif'))

#Allows users to delete their account
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command()
async def del_account(ctx):
  global master_color
  if ctx.author.id in db:
    del db[ctx.author.id]
    p_reply = discord.Embed(description= "I deleted your account and now you are a normie.", color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_reply,file=discord.File('reactions/sad_doge.gif'))
  else:
     p_reply = discord.Embed(description= "You don't even have an account", color = master_color)
     p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
     await ctx.reply(embed = p_reply)

#Flexes robotics

@bot.command()
async def clubs(ctx):
    global master_color
    p_reply = discord.Embed(description= """ "Robotics, thats all doge knows."  :robot: """, color = master_color)
    p_reply.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed =  p_reply)
 
