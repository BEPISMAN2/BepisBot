import asyncio
import discord
import requests
import util
import os

from discord.ext import commands
from cogs.base import Base

class BotCmd(Base):
	def __init__(self, bot):
		conf = util.load_js("config.json")
		self.mod_roles= conf["moderator-roles"]
		super().__init__(bot)

	@commands.command(pass_context = True)
	async def deleteMessages(self, ctx, number : int = 10):
		"""Delete the number of messages specified.  Deletes 10 by default.  This requires special perms."""
		perms = await util.check_perms(self, ctx)
		if not perms:
			return

		await self.bot.purge_from(ctx.message.channel, limit = number)
		msg = await self.bot.say("Deleted {} messages.".format(number))
		await asyncio.sleep(5)
		await self.bot.delete_message(msg)

	@commands.command(pass_context = True)
	async def setAvatar(self, ctx, link : str):
		"""Set the bot's avatar."""
		perms = await util.check_perms(self, ctx)
		if not perms:
			return

		await self.bot.send_typing(ctx.message.channel)
		image = requests.get(link)

		try:
			await self.bot.edit_profile(avatar = image.content)
			await self.bot.say("How do I look?")
		except discord.errors.InvalidArgument:
			await self.bot.say("That image type is unsupported!")
		except:
			await self.bot.say("Something went wrong.  Sorry.")

	@commands.command(pass_context = True)
	async def setUsername(self, ctx, name : str):
		"""Set the bot's username.  This requires special perms."""
		perms = await util.check_perms(self, ctx)
		if not perms:
			return

		try:
			await self.bot.edit_profile(username = name)
			await self.bot.say("Henceforth, I shall be known as {}!".format(name))
		except discord.errors.HTTPException:
			await self.bot.say("Hrm?  Something came up; the profile can't be set.")
		except:
			await self.bot.say("Something went wrong.  Sorry.")

	@commands.command(pass_context = True)
	async def updateBot(self, ctx):
		"""Update the bot to the latest version.  This requires special perms."""
		perms = await util.check_perms(self, ctx)
		if not perms:
			return

		await self.bot.say("Updating the bot...")
		os.system("git fetch origin")
		os.system("git checkout --force origin/master")
		await self.bot.say("Bot is updated!  Restarting...")
		await self.bot.close()
		os.system("python3.5 main.py")

	@commands.command()
	async def setPlaying(self, playing):
		"Set the bot's playing status."""
		if "emibot" in playing.lower():
			await self.bot.say("Haha.  Nice try there.")
			return

		if ( "clone" in playing.lower() ) and ( "bot" in playing.lower() ):
			await self.bot.say("Haha.  Nice try there.")
			return

		if ( "emily" in playing.lower() ) and ( "bot" in playing.lower() ):
			await self.bot.say("Haha.  Nice try there.")
			return

		await self.bot.change_presence(game = discord.Game(name = playing))
		await self.bot.say("Now playing {}".format(playing))

	@commands.command()
	async def inviteLink(self):
		"""Invite the bot to your own server!  Sends you a DM with the invite link."""
		client_id = util.load_js("config.json")["client-id"]
		await self.bot.whisper("https://discordapp.com/oauth2/authorize?&client_id={0}&scope=bot&permissions=0".format(client_id))

	@commands.command(pass_context = True)
	async def say(self, ctx):
		"""Have the bot say something.  Chances are, you're gonna make it say something stupid."""
		thing = ctx.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:]

		if ctx.message.author.id == self.bot.user.id:
			return

		await self.bot.say(thing)

	@commands.command(pass_context = True)
	async def whisper(self, ctx):
		"""Make it so that it looks like the bot said something on its own."""
		thing = ctx.message.content[len(ctx.prefix) + len(ctx.command.name) + 1:]

		if ctx.message.author.id == self.bot.user.id:
			return

		await self.bot.delete_message(ctx.message)
		await self.bot.say(thing)
		
	@commands.command(pass_context = True)
	async def setNick(self, ctx):
		"""Nickname test"""
		nick = ctx.message.content

		if ctx.message.author.id == self.bot.user.id:
			return

		await self.bot.change_nickname(self.bot.user, nick)
		
def setup(bot):
	bot.add_cog(BotCmd(bot))
