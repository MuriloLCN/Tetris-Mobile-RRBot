import discord.errors

import texts

async def check(message: discord.Message):
    """
    Main check function

    :param client: Client context
    :param message: Message context
    """

    if message.content.startswith('$tasks'):
        await message.channel.send(texts.tasks)
        return

    if message.content.startswith('$bonus'):
        await message.channel.send(texts.bonus)
        return

    if message.content.startswith('$guides'):
        await message.channel.send(texts.guides)
        return

    if message.content.startswith('$fullguide'):
        await message.channel.send("You can find the full guide in here:\n"
                                   "https://github.com/MuriloLCN/Tetris-Mobile-RRBot/blob/main/README.md")
        return
