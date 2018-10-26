import re
import typing
from datetime import datetime

import aiohttp
import requests
from bs4 import BeautifulSoup
from yarl import URL


class OWPatch:
    def __init__(
        self,
        patchref: str = None,
        ver: str = None,
        verpatch: str = None,
        patchdate: datetime = None,
        patchURL: URL = None,
        bannerURL: URL = None,
    ):
        """
        Helper object to represent Blizzard's Overwatch Patch notes
        """
        defaultpatchURL = URL("https://playoverwatch.com/en-us/news/patch-notes/pc")
        defaultbannerURL = URL(
            "https://gear.blizzard.com/media/wysiwyg/default/logos/ow-logo-white-nds.png"
        )

        self.patchref = patchref
        self.ver = ver
        self.patchdate = patchdate
        self.verpatch = verpatch
        self.patchURL = patchURL if patchURL is not None else defaultpatchURL
        self.bannerURL = bannerURL if bannerURL is not None else defaultbannerURL

    def __repr__(self):
        return f"OWPatch: v{self.verpatch}, Released: {datetime.strftime(self.patchdate, '%Y-%m-%d')}"

    @staticmethod
    def fromURL(
        inURL: typing.Union[str, URL] = URL(
            "https://playoverwatch.com/en-us/news/patch-notes/pc"
        )
    ) -> typing.List:
        """
        Return a list of OWPatch objects from Blizzard's Patch Notes
        """
        if not inURL:
            raise ValueError("No URL provided")
        inURL = URL(inURL)

        r = requests.get(inURL).text

        return OWPatch._parseOWpatchHTML(r)

    @staticmethod
    async def asyncfromURL(
        inURL: typing.Union[str, URL] = URL(
            "https://playoverwatch.com/en-us/news/patch-notes/pc"
        )
    ) -> typing.List:
        """
        This function is a coroutine

        Return a list of OWPatch objects from Blizzard's Patch Notes
        """
        if not inURL:
            raise ValueError("No URL provided")
        inURL = URL(inURL)

        async with aiohttp.ClientSession() as session:
            async with session.get(inURL) as resp:
                r = await resp.text()

        return OWPatch._parseOWpatchHTML(r)

    @staticmethod
    def _parseOWpatchHTML(inHTML: str) -> typing.List:
        soup = BeautifulSoup(inHTML, "html.parser")

        # Iterate over patches
        patches = soup.find_all("div", class_="patch-notes-patch")

        patchobjs = []
        for patch in patches:
            # Get patch reference ID
            patchref = patch.get("id")
            patchref_num = patchref.split("-")[-1]  # Get numeric reference to build BlizzTrack link later

            # Get version number from sidebar using patch reference ID
            sidebaritem = soup.select_one(f"a[href=#{patchref}]").parent
            ver = sidebaritem.find("h3").get_text().split()[-1]
            
            # Generate full reference from version number & patch reference because
            # Blizzard reuses version numbers for some patches
            # e.g. 1.29.0.1.51948 and 1.29.0.1.51575
            verpatch = f"{ver}.{patchref_num}"

            # Get date
            dateheader = patch.find("h2", class_="HeadingBanner-header")
            if dateheader:
                patchdate = datetime.strptime(dateheader.get_text(), "%B %d, %Y")
            else:
                # In the event there is no banner, the date is instead embedded in <h1>Overwatch Patch Notes – June 5, 2018</h1>
                # Since we already have the sidebar entry, it's slightly simpler to get the date from that instead
                patchdate = datetime.strptime(
                    sidebaritem.find("p").get_text(), "%m/%d/%Y"
                )

            # Get patch banner
            # If there is a banner for the patch, it's embedded in the 'style' portion of the '.HeadingBanner' div
            # e.g. <div class="HeadingBanner" style="background-image: url(https://link/to.jpg);">
            patchbannerdiv = patch.select_one(".HeadingBanner")
            if patchbannerdiv:
                expr = r"url\(\"?([^\"]+)\"?\)"
                m = re.search(expr, patchbannerdiv["style"])
                if m:
                    patchbanner = URL(m.group(1))
                else:
                    patchbanner = None
            else:
                patchbanner = None

            patchobjs.append(
                OWPatch(
                    patchref,
                    ver,
                    verpatch,
                    patchdate,
                    OWPatch.getblizztrack(patchref_num),
                    patchbanner,
                )
            )

        return patchobjs

    @staticmethod
    def getblizztrack(patchref: str = None) -> URL:
        """
        Return BlizzTrack URL to patch notes, built using Blizzard's patchref
        
        e.g. https://blizztrack.com/patch_notes/overwatch/50148
        """
        if not patchref:
            raise ValueError("No patch reference provided")

        baseURL = URL("https://blizztrack.com/patch_notes/overwatch/")
        return baseURL / patchref
