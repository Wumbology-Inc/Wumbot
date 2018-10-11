Steam Abstract Models
==================================

Class Reference
---------------

.. class:: Steam.SteamNewsPost(**kwargs)

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

        .. note::
            URLs are stripped from ``content`` on object instantiation

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

        *This function is blocking*

        Return a list of ``mhw.SteamNewsPost`` objects for the specified ``appID``

        ``count`` specifies the number of posts to Return

        ``maxlength`` specifies the maximum length of the returned contents string

        .. note::
            Additional ``**kwargs`` are discarded


    .. comethod:: asyncgetnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, format: str='json', **kwargs) -> typing.List
        :staticmethod:

        Return a list of ``mhw.SteamNewsPost`` objects for the specified ``appID``

        ``count`` specifies the number of posts to Return

        ``maxlength`` specifies the maximum length of the returned contents string

        .. note::
            Additional ``**kwargs`` are discarded
