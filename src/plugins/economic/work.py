import lightbulb
import hikari

from config import setting
from utils import local, access, db, level

import random

plugin = lightbulb.Plugin("work", default_enabled_guilds=setting.guild_id)


@plugin.command()
@lightbulb.add_checks(access.disable_command)
@lightbulb.add_cooldown(43200, 1, lightbulb.UserBucket)
@lightbulb.command("work", "заработать монеты для разных вещей")
@lightbulb.implements(lightbulb.SlashCommand)
async def work(ctx: lightbulb.Context) -> None:
    l = local.localization(ctx.get_guild().id)
    level.add_xp(ctx.author.id)

    #TODO: поменять после обт
    if db.premium(ctx.author.id) == None:
        coin = random.randint(300, 390)
        if random.randint(1, 1000) == 250:
            macoin = 1
        else:
            macoin = 0

    else:
        coin = random.randint(600, 1080)
        macoin = random.randint(2, 4)

    coins = db.db.user.find_one({"id": ctx.author.id})["coin"]
    macoins = db.db.user.find_one({"id": ctx.author.id})["macoin"]

    db.db.user.update_one(
        {"id": ctx.author.id},
        {
            "$set": {
                "coin": coins + coin
            }
        }
    )
    db.db.user.update_one(
        {"id": ctx.author.id},
        {
            "$set": {
                "macoin": macoins + macoin
            }
        }
    )

    emb = hikari.Embed(
        title = l["work.title"],
        description = l["work.desc"],
        color=setting.color
    )
    emb.add_field(name = l["work.coin"], value = f"{coin} :coin:")
    if macoin >= 1:
        emb.add_field(name = l["work.macoin"], value=f"{macoin} :star:")

    await ctx.respond(embed = emb)

def load(client):
    client.add_plugin(plugin)