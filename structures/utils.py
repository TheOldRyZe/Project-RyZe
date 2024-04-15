import random
import aiohttp
import discord
import asyncio
import datetime
import time

from database.database import database_instance

import settings.links as links
import settings.config as config
import settings.emojis as emojis
import settings.webhooks as webhooks
import settings.credentials as credentials

cluster = database_instance()
database = cluster["RyZe"]

prefix_collection = database["prefixes"]
noprefix_collection = database["no_prefixes"]
noprefix_access_collection = database["no_prefix_access"]
blacklist_collection = database["blacklists"]
antinuke_collection = database["antinuke"]
extraowner_collection = database["extraowners"]
whitelist_collection = database["whitelists"]
mainrole_collection = database["mainroles"]
nightmode_collection = database["nightmode"]

whitelist_options = [
            discord.SelectOption(label="Ban", value="Ban", description="Toggle's the Whitelist of a member with ban permission"),
            discord.SelectOption(label="Kick", value="Kick", description="Toggle's the Whitelist of a member with kick permission"),
            discord.SelectOption(label="Prune", value="Prune", description="Toggle's the Whitelist of a member with prune permission"),
            discord.SelectOption(label="Bot Add", value="Bot_Add", description="Toggle's the Whitelist of a member with bot add permission"),
            discord.SelectOption(label="Server Update", value="Server_Update", description="Toggle's the Whitelist of a member with server update permission"),
            discord.SelectOption(label="Member Update", value="Member_Update", description="Toggle's the Whitelist of a member with member update permission"),
            discord.SelectOption(label="Channel Create", value="Channel_Create", description="Toggle's the Whitelist of a member with channel create permission"),
            discord.SelectOption(label="Channel Delete", value="Channel_Delete", description="Toggle's the Whitelist of a member with channel delete permission"),
            discord.SelectOption(label="Channel Update", value="Channel_Update", description="Toggle's the Whitelist of a member with channel update permission"),
            discord.SelectOption(label="Role Create", value="Role_Create", description="Toggle's the Whitelist of a member with role create permission"),
            discord.SelectOption(label="Role Update", value="Role_Delete", description="Toggle's the Whitelist of a member with role update permission"),
            discord.SelectOption(label="Role Delete", value="Role_Update", description="Toggle's the Whitelist of a member with role delete permission"),
            discord.SelectOption(label="Mention Everyone", value="Manage_Events", description="Toggle's the Whitelist of a member with mention everyone permission"),
            discord.SelectOption(label="Manage Webhook", value="Manage_Webhooks", description="Toggle's the Whitelist of a member with manage webhook permission"),
            discord.SelectOption(label="Manage Stickers & Emojis", value="Manage_Sticker_And_Emoji", description="Toggle's the Whitelist of a member with Manage stickers & emojis permission")
        ]

antinuke_modules = [
    "Anti_Ban",
    "Anti_Unban",
    "Anti_Bot",
    "Anti_Channel_Create",
    "Anti_Channel_Delete",
    "Anti_Channel_Update",
    "Anti_Emoji_Create",
    "Anti_Emoji_Delete",
    "Anti_Emoji_Update",
    "Anti_Sticker_Create",
    "Anti_Sticker_Delete",
    "Anti_Sticker_Update",
    "Anti_Guild_Update",
    "Anti_Kick",
    "Anti_Integration",
    "Anti_Ping",
    "Anti_Role_Ping",
    "Anti_Role_Create",
    "Anti_Role_Delete",
    "Anti_Role_Update",
    "Anti_Prune",
    "Anti_Webhook_Create",
    "Anti_Webhook_Update",
    "Anti_Webhook_Delete",
    "Anti_Member_Update",
    "Anti_Automod_Rule_Create",
    "Anti_Automod_Rule_Update",
    "Anti_Automod_Rule_Delete",
    "Anti_Guild_Event_Create",
    "Anti_Guild_Event_Update",
    "Anti_Guild_Event_Delete",
]

whitelist_modules = [
    "Ban",
    "Kick",
    "Prune",
    "Bot_Add",
    "Server_Update",
    "Member_Update",
    "Channel_Create",
    "Channel_Delete",
    "Channel_Update",
    "Role_Create",
    "Role_Delete",
    "Role_Update",
    "Manage_Events",
    "Manage_Webhooks",
    "Manage_Sticker_And_Emoji"
]

