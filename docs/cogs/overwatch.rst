Overwatch
==================================

Parser Reference
----------------

.. class:: overwatch.PatchNotesParser

    Blizzard's `Overwatch Patch Notes <https://playoverwatch.com/en-us/news/patch-notes/pc>`_ Monitor

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: patchesURL(yarl.URL)

        Blizzard Patch Notes URL

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedpatches(List[str])

        ``List`` containing posted patch notes

        Patches are stored as patch version & ID, as ``str`` (e.g. ``'1.28.0.1.50148'``)

    .. comethod:: patchcheck
        :classmethod:

        Executes the patch check operations:

        #. Scrape Blizzard's Patch Notes
        #. Build ``Models.Overwatch.OWPost`` objects from scraped patch notes
        #. Check patch references against those previously posted
        #. If new patch(es): Build embed, post to channel, and save the patch reference(s) to the local JSON log

.. class:: overwatch.PatchRundownParser

    Reddit user `/u/itsjieyang <https://reddit.com/u/itsjieyang>`_'s Overwatch patch rundown monitor

    Rundows are currently posted as:
      * Gfycat - Brief summary
      * Youtube Video - Extended rundown
      * Streamable - Brief/extended rundown

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: postjsonURL(yarl.URL)

        Reddit's JSON URL for /u/itsjieyang's submissions

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedrundowns(List[str])

        ``List`` containing posted patch notes

        Patches are stored as permalinks, as ``str`` (e.g. ``'https://gfycat.com/MajorDiligentIbizanhound'``)

    .. comethod:: patchcheck
        :classmethod:

        Executes the patch check operations:

        #. Parse /u/itsjieyang's submissions for submissions to /r/overwatch

        .. note::
            An attempt is made to open an authenticated `PRAW <https://github.com/praw-dev/praw>`_ session to query submissions. If a session cannot be generated, Reddit's JSON is used as a fallback

        #. Build `Models.Reddit.RedditPost` objects
        #. Check Gfycat URLs against those previously posted
        #. If new patch rundown(s): Build embed, post to channel, and save the permalink to the local JSON log

    .. staticmethod:: gfygif(inURL: typing.Union[str, yarl.URL]) -> yarl.URL

        Build a direct GIF link from a Gfycat URL

        .. code-block:: python3

            >>> from cogs import overwatch
            >>> gifURL = overwatch.PatchGifParser.gfygif('https://gfycat.com/MajorDiligentIbizanhound')
            >>> print(gif)
            https://giant.gfycat.com/MajorDiligentIbizanhound.gif

.. cofunction:: patchchecktimer(client: WumbotClient, sleepseconds: int=3600)

    Asynchronous patch checking loop for use with Discord.py's event loop

    ``overwatch.PatchNotesParser`` and ``overwatch.PatchRundownParser`` are called every ``sleepseconds``

Command Reference
-----------------
Commands are prefixed with ``~``

.. function:: ~checkOWrundown

    Manually invoke the ``overwatch.PatchRundownParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.

.. function:: ~checkOWpatch

    Manually invoke the ``overwatch.PatchNotesParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.
