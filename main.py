from discord.ext import commands
from dictionary_commands import DictionaryFunctions

bot = commands.Bot(command_prefix='~')


@bot.event
async def on_ready():
    print('logged in as {0.user.name}'.format(bot))


bot.add_cog(DictionaryFunctions(bot))

bot.run('OTEwNTAwNTU1MzkzMjA0MjI1.YZTvuA.1a8Ajc10virg0LESOZaiM7UzTFc')
