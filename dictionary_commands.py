from discord.ext import commands
import requests


def get_data(msg):
    response = requests.request("GET", "https://api.dictionaryapi.dev/api/v2/entries/en/" + msg)
    return response.json()


def send_def(data):
    output = ''
    output += '**{}**\n\n'.format(data[0]['word'])
    for i in data[0]['meanings']:
        output += '\t{}\n\t\tDefinition: *{}*\n\n'.format(
            i['partOfSpeech'],
            i['definitions'][0][
                'definition']
        )
    return output


def send_all(data):
    output = ''
    output += '**{}**\n\n'.format(data[0]['word'])
    for i in data[0]['meanings']:
        if len(i['definitions'][0]['synonyms']) == 0:
            output += '\t{}\n\t\tDefinition: *{}*\n\t\tExample: *{}*\n\n'.format(
                i['partOfSpeech'],
                i['definitions'][0][
                    'definition'],
                i['definitions'][0][
                    'example']
            )
        elif len(i['definitions'][0]['synonyms']) < 5:
            syn = ', '.join(i['definitions'][0]['synonyms'])
            output += '\t{}\n\t\tDefinition: *{}*\n\t\tExample: *{}*\n\t\tSynonyms: *{}*\n\n'.format(
                i['partOfSpeech'],
                i['definitions'][
                    0][
                    'definition'],
                i['definitions'][
                    0][
                    'example'],
                syn
            )
        else:
            syn = ', '.join(i['definitions'][0]['synonyms'][:4])
            output += '\t{}\n\t\tDefinition: *{}*\n\t\tExample: *{}*\n\t\tSynonyms: *{}*\n\n'.format(
                i['partOfSpeech'],
                i['definitions'][
                    0][
                    'definition'],
                i['definitions'][
                    0][
                    'example'],
                syn
            )

    return output


def send_examples(data):
    output = ''
    output += '**{}**\n\n'.format(data[0]['word'])
    for i in data[0]['meanings']:
        output += '\t{}\n\t\tExample: *{}*\n\n'.format(
            i['partOfSpeech'],
            i['definitions'][0][
                'example']
        )
    return output


def send_syn(data):
    output = ''
    output += '**{}**\n\tSynonyms: '.format(data[0]['word'])
    for i in data[0]['meanings']:
        if len(i['definitions'][0]['synonyms']) == 0:
            pass
        elif len(i['definitions'][0]['synonyms']) < 5:
            syn = ', '.join(i['definitions'][0]['synonyms'])
            output += syn
        else:
            syn = ', '.join(i['definitions'][0]['synonyms'][:4])
            output += syn
    if output == '**{}**\n\tSynonyms: '.format(data[0]['word']):
        output = 'Sorry, we couldn\'t find any.'
    return output


def send_pos(data):
    output = ''
    output += 'This word, **{}** can act as '.format(data[0]['word'])
    output += ', '.join([i['partOfSpeech'] for i in data[0]['meanings']])
    return output


class DictionaryFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='all', brief='Gives all definitions, examples and synonyms of the word',
                      description='Replies with Pos, definition, example and synonyms of the word. For pronunciation use ~pronounce <word>')
    async def all_info(self, ctx, word):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        async with ctx.typing():
            data = get_data(word)
            output = send_all(data)
        await ctx.channel.send(output)

    @commands.command(name='pronounce', brief='Uses Discord tts to pronounce the word',
                      description='Uses Discord tts to pronounce the word. Permission for tts messages needed for some features of this command to work. For full details and definitions use ~all<word>')
    async def pronounce(self, ctx, word):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        async with ctx.typing():
            data = get_data(word)
            output = ''
            output += '{}'.format(data[0]['word'])
        await ctx.send(output, tts=True)
        output = data[0]['phonetics'][0]['text']
        await ctx.send(output)

    @commands.command(name='def', brief='Gives only the definitions of the word',
                      description='Only gives definitions of word under different pos. For all details use ~all <word>')
    async def only_def(self, ctx, word):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        async with ctx.typing():
            data = get_data(word)
            output = send_def(data)
        await ctx.channel.send(output)

    @commands.command(name='syn', brief='Gives synonyms of the word',
                      description='Only gives synonyms of the word. For all details use ~all <word>')
    async def syn(self, ctx, word):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        async with ctx.typing():
            data = get_data(word)
            output = send_syn(data)
        await ctx.channel.send(output)

    @commands.command(name='example', brief='Gives examples for the usage of the word',
                      description='Only shows examples of word. For full details use ~all<word>')
    async def example(self, ctx, word):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        async with ctx.typing():
            data = get_data(word)
            output = send_examples(data)
        await ctx.channel.send(output)

    @commands.command(name='pos', brief='Lists all Parts of speech of this word',
                      description='Only Lists parts of speech of the word. For full details use ~all <word>')
    async def PartsOfSpeech(self, ctx, word):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        async with ctx.typing():
            data = get_data(word)
            output = send_pos(data)
        await ctx.channel.send(output)
