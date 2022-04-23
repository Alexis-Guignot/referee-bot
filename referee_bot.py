import discord
import os
import texttable
import os

token = os.environ.get('BOT_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print ('We Gucci with {0.user}'.format(client))

@client.event
async def on_message(message):
	if (message.content == 'Allo l\'arbitre'):
		await message.channel.send('Je demande à la var')

		text_channel_list = get_all_channels(message)
		warning_list = {}
		for channel in text_channel_list:
			try:
				async for msg in channel.history(limit=None):
					if (len(msg.reactions) > 0):
						for reaction in msg.reactions:
							if (reaction.emoji in ('🟥', '🟨', '🟩')):
								if (msg.author not in warning_list):
									warning_list[msg.author] = {'🟥':0, '🟨':0, '🟩':0}
								warning_list[msg.author][reaction.emoji] += reaction.count
			except:
				print (channel.name)
		tableObj = texttable.Texttable()
		tableObj.set_cols_align(["l", "l", "c", "c", "c"])
		tableObj.set_cols_dtype(["t", "t", "t", "t", "t"])
		tableObj.set_cols_valign(["m", "m", "m", "m", "m"])
		table_array = []
		table_array.append(["Classement", "Utilisateur", "🟥", "🟨", "🟩"])

		i = 1
		while (len(warning_list) > 0):
			my_max = 0
			for user in warning_list:
				my_max = max(my_max, warning_list[user]['🟥'])
				if (my_max == warning_list[user]['🟥']):
					user_max = user
			table_array.append([i, user_max.name, warning_list[user_max]["🟥"], warning_list[user_max]["🟨"], warning_list[user_max]["🟩"]])
			del warning_list[user_max]
			i += 1
		tableObj.add_rows(table_array)
		print((tableObj.draw()))
		await message.channel.send("```" + tableObj.draw() + "```")


def get_all_channels(message):
	text_channel_list = []
	for channel in message.guild.channels:
	    if str(channel.type) == 'text':
	        text_channel_list.append(channel)
	return text_channel_list

def get_color(reaction):
	emoji = reaction.emoji
	if (emoji == '🟥'):
		return 'red'
	if (emoji == '🟨'):
		return 'yellow'
	if (emoji == '🟩'):
		return 'green'

token = os.environ.get('BOT_TOKEN')
client.run(token)