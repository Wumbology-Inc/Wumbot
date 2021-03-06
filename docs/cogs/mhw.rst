Monster Hunter World
==================================

Parser Reference
----------------

.. class:: mhw.MHWNewsParser

    Official Capcom Monster Hunter World announcements monitor

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedMHWnews(List[yarl.URL])

        ``List`` containing posted news posts

        Patches are stored as Steam news permalinks, as ``yarl.URL`` (e.g. ``[URL('https://steamcommunity.com/games/582010/announcements/detail/1689302358462352379')]``)

    .. attribute:: appID(int)

        Steam app ID

    .. attribute:: officialaccount(str)

        Official account name

    .. comethod:: patchcheck
        :classmethod:

        Executes the patch check operations:

        #. Parse Steam News posts for posts made by the account specified by ``MHWNewsParser.officialaccount``
        #. Build ``Models.Steam.SteamNewsPost`` objects
        #. Check news URLs against those previously posted
        #. If new news post(s): Build embed, post to channel, and save the Steam news permalink to the local JSON log

.. cofunction:: patchchecktimer(client: WumbotClient, sleepseconds: int=3600)

    Asynchronous patch checking loop for use with Discord.py's event loop

    ``mhw.MHWNewsParser`` is called every ``sleepseconds``

Command Reference
-----------------
Commands are prefixed with ``~``

.. function:: ~checkMHWpatch

    Manually invoke the ``mhw.MHWNewsParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.
