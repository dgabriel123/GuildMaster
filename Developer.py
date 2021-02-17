from discord.ext import commands
import discord
import ast
import time
import sys


class TestError(Exception):
    """Test exception to test error handling. Can be ignored."""
    pass


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected to Discord with ID {}.".format(self.bot.user.id))
        print("~~~~~~~~~~~~~~~~~~~~~GM~Logs~~~~~~~~~~~~~~~~~~~~~")

    @commands.is_owner()
    @commands.command(name="reload")
    async def reload_extensions(self, ctx):
        embed = discord.Embed(title="Reloading...", color=self.bot.YELLOW)
        embed.set_footer(text="Please wait.")
        message = await ctx.send(embed=embed)
        print("Reloading...")

        before = time.monotonic()

        self.bot.reload_extension("Developer")
        self.bot.reload_extension("General")
        self.bot.reload_extension("Leveling")
        self.bot.reload_extension("Information")
        self.bot.reload_extension("Fun")
        self.bot.reload_extension("Interactions")

        reload_time = round((time.monotonic() - before) * 1000, 1)

        success_embed = discord.Embed(title="Success!", description="GuildMaster reloaded in {}ms.".format(reload_time), color=self.bot.GREEN)
        success_embed.set_footer(text="Requested by {}.".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await message.edit(embed=success_embed)
        print("Reloaded!")
    
    @commands.is_owner()
    @commands.command()
    async def shutdown(self, ctx):
        print("Shutdown initiated from user \"{}\"".format(ctx.message.author))
        await self.bot.logout()

    @commands.command()
    async def error(self, ctx):
        raise TestError

    # VERY BUGGY
    @commands.is_owner()
    @commands.command()
    async def exec(self, ctx, *, code):
        before = time.monotonic()
        try:
            print("attemting as normal code")
            eval(compile(code, "<string>", mode="exec"))
        except SyntaxError:
            try:
                print("attempting as async code")
                await eval(compile(code, "<string>", mode="exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT))
            except:
                await ctx.send("Error: {}".format(sys.exc_info[0]))
        except:
            await ctx.send("Error: {}".format(sys.exc_info[0]))
                
        exec_time = before - time.monotonic()

    @commands.command()
    async def token(self, ctx):
        await ctx.send("NzY5NzI0MjM0MzkyOTI4Mjc3.X5TLjg.dKHDuWCwbKG_R3-RYT-HvKa17IE")


def setup(bot):
    print("Loading Developer extension...")
    bot.add_cog(Developer(bot))