default_whitelist_db = {
    "Ban": False,
    "Kick": False,
    "Prune": False,
    "Bot_Add": False,
    "Server_Update": False,
    "Member_Update": False,
    "Channel_Create": False,
    "Channel_Delete": False,
    "Channel_Update": False,
    "Role_Create": False,
    "Role_Delete": False,
    "Role_Update": False,
    "Manage_Events": False,
    "Manage_Webhooks": False,
    "Manage_Sticker_And_Emoji": False
}




async def ban(guild_id, user_id, reason="Suspicious Activity | RyZe"):
    url = f'https://discord.com/api/v9/guilds/{str(guild_id)}/bans/{str(user_id)}'
    headers = {
        'Authorization': f'Bot {credentials.token}'
    }
    payload = {
        'reason': reason
    }


    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(url, headers=headers, json=payload) as response:
                if response.status == 204:
                    return True
                else:
                    return False
        except:
            return False









async def sleep(ms):
    await asyncio.sleep(ms)

async def add_role_to_nightmode(guild_id, role_id, permissions):
    server_data = nightmode_collection.find_one({'guild_id': str(guild_id), 'role_id': str(role_id)})
    if server_data:
        nightmode_collection.update_one({'guild_id': str(guild_id), 'role_id': str(role_id)}, {'$set': {'admin_permissions': permissions}}, upsert=True)
    else:
        nightmode_collection.insert_one({'guild_id': str(guild_id), 'role_id': str(role_id), 'admin_permissions': permissions})
    return True

async def get_nightmode_roles(guild_id):
    stored_roles = nightmode_collection.find({'guild_id': str(guild_id)})
    return stored_roles

async def remove_role_from_nightmode(guild_id, role_id):
    nightmode_collection.delete_one({'guild_id': str(guild_id), 'role_id': str(role_id)})
    return True


async def add_mainrole(guild_id, role_id):
    mainrole_find = mainrole_collection.find_one({"id": str(guild_id)})
    if mainrole_find:
        ryze = mainrole_find["mainroles"]
        if len(ryze) >= 5:
            return "maximum"
        elif role_id in ryze:
            return "already"
        else:
            mainrole_collection.update_one(
                {"id": str(guild_id)}, {"$push": {"mainroles": role_id}}
            )
            return "added"
    else:
        mainrole_collection.insert_one(
            {"id": str(guild_id), "mainroles": [role_id]}
        )
        return "added"

async def remove_mainrole(guild_id, role_id):
    mainrole_find = mainrole_collection.find_one({"id": str(guild_id)})
    if mainrole_find:
        ryze = mainrole_find["mainroles"]
        if role_id in ryze:
            ryze.remove(role_id)
            mainrole_collection.update_one(
                {"id": str(guild_id)}, {"$set": {"mainroles": ryze}}
            )
            return "removed"
        else:
            return "not_found"
    else:
        return "not_found"


async def list_mainroles(guild_id):
    mainrole_find = mainrole_collection.find_one({"id": str(guild_id)})
    if mainrole_find:
        ryze = mainrole_find["mainroles"]
        return ryze
    else:
        return []

async def clear_mainroles(guild_id):
    mainrole_collection.delete_one({"id": str(guild_id)})
    return True




async def error_logger(error):
        error_embed = discord.Embed(
            description=f"```{error}```",
            color=config.color
        )
        error_embed.set_footer(text=f"{datetime.date.today()} | {datetime.datetime.now().strftime('%H:%M:%S')}")

        await send_to_webhook(webhooks.error_logs, error_embed)


