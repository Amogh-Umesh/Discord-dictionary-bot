from discord.ext import commands
from dictionary_commands import DictionaryFunctions
import os

bot = commands.Bot(command_prefix='~')


@bot.event
async def on_ready():
    print('logged in as {0.user.name}'.format(bot))


bot.add_cog(DictionaryFunctions(bot))

bot.run(os.environ['DISCORD_TOKEN'])
