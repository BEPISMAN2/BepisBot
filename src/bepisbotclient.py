import asyncio
import discord
import traceback
import util

from discord.ext import commands
from discord.ext.commands import errors

from os.path import join as opj

class BepisBotClient(commands.Bot):
    JSON_PATH = "jsondata"

    async def on_ready(self):
        print("Login successful.")
        print("User Name:  %s" % self.user.name)
        print("User ID:    %s" % self.user.id)

        self.blacklistUpdated = None
        self.disabledCommandsUpdated = None

        self.blacklist = {}
        self.disabledCommands = {}

        for guild in self.guilds:
            self.blacklist[str(guild.id)] = util.load_js(opj(self.JSON_PATH, \
                        "blacklist-%s" % guild.id), returnListIfEmpty=True)
            self.disabledCommands[str(guild.id)] = util.load_js(opj(self.JSON_PATH, \
                        "disabled-commands-%s.json" % guild.id),
                        returnListIfEmpty=True)

            self.add_check(self.checkIfBlacklisted, call_once = True)
            self.add_check(self.checkIfEnabled, call_once = True)
        print("Blacklist and Disabled Command Dictionaries loaded.")
            
    def checkIfBlacklisted(self, ctx):
        guildBlacklist = self.blacklist[str(ctx.guild.id)]
        print(guildBlacklist)

        if str(ctx.author.id) in guildBlacklist:
            return False
        return True

    def checkIfEnabled(self, ctx):
        if ctx.guild != None:  # not a DM
            for command in self.disabledCommands[str(ctx.guild.id)]:
                if "%s%s" % (self.command_prefix, command) in \
                    ctx.message.content:
                    return False
        
        return True

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_command_error(self, ctx, exception):
        eType = type(exception)
        if (eType == errors.MissingRequiredArgument or \
           eType == errors.BadArgument):
            if ctx.command.hidden:
                return

            helpList = await self.formatter.format_help_for(ctx, ctx.command)

            for helpStr in helpList:
                await ctx.send(helpStr)
        elif eType == errors.CommandNotFound:
            pass
        elif eType == errors.NoPrivateMessage:
            await ctx.author.send("Sorry, but I can't do that command in DMs.")
        else:
            eText = ""
            eList = traceback.format_exception(None, exception, None)
            for line in eList:
                eText += line
            await ctx.send("```%s```" % eText)