async def get_whitelist_embed(guild_id, user_id, ctx):
    embed = discord.Embed(description="**Whitelisting this user will grant immunity from antinuke measures. You can view the current whitelists using the command: `whitelist config`**",color=config.color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    embed.add_field(name = "Modules", value = await list_whitelists(guild_id, user_id))
    return embed

async def add_whitelist(guild_id, user_id, module):
    if module == "All":
        whitelist_collection.update_one(
            {"id": str(guild_id), "user_id": str(user_id)},
            {"$set": {"whitelists": {module: True for module in whitelist_modules}}},
            upsert=True
        )
        return True
    else:
        whitelist_find = whitelist_collection.find_one({"id": str(guild_id), "user_id": str(user_id)})
        if whitelist_find:
            ryze = whitelist_find["whitelists"]
            ryze[module] = True
            whitelist_collection.update_one(
                {"id": str(guild_id), "user_id": str(user_id)},
                {"$set": {"whitelists": ryze}}
            )
            return True
        else:
            default_whitelist_db_copy = default_whitelist_db.copy()
            default_whitelist_db_copy[module] = True
            whitelist_collection.insert_one(
                {"id": str(guild_id), "user_id": str(user_id), "whitelists": default_whitelist_db_copy}
            )
            return True

async def get_whitelist(guild_id, user_id):
    whitelist_find = whitelist_collection.find_one({"id": str(guild_id), "user_id": str(user_id)})
    if whitelist_find:
        ryze = [module for module in whitelist_find["whitelists"].items()]
        return ryze
    else:
        whitelist_collection.insert_one(
                {"id": str(guild_id), "user_id": str(user_id), "whitelists": default_whitelist_db}
            )
        whitelist_find2 = whitelist_collection.find_one({"id": str(guild_id), "user_id": str(user_id)})
        ryze = [module for module in whitelist_find2["whitelists"].items()]
        return ryze

async def list_whitelisted_users(guild_id):
    whitelisted_users = []
    whitelist_find = whitelist_collection.find({"id": str(guild_id)})
    if whitelist_find:
        for document in whitelist_find:
            user_id = document["user_id"]
            whitelists = document["whitelists"]
            for module, status in whitelists.items():
                if status:
                    whitelisted_users.append(user_id)
                    break
    return whitelisted_users


async def list_whitelists(guild_id, user_id):
    text = ""
    whitelists = await get_whitelist(guild_id, user_id)
    for module, status in whitelists:
        text += f"\n**{module.replace('_', ' ')}: {emojis.tick if status else emojis.cross}**"
    return text

async def remove_whitelist(guild_id, user_id, module):
    if module == "All":
        whitelist_collection.update_one(
            {"id": str(guild_id), "user_id": str(user_id)},
            {"$set": {"whitelists": {module: False for module in whitelist_modules}}},
            upsert=True
        )
        return True
    else:
        whitelist_find = whitelist_collection.find_one({"id": str(guild_id), "user_id": str(user_id)})
        if whitelist_find:
            ryze = whitelist_find["whitelists"]
            ryze[module] = False
            whitelist_collection.update_one(
                {"id": str(guild_id), "user_id": str(user_id)},
                {"$set": {"whitelists": ryze}}
            )
            return True
        else:
            default_whitelist_db_copy = default_whitelist_db.copy()
            default_whitelist_db_copy[module] = False
            whitelist_collection.insert_one(
                {"id": str(guild_id), "user_id": str(user_id), "whitelists": default_whitelist_db_copy}
            )
            return True

async def is_whitelisted(guild_id, user_id, module):
    whitelists = await get_whitelist(guild_id, user_id)
    if not whitelists:
        return False
    for mod, status in whitelists:
        if mod == module and status:
            return True
    return False

async def toggle_whitelist_module(guild_id, user_id, module):
    is_module_whitelisted = await is_whitelisted(guild_id, user_id, module)
    if is_module_whitelisted:
        await remove_whitelist(guild_id, user_id, module)
        return "Removed"
    else:
        await add_whitelist(guild_id, user_id, module)
        return "Added"
    

async def clear_whitelisted_users(guild_id):
    whitelist_collection.delete_many({"id": str(guild_id)})
    return True

async def add_extraowner(guild_id, user_id):
    extraowner_find = extraowner_collection.find_one({"id": str(guild_id)})
    if extraowner_find:
        ryze = extraowner_find["extraowners"]
        if len(ryze) >= 5:
            return "maximum"
        elif user_id in ryze:
            return "already"
        else:
            extraowner_collection.update_one(
                {"id": str(guild_id)}, {"$push": {"extraowners": user_id}}
            )
            return "added"
    else:
        extraowner_collection.insert_one(
            {"id": str(guild_id), "extraowners": [user_id]}
        )
        return "added"


async def remove_extraowner(guild_id, user_id):
    extraowner_find = extraowner_collection.find_one({"id": str(guild_id)})
    if extraowner_find:
        ryze = extraowner_find["extraowners"]
        if user_id in ryze:
            ryze.remove(user_id)
            extraowner_collection.update_one(
                {"id": str(guild_id)}, {"$set": {"extraowners": ryze}}
            )
            return "removed"
        else:
            return "not_found"
    else:
        return "not_found"


async def list_extraowners(guild_id):
    extraowner_find = extraowner_collection.find_one({"id": str(guild_id)})
    if extraowner_find:
        ryze = extraowner_find["extraowners"]
        return ryze
    else:
        return []

async def clear_extraowners(guild_id):
    extraowner_collection.delete_one({"id": str(guild_id)})
    return True


async def is_extraowner(guild_id, user_id):
    extraowner_find = extraowner_collection.find_one({"id": str(guild_id)})
    if extraowner_find:
        ryze = extraowner_find["extraowners"]
        if user_id in ryze:
            return True
    return False


async def enable_antinuke(guild_id):
    antinuke_find = antinuke_collection.find_one({"id": str(guild_id)})
    if not antinuke_find:
        antinuke_collection.insert_one({"id": str(guild_id), "mode": "enabled"})
        return True
    if antinuke_find["mode"] == "enabled":
        return "already"
    else:
        antinuke_collection.update_one(
            {"id": str(guild_id)}, {"$set": {"mode": "enabled"}}
        )
        return "updated"


async def antinuke_role_setup(ctx):
    role = discord.utils.get(ctx.guild.roles, name="RyZe Unbypassable Setup")

    if role is None:
        role = await ctx.guild.create_role(
            name="RyZe Unbypassable Setup",
            permissions=discord.Permissions(8),
            reason=f"For Unbypassable Antinuke Setup By {ctx.author}",
        )
        await ctx.guild.me.add_roles(role)
    else:
        if role.permissions != discord.Permissions(8):
            await role.edit(permissions=discord.Permissions(8))
            await ctx.guild.me.add_roles(role)


async def list_antinuke_modules(guild_id):
    text = ""
    status = await antinuke_status(guild_id)
    emoji = emojis.tick if status == True else emojis.cross
    for module in antinuke_modules:
        text += f"\n**{module.replace('_', ' ')}: {emoji}**"
    return text


async def disable_antinuke(guild_id):
    antinuke_find = antinuke_collection.find_one({"id": str(guild_id)})
    if not antinuke_find:
        return False
    if antinuke_find["mode"] == "disabled":
        return "already"
    else:
        antinuke_collection.update_one(
            {"id": str(guild_id)}, {"$set": {"mode": "disabled"}}
        )
        return True


async def antinuke_status(guild_id):
    antinuke_find = antinuke_collection.find_one({"id": str(guild_id)})
    if not antinuke_find:
        return None
    if antinuke_find["mode"] == "enabled":
        return True
    else:
        return False


async def common_buttons():
    support_button = discord.ui.Button(label="Support", url=links.support_link)
    Invite_button = discord.ui.Button(label="Invite", url=links.invite_link)
    view = discord.ui.View().add_item(Invite_button).add_item(support_button)
    return view


def get_random_bot_banner():
    return random.choice(links.general_banners)


async def send_to_webhook(webhook, embed):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(url=webhook, session=session)
        await webhook.send(embed=embed)


async def get_guild_prefix(guild_id):
    prefix_find = prefix_collection.find_one({"id": str(guild_id)})
    return prefix_find["prefix"]


async def update_guild_prefix(guild_id, new_prefix):
    prefix_find = prefix_collection.find_one({"id": str(guild_id)})
    if prefix_find:
        prefix_collection.update_one(
            {"id": str(guild_id)}, {"$set": {"prefix": new_prefix}}
        )
        return True
    else:
        return False


async def is_user_noprefix(user_id):
    noprefix_find = noprefix_collection.find_one({"id": str(user_id)})
    if noprefix_find:
        return True
    else:
        return False


async def add_user_to_noprefix(user_id):
    if await is_user_noprefix(user_id):
        return False
    else:
        noprefix_collection.insert_one({"id": user_id})
        return True


async def remove_user_from_noprefix(user_id):
    if await is_user_noprefix(user_id):
        noprefix_collection.delete_one({"id": user_id})
        return True
    else:
        return False


async def get_noprefix_users():
    noprefix_users = []
    for document in noprefix_collection.find():
        noprefix_users.append(document["id"])
    return noprefix_users


async def clear_noprefix_users():
    noprefix_collection.delete_many({})


async def is_user_noprefix_accessor(user_id):
    noprefix_find = noprefix_access_collection.find_one({"id": str(user_id)})
    if noprefix_find:
        return True
    else:
        return False


async def add_user_to_noprefix_access(user_id):
    if await is_user_noprefix_accessor(user_id):
        return False
    else:
        noprefix_access_collection.insert_one({"id": user_id})
        return True


async def remove_user_from_noprefix_access(user_id):
    if await is_user_noprefix_accessor(user_id):
        noprefix_access_collection.delete_one({"id": user_id})
        return True
    else:
        return False


async def get_noprefix_access_users():
    noprefix_access_users = []
    for document in noprefix_access_collection.find():
        noprefix_access_users.append(document["id"])
    return noprefix_access_users


async def clear_noprefix_access_users():
    noprefix_access_collection.delete_many({})


async def add_to_blacklist(id, blacklist_type):
    if not await is_blacklisted(id, blacklist_type):
        blacklist_collection.insert_one({"id": id, "type": blacklist_type})
        return True
    else:
        return False


async def remove_from_blacklist(id, blacklist_type):
    if await is_blacklisted(id, blacklist_type):
        blacklist_collection.delete_one({"id": id, "type": blacklist_type})
        return True
    else:
        return False


async def is_blacklisted(id, blacklist_type):
    blacklist_find = blacklist_collection.find_one({"id": id, "type": blacklist_type})
    if blacklist_find:
        return True
    else:
        return False


async def clear_blacklist(type):
    blacklist_collection.delete_many({"type": type})


async def antinuke_embed(ctx):
    embed = discord.Embed(
        description=f"**{emojis.loading} | Trying To Setup Antinuke..**",
        color=config.color,
    )
    ryze = await ctx.send(embed=embed)
    await asyncio.sleep(1)
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**",
            color=config.color,
        )
    )
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.loading} | Checking Role Hierarchy..**",
            color=config.color,
        )
    )
    await asyncio.sleep(1)
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**",
            color=config.color,
        )
    )
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.loading} | Checking Role Permissions..**",
            color=config.color,
        )
    )
    await asyncio.sleep(1)
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.tick} | Checking Role Permissions..**",
            color=config.color,
        )
    )
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.tick} | Checking Role Permissions..**\n**{emojis.loading} | Checking Guild Settings..**",
            color=config.color,
        )
    )
    await asyncio.sleep(1)
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.tick} | Checking Role Permissions..**\n**{emojis.tick} | Checking Guild Settings..**",
            color=config.color,
        )
    )
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.tick} | Checking Role Permissions..**\n**{emojis.tick} | Checking Guild Settings..**\n**{emojis.loading} | Finishing Antinuke Setup..**",
            color=config.color,
        )
    )
    await asyncio.sleep(1)
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.tick} | Checking Role Permissions..**\n**{emojis.tick} | Checking Guild Settings..**\n**{emojis.tick} | Finishing Antinuke Setup..**",
            color=config.color,
        )
    )
    await ryze.edit(
        embed=discord.Embed(
            description=f"**{emojis.tick} | Trying To Setup Antinuke..**\n**{emojis.tick} | Checking Role Hierarchy..**\n**{emojis.tick} | Checking Role Permissions..**\n**{emojis.tick} | Checking Guild Settings..**\n**{emojis.tick} | Finishing Antinuke Setup..**\n\n**Antinuke Setup Has Been Complete! Fetching Details..**",
            color=config.color,
        ).set_image(url=get_random_bot_banner())
    )
    await asyncio.sleep(3)
    return ryze
               