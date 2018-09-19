Overwatch Extension
==================================

Parser Reference
----------------

.. class:: overwatch.PatchNotesParser

    Blizzard's `Overwatch Patch Notes <https://playoverwatch.com/en-us/news/patch-notes/pc>`_ Monitor

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: patchesURL(yar.URL)

        Blizzard Patch Notes URL

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedpatches(List[str])

        ``List`` containing posted patch notes

        Patches are stored as patch reference IDs, as ``str`` (e.g. ``'50148'``)

    .. classmethod:: patchcheck

        *This function is a coroutine*

        Executes the patch check operations:

        #. Scrape Blizzard's Patch Notes
        #. Build ``overwatch.OWPost`` objects from scraped patch notes
        #. Check patch references against those previously posted
        #. If new patch(es): Build embed, post to channel, and save the patch reference(s) to the local JSON log

    .. staticmethod:: getblizztrack(patchref:str) -> yarl.URL

        Build a ``yarl.URL`` object from a patch reference ID

        .. code-block:: python3

            >>> from cogs import overwatch
            >>> patchURL = overwatch.PatchNotesParser.getblizztrack('50148')
            >>> print(patchURL)
            https://blizztrack.com/patch_notes/overwatch/50148

.. class:: overwatch.PatchNotesParser

    Reddit user `/u/itsjieyang <https://reddit.com/u/itsjieyang>`_'s Overwatch Patch GIF Monitor

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: postjsonURL(yar.URL)

        Reddit's JSON URL for /u/itsjieyang's submissions

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedGIFs(List[str])

        ``List`` containing posted patch notes

        Patches are stored as Gfycat permalinks, as ``str`` (e.g. ``'https://gfycat.com/MajorDiligentIbizanhound'``)

    .. classmethod:: patchcheck

        *This function is a coroutine*

        Executes the patch check operations:

        #. Parse /u/itsjieyang's submission JSON for Gfycat submissions to /r/overwatch
        #. Build `reddit.RedditPost` objects
        #. Check Gfycat URLs against those previously posted
        #. If new patch GIF(s): Build embed, post to channel, and save the Gfycat permalink to the local JSON log

    .. staticmethod:: gfygif(inURL: str) -> str

        Build a direct GIF link from a Gfycat URL

        .. code-block:: python3

            >>> from cogs import overwatch
            >>> gifURL = overwatch.PatchGifParser.gfygif('https://gfycat.com/MajorDiligentIbizanhound')
            >>> print(gif)
            https://giant.gfycat.com/MajorDiligentIbizanhound.gif

.. function:: patchchecktimer(client: WumbotClient, sleepseconds: int=3600)

    This function is a *coroutine*

    Asynchronous patch checking loop for use with Discord.py's event loop

    ``overwatch.PatchNotesParser`` and ``overwatch.PatchGifParser`` are called every ``sleepseconds``

Command Reference
-----------------
Commands are prefixed with ``~``

.. function:: ~checkOWgif

    Manually invoke the ``overwatch.PatchGifParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.

.. function:: ~checkOWpatch

    Manually invoke the ``overwatch.PatchNotesParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.

Class Reference
---------------
.. class:: overwatch.OWPatch(**kwargs)

    Helper class to generate an object from Blizzard's Patch Notes

    .. attribute:: patchref(str)

        Patch reference ID

        e.g. ``'patch-50148'``

    .. attribute:: ver(str)

        Patch version number

        e.g. ``'1.28.0.1'``

    .. attribute:: patchdate(datetime)

        Patch date (UTC)

        e.g. ``dt.strptime('09/11/2018', '%m/%d/%Y')``

    .. attribute:: patchURL(yarl.URL)

        Patch notes permalink

        Patch note permalink is provided by `BlizzTrack <https://blizztrack.com/patch_notes/overwatch/latest>`_

    .. attribute:: bannerURL(yar.URL)

        Blizzard patch banner URL permalink
