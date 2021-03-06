import logging
import typing
from pathlib import Path

import discord
from discord.ext import commands, tasks
from yarl import URL

from bot.models.ManualCheck import ManualCheck
from bot.models.NewsParser import NewsParser
from bot.models.Overwatch import OWPatch
from bot.models.Reddit import RedditJSON, RedditPost, RedditPRAW
from bot.utils.Constants import Channels


class PatchRundownParser(NewsParser):
    def __init__(self, bot):
        super().__init__(bot)
        self.postjsonURL = URL("https://www.reddit.com/user/itsjieyang/submitted.json")
        self.postchannelID = Channels.ow
        self.logJSONpath = Path("./log/postedRundowns.JSON")

        self._parsername = "OW Rundown(s)"
        self._loadconverter = URL
        self._saveconverter = str
        self._comparator = "contentURL"

    async def getpatchrundowns(self, jsonURL: URL = None):
        """
        Return a list of RedditPost objects generated from Patch Notes submissions by /u/itsjieyang
        to /r/Overwatch
        """
        jsonURL = jsonURL if jsonURL is not None else self.postjsonURL

        prawinstance = RedditPRAW()
        if prawinstance.isauthenticated:
            postobjs = [
                RedditPost.fromPRAW(submission)
                for submission in prawinstance.getnewusersubmissions("itsjieyang")
            ]
        else:
            postobjs = await RedditJSON.asyncfromJSON(jsonURL)

        logging.info(f"Found {len(postobjs)} submission(s) by /u/itsjieyang")

        patchposts = []
        for postobj in postobjs:
            # So far, patch notes rundowns we want are from /r/Overwatch and start with "patch"
            if postobj.subreddit == "Overwatch" and "patch" in postobj.title.lower():
                patchposts.append(postobj)

        logging.info(f"Found {len(patchposts)} {self._parsername}")
        return patchposts

    async def postembed(self, postobj: RedditPost = None, channelID: int = None):
        """
        Generate & send an embed for the input RedditPost object, built from /u/itsjieyang's
        Reddit submissions

        There are 2 message formats:
            * Gfycat: Generate an embed with the .gif version of the gfy embedded
            * Youtube & Streamable: Use a regular message and defer to Discord's embed
        """
        channelID = channelID if channelID is not None else self.postchannelID
        postchannel = self.bot.get_channel(channelID)

        host = postobj.contentURL.host.lower()
        if "gfycat.com" in host:
            if postobj is None:
                raise ValueError("No post object provided")
            if not isinstance(postobj, RedditPost):
                raise TypeError(
                    f"Invalid post type provided: '{type(postobj)}', input must be RedditPost"
                )

            postembed = discord.Embed(
                title=postobj.title,
                color=discord.Color(0x9C4AF7),
                description=(
                    f"[View Full Resolution]({postobj.contentURL})\n\n"
                    f"[View Reddit Post]({postobj.permalink})"
                ),
            )
            postembed.set_author(
                name="/u/itsjieyang", url=URL("https://www.reddit.com/user/itsjieyang")
            )
            postembed.set_thumbnail(
                url=URL(
                    "https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png"
                )
            )
            postembed.set_image(url=self.gfygif(postobj.contentURL))
            postembed.set_footer(text="Overwatch, it's Ameizing!")
            await postchannel.send("A new patch gif has been posted!", embed=postembed)
        else:
            msg = (
                f"A new patch rundown video has been posted!\n{postobj.contentURL}\n\n"
                f"View the full Reddit post here:\n<{postobj.permalink}>"
            )
            await postchannel.send(msg)

    async def patchcheck(self):
        posts = await self.getpatchrundowns()
        await super().patchcheck(posts)

    @staticmethod
    def gfygif(inURL: typing.Union[str, URL]) -> URL:
        """
        Build a direct gif link from a gfycat URL

        e.g. https://gfycat.com/flippantvariablediplodocus
             to
             https://giant.gfycat.com/FlippantVariableDiplodocus.gif

        Returns a string
        """
        gfyID = URL(inURL).path.replace("/", "")
        return URL.build(scheme="https", host="giant.gfycat.com", path=f"/{gfyID}.gif")


class PatchNotesParser(NewsParser):
    def __init__(self, bot):
        super().__init__(bot)
        self.patchesURL = URL("https://playoverwatch.com/en-us/news/patch-notes/pc")
        self.postchannelID = Channels.ow
        self.logJSONpath = Path("./log/postedOWpatches.JSON")

        self._parsername = "OW Patch(es)"
        self._loadconverter = str
        self._saveconverter = str
        self._comparator = "verpatch"

    async def postembed(self, postobj: OWPatch = None, channelID: int = None):
        channelID = channelID if channelID is not None else self.postchannelID
        if postobj is None:
            raise ValueError("No post object provided")
        if not isinstance(postobj, OWPatch):
            raise TypeError(
                f"Invalid object type provided: '{type(postobj)}', input must be OWPatch"
            )

        postchannel = self.bot.get_channel(channelID)

        postembed = discord.Embed(
            title=str(postobj),
            color=discord.Color(0x9C4AF7),
            description=f"[View full patch notes]({postobj.patchURL})",
        )
        postembed.set_author(
            name="Blizzard",
            url=URL("https://playoverwatch.com/en-us/news/patch-notes/pc"),
            icon_url=URL("http://us.blizzard.com/static/_images/logos/blizzard.jpg"),
        )
        postembed.set_thumbnail(
            url=URL(
                "https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png"
            )
        )
        postembed.set_image(url=postobj.bannerURL)
        postembed.set_footer(text="Patch Notes Provided by BlizzTrack")
        await postchannel.send(
            "A new Overwatch Patch has been released!", embed=postembed
        )

    async def patchcheck(self):
        posts = await OWPatch.asyncfromURL(self.patchesURL)
        await super().patchcheck(posts)


class OverwatchHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.rundown_parser = PatchRundownParser(self.bot)
        self.patch_parser = PatchNotesParser(self.bot)
        self.overwatch_patch_check_timer.start()

    def cog_unload(self):
        self.overwatch_patch_check_timer.cancel()

    @tasks.loop(hours=1)
    async def overwatch_patch_check_timer(self):
        """Task loop for fetching OW game updates"""
        await self.rundown_parser.patchcheck()
        await self.patch_parser.patchcheck()

    @overwatch_patch_check_timer.before_loop
    async def before_patch_check(self):
        await self.bot.wait_until_ready()

    @commands.command(hidden=True)
    async def checkOWrundown(self, ctx: commands.Context):
        await ManualCheck.check(
            ctx=ctx,
            toinvoke=PatchRundownParser(self.bot).patchcheck,
            commandstr="OW Patch Rundown",
        )

    @commands.command(hidden=True)
    async def checkOWpatch(self, ctx: commands.Context):
        await ManualCheck.check(
            ctx=ctx,
            toinvoke=PatchNotesParser(self.bot).patchcheck,
            commandstr="OW Patch",
        )


def setup(bot):
    bot.add_cog(OverwatchHelper(bot))
    logging.info("OverwatchHelper Cog loaded")
