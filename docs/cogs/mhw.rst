Monster Hunter World
==================================

Parser Reference
----------------

.. class:: mhw.MHWNewsParser

    Official Capcom Monster Hunter World announcements monitor

    .. note::
        Posts with "Status Update" in the title are excluded

    .. attribute:: bot(WumbotClient)

        Discord bot instance

    .. attribute:: postchannelID(int)

        Discord channel ID for patch notes embed

    .. attribute:: logJSONpath(pathlib.Path)

        Path to JSON storage file

    .. attribute:: postedMHWnews(List[str])

        ``List`` containing posted news posts

        Patches are stored as Steam news permalinks, as ``str`` (e.g. ``'https://steamcommunity.com/games/582010/announcements/detail/1689302358462352379'``)

    .. attribute:: appID(int)

        Steam app ID

    .. attribute:: officialaccount(str)

        Official account name

    .. classmethod:: patchcheck

        *This function is a coroutine*

        Executes the patch check operations:

        #. Parse Steam News posts for posts made by the account specified by ``MHWNewsParser.officialaccount``
        #. Build ``mhw.SteamNewsPost`` objects
        #. Check news URLs against those previously posted
        #. If new news post(s): Build embed, post to channel, and save the Steam news permalink to the local JSON log

.. function:: patchchecktimer(client: WumbotClient, sleepseconds: int=3600)

    This function is a *coroutine*

    Asynchronous patch checking loop for use with Discord.py's event loop

    ``mhw.MHWNewsParser`` is called every ``sleepseconds``

Command Reference
-----------------
Commands are prefixed with ``~``

.. function:: ~checkMHWpatch

    Manually invoke the ``mhw.MHWNewsParser.patchcheck()`` coroutine

    .. note::
        This command is only enabled for the server owner via DM.

Class Reference
---------------

.. class:: mhw.SteamNewsPost(**kwargs)

    Helper class for Steam News Posts

    .. attribute:: gid(str)

        Global post ID

    .. attribute:: title(str)

        News post title

    .. attribute:: url(yarl.URL)

        News post permalink

    .. attribute:: is_external_url(bool)

        External URL flag

    .. attribute:: author(str)

        News post author

    .. attribute:: contents(str)

        News post contents

        .. note::
            Contents are truncated by the API call based on the ``maxlength`` parameter

    .. attribute:: feedlabel(str)

        News feed label

    .. attribute::  date(datetime)

        Post date (UTC)

    .. attribute:: feedname(str)

        News feed name

    .. attribute:: feed_type(int)

        News feed type [#apilink]_

    .. attribute:: appid(int)

        App ID [#apilink]_

    .. [#apilink] See `Steam's API Documentation <https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0002.29>`_ for additional details

    .. staticmethod:: getnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, format: str='json', **kwargs) -> typing.List

        Return a list of ``mhw.SteamNewsPost`` objects for the specified ``appID``

        ``count`` specifies the number of posts to Return

        ``maxlength`` specifies the maximum length of the returned contents string

        .. note::
            Additional ``**kwargs`` are discarded


    .. staticmethod:: asyncgetnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, format: str='json', **kwargs) -> typing.List

        This function is a *coroutine*

        Return a list of ``mhw.SteamNewsPost`` objects for the specified ``appID``

        ``count`` specifies the number of posts to Return

        ``maxlength`` specifies the maximum length of the returned contents string

        .. note::
            Additional ``**kwargs`` are discarded
