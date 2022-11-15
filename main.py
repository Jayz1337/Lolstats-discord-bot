import discord
from discord.ext import commands
from riotwatcher import LolWatcher
from champions import get_champions_name


watcher = LolWatcher(".") # Riot API Code https://developer.riotgames.com
intents = discord.Intents().all()
bot=commands.Bot(command_prefix=".",intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command()
async def stats(ctx,region,*,ign):

    # -- Ids for summoners 
    id = watcher.summoner.by_name(region,ign)['id']
    #acc_id = watcher.summoner.by_name(region,ign)['accountId']
    #puuid = watcher.summoner.by_name(region,ign)['puuid']
    name = watcher.summoner.by_name(region,ign)['name']
    pficon_id = watcher.summoner.by_name(region,ign)['profileIconId']
    sum_lvl = watcher.summoner.by_name(region,ign)['summonerLevel']


    # -- In game stats
    summoner = watcher.league.by_summoner(region,id)
    q_type = summoner[0]['queueType']
    tier = summoner[0]['tier']
    rank = summoner[0]['rank']
    lp = summoner[0]['leaguePoints']
    wins = summoner[0]['wins']
    losses = summoner[0]['losses']
    inactive = summoner[0]['inactive']
    hot_streak = summoner[0]['hotStreak']
    winrate = wins/(wins+losses)*100

    # -- Top champ
    masteries = watcher.champion_mastery.by_summoner(region,id)
    print(masteries[0]["championPoints"])
    max_points=-1
    for i in range(len(masteries)):
        if masteries[i]["championPoints"] > max_points:
            max_points = masteries[i]["championPoints"]
            max_champid = masteries[i]["championId"]
            max_champlvl = masteries[i]["championLevel"]
            max_chest = masteries[i]["chestGranted"]
    print(max_points,max_champid,max_champlvl,max_chest)

    # -- Find champion by id
    champ = get_champions_name(max_champid)
    print(champ)

    # -- Embed
    embed = discord.Embed(title=f"{name} — Stats")
    embed.set_footer(text=f"Action called by {ctx.author.name}")
    embed.add_field(name="Useless info:", value=f"Name: **{name}**\nProfile Icon ID: **{pficon_id}**\nSummoner Level: **{sum_lvl}**",inline=False)
    embed.add_field(name="Statistics:",value=f"QueueType: **{q_type}**\nDivision: **{tier} {rank} {lp} LP**\nW/R: **{round(winrate,2)}%**\nInactive: **{inactive}**\nHotStreak: **{hot_streak}**", inline=False)
    embed.add_field(name="Champions:", value=f"Top champ: **{champ}**\nMastery Points: **{max_points}**\nLevel: **{max_champlvl}**\nChest Granted: **{max_chest}**", inline=False)
    await ctx.send(embed=embed)


bot.run(".") # Discord Bot Token


