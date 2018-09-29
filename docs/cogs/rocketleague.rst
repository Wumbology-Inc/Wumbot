Rocket League
==================================

Parser Reference
----------------

.. class:: rocketleague.RLNewsParser

    Official Psyonix Rocket League announcements monitor

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedRLnews(List[yarl.URL])

        ``List`` containing posted news posts

        Patches are stored as Steam news permalinks, as ``yarl.URL`` (e.g. ``[URL('https://steamcommunity.com/games/252950/announcements/detail/1708444560032073223')]``)

    .. attribute:: appID(int)

        Steam app ID

    .. attribute:: psyonixstaff(Tuple)

        Tuple containing account names of Psyonix employees, as ``str``

    .. comethod:: patchcheck
        :classmethod:

        Executes the patch check operations:

        #. Parse Steam News posts for posts made by an account specified by ``RLNewsParser.psyonixstaff``
        #. Build ``Models.Steam.SteamNewsPost`` objects
        #. Check news URLs against those previously posted
        #. If new news post(s): Build embed, post to channel, and save the Steam news permalink to the local JSON log

.. cofunction:: patchchecktimer(client: WumbotClient, sleepseconds: int=3600)

    Asynchronous patch checking loop for use with Discord.py's event loop

    ``rocketleague.RLNewsParser`` is called every ``sleepseconds``

Command Reference
-----------------
Commands are prefixed with ``~``

.. function:: ~checkRLpatch

    Manually invoke the ``rocketleague.RLNewsParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.
