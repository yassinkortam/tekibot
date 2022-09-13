import discord
import os
import random
import asyncio
import logging
from replit import db
from discord.ext import commands, tasks
import clubinfo
import keywords

bot = commands.Bot(command_prefix='pls ')
admins = [588483247256895500]
client = discord.Client()
logging.basicConfig(level=logging.INFO)
        
#Lets us know the bot is active

@bot.event
async def on_ready():
  print("%s has entered the chat" % (bot.user))
#________GAMES________
@bot.event
async def on_message(message):
    global month
    global day
    await bot.process_commands(message)
    accel_color = 0x0047ab

    if message.author == bot.user:
      return
    accel_color = 0x0047ab

    features = ["List clubs", "How to join clubs", "Club information"]
    clubs = clubinfo.clubs 
    club_info_keywords = keywords.club_info_keywords
    join_club_keywords = keywords.join_club_keywords
    existing_clubs_keywords = keywords.existing_clubs_keywords
    recommend_clubs_keywords = keywords.recommend_clubs_keywords
    info_clubs_keywords = keywords.info_clubs_keywords
  
    message_content = message.content.lower()
    punctuation = ['.','?','!',',']
    for x in punctuation:
      message_content = message_content.replace(x," ")
    word_list = message_content.split()
    if message.content.lower().startswith('helper'):
    #Checks how relevant the message is for the club search feature

      club_search_relevance = 0
      for word in word_list:
        if word in club_info_keywords.keys():
          club_search_relevance += club_info_keywords[word]
      if club_search_relevance >= 2:
        contextualizer = {'join':0, 'list':0, 'recommend':0, 'info':0}
        for word in word_list:

        #Checks the context of the message to streamline the help
          if word in join_club_keywords.keys():
            contextualizer['join'] += join_club_keywords[word]
          if word in existing_clubs_keywords.keys():
            contextualizer['list'] += existing_clubs_keywords[word]
          if word in recommend_clubs_keywords.keys():
            contextualizer['recommend'] += recommend_clubs_keywords[word]
          if word in info_clubs_keywords.keys():
            contextualizer['info'] += info_clubs_keywords[word]
        ctxj = contextualizer['join'] 
        ctxl = contextualizer['list']
        ctxr = contextualizer['recommend']
        ctxi = contextualizer['info']
        print(ctxj,ctxl,ctxr,ctxi)
        values = []
        for key in contextualizer.keys():
          values.append(contextualizer[key])
        largest_value = max(values)
        big_keys = []
        for key in contextualizer.keys():
          if largest_value == contextualizer[key]:
            big_keys.append(key)
        print(big_keys)
        if len(big_keys) <= 1 and largest_value >= 2:
          if 'info' in big_keys:
            dtxt = """Type the name of the club **exactly** as it appears in this list:

"""
            for club in clubs.keys():
                row1= "**" + club + "**" 
                dtxt += row1+"\n \n"
            response = discord.Embed(description = dtxt, color = accel_color)
            response.set_author(name = "Helper", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
            await message.reply(embed = response)
            msg = await bot.wait_for('message')
            if msg.content in clubs.keys():
              if "Poster" in clubs[msg.content].keys():
                path = clubs[msg.content]["Poster"]
                poster = discord.File(path)
                await message.reply(file = poster)
                return
              else:
                await message.reply("This club has no information")
                return
          elif 'join' in big_keys:
            dtxt = "There is no official way to join clubs, but you can reach out to club leaders and talk to them about it. `Would you like to view a list of all the clubs and their leaders? Yes or No.`"
            response = discord.Embed(description = dtxt, color = accel_color)
            response.set_author(name = "Helper", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
            await message.reply(embed = response)
            msg = await bot.wait_for('message')
            if "yes" in msg.content.lower():
              dtxt = """ """
              for club in clubs.keys():
                row1= "**" + club + "**    " + clubs[club]["Icon"] + " **:** " 
                row2= "*Contact*: " + clubs[club]["Contact"] 
                row3= "*Members*: " + str(clubs[club]["Members"])
                if len(clubs[club]["Discord Invite"]) >= 3: 
                  row4= "*Discord Invite*: " + clubs[club]["Discord Invite"]
                  dtxt += row1+"\n"+row2+"\n"+row3+"\n"+row4+"\n \n"
                else:
                  dtxt += row1+"\n"+row2+"\n"+row3+"\n \n"
              response = discord.Embed(description = dtxt, color = accel_color)
              response.set_author(name = "Helper", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
              await message.reply(embed = response)
              return
            elif "no" in msg.content.lower():
              await message.reply("Ok, see you later")
              return
          elif 'list' in big_keys:
            await message.reply("Would you like me to list all the clubs at accel? `Yes or No`")
            msg = await bot.wait_for('message')
            msg_lower = msg.content.lower()
            if "yes" in msg_lower:
              dtxt = """ """
              for club in clubs.keys():
                row1= "**" + club + "**    " + clubs[club]["Icon"] + " **:** " 
                row2= "*Contact*: " + clubs[club]["Contact"] 
                row3= "*Members*: " + str(clubs[club]["Members"])
                row4 = ""
                if len(clubs[club]["Discord Invite"]) >= 3: 
                  row4= "*Discord Invite*: " + clubs[club]["Discord Invite"]
                  dtxt += row1+"\n"+row2+"\n"+row3+"\n"+row4+"\n \n"
                else:
                  dtxt += row1+"\n"+row2+"\n"+row3+"\n \n"
              response = discord.Embed(description = dtxt, color = accel_color)
              response.set_author(name = "Helper", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
              await message.reply(embed = response)
              return
            elif "no" in msg_lower:
              await message.reply("Sorry about that, try rephrasing your request if you wanted me to respond")
            else:
              await message.reply("Sorry about that, try rephrasing your request if you wanted me to respond")
          elif 'recommend' in big_keys:
            await message.channel.send("The club reccomendation feature is a work in progress")
            return
          else:
            dtxt = """**I can't help you with that, however here are the things I can do for you:**

"""
            for feature in features:
              row =  "*"+feature+"* \n" 
              dtxt += row
            response = discord.Embed(description = dtxt, color = accel_color)
            response.set_author(name = "Helper", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
            await message.reply(embed = response)
            return
      else:
          await message.reply("Sorry, your request might be too general. Please rephrase it.")
          return


    
  #DERIVATIVE GAME
    if message.author == bot.user:
      return
    if message.content.startswith('whose birthday'):
      if month == 3 and day == 18:
        p_lealbday = discord.Embed(description="%s would like to say happy birthday to Ms. Leal" %(message.author.name), color = 0xff0000)
        p_lealbday.set_author(name = "Master Doge",icon_url = "https://i.imgur.com/zDuMDuW.jpg")
        await message.reply(embed = p_lealbday, file = discord.File('reactions/bday.gif') )
    if message.content.startswith('pls derivative'):
        if message.author.id not in db.keys():
          db[message.author.id] = {}
        user_data = db[message.author.id]
        if "xp" not in user_data.keys():
          user_data["xp"] = 0
          db[message.author.id] = user_data
        channel = message.channel
        a = random.randint(1,100)
        n = random.randint(1,100)
        question = ("Differentiate `%sx^(%s)`. Write your answer exactly in the format `ax^(n)`. " % (str(a),str(n)))
        new_const = a * n
        new_expo = n - 1
        solution = ("%sx^(%s)" % (new_const,new_expo))
        p_question = discord.Embed(title = "Calculus Game: Derivatives",description= question, color = 0x0047ab)
        await channel.send(embed = p_question)
        msg = await bot.wait_for('message', check=None)
        if msg.content == solution:
          user_data = db[msg.author.id]
          xp = user_data['xp']
          xp += 100
          user_data['xp'] = xp
          db[msg.author.id] = user_data
          result = """Correct **%s**, you earned `100 XP` for making your calc professor proud.""" % (msg.author.name)
          p_result = discord.Embed(title = "Results:", description = result, color = 0x0047ab)
          await message.reply(embed = p_result)
        else:
          result = """That's wrong **%s**, you dissapointed your calc professor.
Correct answer: `%s`""" % (msg.author.name, solution)
          p_result = discord.Embed(title = "Results:", description = result, color = 0x0047ab)
          await message.reply(embed = p_result)
    #INTEGRATION GAME
    if message.content.startswith('pls integral'):
        if message.author.id not in db.keys():
          db[message.author.id] = {}
        user_data = db[message.author.id]
        if "xp" not in user_data.keys():
          user_data["xp"] = 0
          db[message.author.id] = user_data
        channel = message.channel
        a = random.randint(1,100)
        n = random.randint(1,100)
        question = ("Integrate `%sx^(%s)`. Write your answer exactly in the format `(a/1)x^(n)`. " % (str(a),str(n)))
        new_const = "(%s/%s)" % (a,n)
        new_expo = n+1
        solution = ("%sx^(%s)" % (new_const,new_expo))
        p_question = discord.Embed(title = "Calculus Game: Integrals",description= question, color = 0x0047ab)
        await channel.send(embed = p_question)
        msg = await bot.wait_for('message', check=None)
        if msg.content == solution:
          user_data = db[msg.author.id]
          xp = user_data['xp']
          xp += 100
          user_data['xp'] = xp
          db[msg.author.id] = user_data
          result = """Correct **%s**, you earned `100 XP` for making your calc professor proud.""" % (msg.author.name)
          p_result = discord.Embed(title = "Results:", description = result, color = 0x0047ab)
          await message.reply(embed = p_result)
        else:
         result = """That's wrong **%s**, you dissapointed your calc professor.
Correct answer: `%s`""" % (msg.author.name, solution)
         p_result = discord.Embed(title = "Results:", description = result, color = 0x0047ab)
         await message.reply(embed = p_result)
         
    #SPACE TRAVEL GAME

    if message.content.startswith('pls starship'):
      if message.author.id not in db:
        db[message.author.id] = {}
      user_data = db[message.author.id]
      if "items" not in user_data.keys():
        user_data["items"] = {}
        db[message.author.id] = user_data
      user_data = db[message.author.id]
      items = user_data["items"]
      if "planet" not in user_data.keys():
        user_data["planet"] = "earth"
        db[message.author.id] = user_data
      user_data = db[message.author.id]
      planet = user_data["planet"]
      user_items = user_data['items']
      if "starship_ticket" not in items.keys():
        await message.reply("No freeloaders, buy a `starship_ticket`")
        return
      q_starship = user_items['starship_ticket']
      if q_starship <=0:
         p_response = discord.Embed(description = """ "No freeloaders, buy a `starship_ticket`." """, color = master_color)
         p_response.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
         await message.reply(embed = p_response)
         return
      p_question = discord.Embed(description = """ "Where would you like to go to?" 

`earth`  :earth_africa:
`mars`  <:mars:820133233328521257>
""", color = master_color)
      p_question.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
      await message.reply(embed = p_question)
      msg = await bot.wait_for('message', check=None)

      #GO TO MARS

      if msg.content == "mars":
          if planet != "mars":
            q_starship -= 1
            user_data["planet"] = "mars"
            user_items['starship_ticket'] = q_starship
            user_data["items"] = user_items
            db[message.author.id] = user_data
            p_responsem = discord.Embed(description = """ "%s has boarded starship and is headed to `mars`  <:mars:820133233328521257>" """ %(message.author.name), color = master_color)
            p_responsem.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
            await message.reply(embed = p_responsem)
            await asyncio.sleep(2)
            await message.channel.send(file = discord.File('reactions/takeoff.gif'))
            await asyncio.sleep(5)
            await message.channel.send(file = discord.File('reactions/mars.gif'))
            await asyncio.sleep(4)
            p_arrivalm = discord.Embed(description = """ "Congratulations %s, you have reached `mars`" """ %(message.author.name), color = master_color)
            p_arrivalm.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
            await message.reply(embed = p_arrivalm)
            return
          else:
            p_question = discord.Embed(description = """ "You're already on `mars` man." """, color = master_color)
            p_question.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
            await message.reply(embed = p_question)
            return

      #GO TO EARTH

      if msg.content == "earth": 
          if planet != "earth":
            q_starship -= 1
            user_data["planet"] = "earth"
            user_items['starship_ticket'] = q_starship
            user_data["items"] = user_items
            db[message.author.id] = user_data
            p_responsee = discord.Embed(description = """ "%s has boarded starship and is headed to `earth`. :earth_africa:" """ %(message.author.name), color = master_color)
            p_responsee.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
            await message.reply(embed = p_responsee)
            await asyncio.sleep(2)
            await message.channel.send(file = discord.File('reactions/takeoff.gif'))
            await asyncio.sleep(5)
            await message.channel.send(file = discord.File('reactions/earth_landing.gif'))
            await asyncio.sleep(4)
            p_arrival = discord.Embed(description = """ "Congratulations %s, you have reached `earth`" """ %(message.author.name), color = master_color)
            p_arrival.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
            await message.reply(embed = p_arrival)
            return
          else:
            p_question = discord.Embed(description = """ "You're already on `earth` man." """, color = master_color)
            p_question.set_author(name = "Elon Musk", icon_url = "https://pbs.twimg.com/profile_images/1364491704817098753/V22-Luf7_400x400.jpg")
            await message.reply(embed = p_question)
            return
         

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
 

#________BIRTHDAY FEATURES________
bday_color = 0xffc0cb
#Allows user to add their birthdate
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command()
async def new_bday(ctx, mm: int, dd: int, yyyy: int):
  global bday_color
  if ctx.author.id not in db.keys():
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "xp" not in user_data.keys():
    user_data["xp"] = 0
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  user_data["xp"] += 5
  if "Birthdate" not in user_data:
    bdate = []
    bdate.append(mm)
    bdate.append(dd)
    bdate.append(yyyy)
    user_data["Birthdate"] = bdate
    db[ctx.author.id] = user_data
    simple_date = "**%s's** birthday on `%02d/%02d/%04d` has been saved." % (ctx.author.name, mm, dd, yyyy)
    p_bday = discord.Embed(title = "%s's  :birthday:"%(ctx.author.name),description= simple_date, color = bday_color)
    await ctx.reply(embed =  p_bday)
  
  else:
    p_reply = discord.Embed(title = ":birthday:  Doge",description = "You already told me your birthday silly goose.",color = bday_color)
    await ctx.reply(embed = p_reply, file = discord.File('reactions/silly.gif'))


#Changes user's birthdate
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command()
async def change_bday(ctx, mm: int, dd: int, yyyy: int):
  global bday_color
  if ctx.author.id not in db.keys():
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "xp" not in user_data.keys():
    user_data["xp"] = 0
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
  user_data["xp"] += 5
  if "Birthdate" in user_data:
    bdate = []
    bdate.append(mm)
    bdate.append(dd)
    bdate.append(yyyy)
    user_data["Birthdate"] = bdate
    db[ctx.author.id] = user_data
    simple_date = "**%s's** birthday has been changed to `%02d/%02d/%04d`" % (ctx.author.name, mm, dd, yyyy)
    p_bday = discord.Embed(title = ":birthday:  Doge",description = simple_date, color = bday_color)
    await ctx.reply(embed =  p_bday)
  else:
    p_bday = discord.Embed(title = ":birthday:  Doge",description= """ "SMH. You never told me your birthday to begin with." """, color = bday_color)
    await ctx.reply(embed = p_bday, file=discord.File('reactions/silly.gif'))

#Prints user bday

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def my_bday(ctx):
  global bday_color
  if ctx.author.id not in db.keys():
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  if "Birthdate" not in user_data.keys():
   p_bday = discord.Embed(title = ":birthday:  Doge",description= """ "SMH. You never told me your birthday to begin with." """, color = bday_color)
   await ctx.reply(embed = p_bday, file=discord.File('reactions/silly.gif'))
   return
  else:
    user_data = db[ctx.author.id]
    user_data["xp"] += 5
    bdate = user_data["Birthdate"]
    simple_date = "Your birthday is on `%02d/%02d/%02d`. Its kinda sad that you need a bot to remind you when you were born." % (bdate[0],bdate[1],bdate[2])
    p_bday = discord.Embed(title = "%s's  :birthday:"%(ctx.author.name),description= simple_date, color = bday_color)
    await ctx.reply(embed =  p_bday)

#________DOGE MONEY FEATURES________
money_color = 0x00ff00
#Begging feature
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def beg(ctx):
  global money_color
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "money" not in user_data.keys():
    user_data["money"] = 0
    db[ctx.author.id] = user_data
  if "xp" not in user_data.keys():
    user_data["xp"] = 0
    db[ctx.author.id] = user_data
  if "name" not in user_data.keys():
    user_data["name"] = ctx.author.name
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
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
    d_beg = """ "Sup homie, I'ma give you `%s`  :coin:  " """ % (add_doge)
    p_beg = discord.Embed(description = d_beg, color = money_color)
    p_beg.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_beg)
  else:
    response = """ "You aint got enough XP man stop tripping" """
    p_beg = discord.Embed(description = response, color = money_color)
    p_beg.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
    await ctx.reply(embed = p_beg)

#Balance and XP statement feature
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def bal(ctx):
  global money_color
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "money" not in user_data.keys():
    user_data["money"] = 0
  if "xp" not in user_data.keys():
    user_data["xp"] = 0
  xp = user_data["xp"]
  bal = user_data["money"]
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  if bal >= 100000:
    bal_title = "%s's Wallets" % (ctx.author.name)
    bal_description = """
"You're pretty rich"

**Money**: `%s`  :coin:
**XP**: `%s`
 """ % (str(bal), str(xp))
    p_bal = discord.Embed(description = bal_description, color = money_color)
    p_bal.set_author(name = bal_title, icon_url = ctx.author.avatar_url)
    await ctx.reply(embed = p_bal)
    return
  if bal >= 50000:
     bal_title = "%s's Wallets" % (ctx.author.name)
     bal_description = """
"Doge not very much impressed"

**Money**: `%s`  :coin:
**XP**: `%s`
 """ % (str(bal), str(xp))
     p_bal = discord.Embed(description = bal_description, color = money_color)
     p_bal.set_author(name = bal_title, icon_url = ctx.author.avatar_url)
     await ctx.reply(embed = p_bal)
     return
  if bal > 0:
      bal_title = "%s's Wallets" % (ctx.author.name)
      bal_description = """
"Normie"

**Money**: `%s`  :coin:
**XP**: `%s`
 """ % (str(bal), str(xp))
      p_bal = discord.Embed(description = bal_description, color = money_color)
      p_bal.set_author(name = bal_title, icon_url = ctx.author.avatar_url)
      await ctx.reply(embed = p_bal)
      return
  else:
    bal_title = "%s's Wallets" % (ctx.author.name)
    bal_description = """
"LOL ur broke"

**Money**: `%s`  :coin:
**XP**: `%s`
 """ % (str(bal), str(xp))
    p_bal = discord.Embed( description = bal_description, color = money_color)
    p_bal.set_author(name = bal_title, icon_url = ctx.author.avatar_url)
    await ctx.reply(embed = p_bal, file=discord.File('reactions/sad_doge.gif'))

#Wallet balance list feature (WORK IN PROGRESS)
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def wallets(ctx):
  global money_color
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "name" not in user_data.keys():
    user_data["name"] = ctx.author.name
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
  worth_list = """
"""
  for id in db.keys():
      data = db[id]
      guild = bot.get_guild(ctx.message.guild.id)
      if guild.get_member(id) is None:
        if "name" in data.keys():
          name = data["name"]
          money = data["money"]
          row = name+": `"+str(money)+"` :coin:\n"
          worth_list += row
        elif "money" in data.keys():
          name = "Unknown"
          money = data["money"]
          row = name+": `"+str(money)+"`  :coin:\n"
          worth_list += row
  p_worth_list = discord.Embed(title = "%s's Wallets:" % (ctx.message.guild.name), description = worth_list, color = money_color)
  await ctx.reply(embed = p_worth_list)

#Robbery feature
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def rob(ctx, victim):
  user_data = {}
  fail = random.randint(0,2)
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "money" not in user_data.keys():
    user_data["money"] = 0
    db[ctx.author.id] = user_data
  if "items" not in user_data.keys():
    user_data["items"] = {}
    db[ctx.author.id] = user_data
  items = user_data["items"]
  if "disguise" not in items.keys():
    items["disguise"] = 0
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  names = []
  name_id = {}
  user_data = db[ctx.author.id]
  user_items = user_data['items']
  q_disguise = user_items['disguise']
  if q_disguise > 0:
    q_disguise -= 1
    user_items['disguise'] = q_disguise
    user_data["items"] = user_items
    db[ctx.author.id] = user_data
    for x in db:
      named = db[x]['name']
      names.append(named)
      name_id[named] = x
    if victim in names and (fail == 1 or fail == 0): 
      victimid = name_id[victim]
      victim_data = db[victimid]
      if 1 == 1:     #insert server check here
          rich_dict = {}
          for id in db:
            data = db[id]
            name = data["name"]
            money = data["money"]
            rich_dict[name] = money
          person_bal = (rich_dict[victim])
          to_steal = int(person_bal/4)
          stolen = random.randint(0,(to_steal))
          person_bal -= stolen
          user_data['money'] += stolen
          victim_data['money'] -= stolen
          db[ctx.author.id] = user_data
          db[victimid] = victim_data
          if person_bal > 0:
            await ctx.reply("You have stolen `%s`  :coin:  from **%s** but your `disguise` tore while you were getting away" % (stolen, victim))
            return
          else:
            await ctx.reply("HAHA LMAO you tried robbing a broke person and you lost your `disguise`.")
            return
      
    elif fail != 1:
          await ctx.reply("L, you got busted and lost your `disguise`")
          return
    else:
          await ctx.reply("I don't know anyone with that name in this server normie. Btw you lost ur `disguise` because you tripping.")
          return
  else:
        await ctx.reply("SMH you need to buy a `disguise` to rob people genius.")

#Money giving command
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def give(ctx,victim, amount: int):
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "money" not in user_data.keys():
    user_data["money"] = 0
    db[ctx.author.id] = user_data
  if "name" not in user_data.keys():
    user_data["name"] = ctx.author.name
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  names = []
  name_id = {}
  user_data = db[ctx.author.id]
  user_bal = user_data['money']
  if amount >= 0:
    if amount <= user_bal:
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
        victimid = name_id[victim]
        victim_data = db[victimid]
        person_bal += amount
        user_data['money'] -= amount
        victim_data['money'] += amount
        db[ctx.author.id] = user_data
        db[victimid] = victim_data
        await ctx.reply("You have given **%s** `%s`  :coin:" % (victim,amount))
        return
      else:
        await ctx.reply("I dont know who that is.")
    else:
      await ctx.reply("You are too poor to give that amount.")
      return
  else:
    await ctx.reply("Nice try.")

#________STORE ITEMS_________
store_color = 0x964B00
store = {"disguise":1000,"doge_statue":10000,"starship_ticket":100000,"pop-socket":2000}

#Lists store items

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def shop(ctx):
  global store_color
  global store
  pretty_store = """
"""
  for x in store:
    item = x
    price = store[x]
    row = "**" + item + "** ---------- `"+ str(price) +"`  :coin: \n"
    pretty_store += row
  p_store = discord.Embed(title = "Items For Sale:", description = pretty_store, color = store_color)
  await ctx.reply(embed = p_store) 

#Buy items

@commands.cooldown(1, 1, commands.BucketType.user)
@bot.command()
async def buy(ctx, item: str):
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "items" not in user_data.keys():
    user_data["items"] = {}
    db[ctx.author.id] = user_data
  if "money" not in user_data.keys():
    user_data["money"] = 0
    db[ctx.author.id] = user_data
  if "xp" not in user_data.keys():
    user_data["xp"] = 0
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  global store
  if item in store.keys():
    user_data = db[ctx.author.id]
    items = user_data["items"]
    price = store[item]
    bal = user_data["money"]
    if item not in items.keys():
      items[item] = 0
    quantity = items[item]
    if (bal >= price):
      bal = bal - price
      quantity += 1
      items[item] = quantity
      user_data["money"] = bal
      user_data["items"] = items
      db[ctx.author.id] = user_data
      await ctx.reply("You bought a `%s`for `%s`  :coin:" % (item, price))
    else:
      await ctx.reply("You cant afford a `%s`" % (item))
  else: 
    await ctx.reply("This item isn't for sale")

#View inventory feature

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def inv(ctx):
  global store_color
  if ctx.author.id not in db:
    db[ctx.author.id] = {}
  user_data = db[ctx.author.id]
  if "items" not in user_data.keys():
    user_data["items"] = {}
    db[ctx.author.id] = user_data
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  user_data = db[ctx.author.id]
  items = user_data["items"]
  pretty_items = """"""
  for x in items:
    if items[x] > 0:
      quantity = items[x]
      item = x
      row = item+": `"+str(quantity)+"` \n"
      pretty_items += row
  if len(pretty_items) == 0:
    pretty_items += "You have no items."
  p_items = discord.Embed(description = pretty_items, color = store_color)
  p_items.set_author(name = ctx.author.name + "'s Inventory", icon_url = ctx.author.avatar_url)
  await ctx.reply(embed = p_items)
  
#Random Memes

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
async def plsmch(ctx):
  global master_color
  p_plsmch = discord.Embed(description = "**PLSMCH** stop.", color = master_color)
  p_plsmch.set_author(name = "Master Doge", icon_url = "https://i.imgur.com/zDuMDuW.jpg")
  await ctx.reply(embed = p_plsmch,file=discord.File('reactions/plsmch.gif'))
@bot.command()
async def test(ctx):
  user_data = db[ctx.author.id]
  if "server" not in user_data.keys():
    user_data["server"] = []
  servers = user_data["server"]
  if ctx.message.guild.id not in servers:
    servers.append(ctx.message.guild.id)
    user_data["servers"] = servers
    db[ctx.author.id] = user_data
  server = ctx.message.guild.name
  await ctx.reply(server)

#Keeps the bot active



#Gives the script permission to run on discord

bot.run(os.getenv('TOKEN'))
