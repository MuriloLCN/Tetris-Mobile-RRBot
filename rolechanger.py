import datahandling
import re
import discord

# Triggers every time a reaction is added
async def check(client, payload, data):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    user = payload.member
    reaction = payload.emoji

    curId = message.guild.id
    serverData = datahandling.getserverdata(curId, data)

    if user.id == client.user.id:
        return

    if str(message.id) not in serverData.rolechangerids:
        return

    # Since the roles are meant to alternate, meaning a user can only have one of the available roles at any given time,
    # the role that will be given is stored in 'role', and all others are stored in 'removeRoles'. This way we can
    # remove the other roles before giving a new one, thus making sure the users can alternate.
    rows = str(message.content).split('\n')
    removeRoles = []
    isOption = False
    role = ''

    for row in rows[1:]:
        if str(reaction) in str(row):
            role = row.split(':')[1]
            isOption = True
        else:
            try:
                removeRoles.append(row.split(':')[1])
            except IndexError:
                continue

    if isOption:

        # If there are no digits, it means that it's either @here or @everyone, which cannot be given
        # I hate using regex but there was no real escape here. Some roles had '&', others '@', etc.
        if re.sub('\D', '', role) != '':
            role = re.sub('\D', '', role)
        else:
            await channel.send("This is not a role that can be given: " + str(role))
            return

        role = int(role)
        role = discord.utils.get(client.get_guild(message.guild.id).roles, id=role)

        try:
            await user.add_roles(role)
        except discord.errors.Forbidden:
            # This happened quite a lot because people forget that the roles need to be below the bot's perms level
            # in order for this to work. It's not magic!!
            await message.channel.send("I don't have permission to give this role: " + str(role))
            return
        except AttributeError:
            await message.channel.send("This is not a role that can be given: " + str(role))
            return

        # Remove the role from the other options
        for role in removeRoles:
            role = re.sub('\D', '', role)

            if role == '':
                continue

            role = int(role)
            role = discord.utils.get(client.get_guild(message.guild.id).roles, id=role)

            try:
                await user.remove_roles(role)
            except discord.errors.Forbidden:
                continue
            except AttributeError:
                continue

    else:
        await message.channel.send("No roles found for that changer")
        return
