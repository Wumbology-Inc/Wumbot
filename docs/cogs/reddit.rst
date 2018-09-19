Reddit Extension
==================================

Event Reference
---------------

``on_message`` Events
^^^^^^^^^^^^^^^^^^^^^

.. note::
    Messages starting with the command prefix (``~``) short circuit to the command handler and are not parsed

Subreddit Detection & Embed
"""""""""""""""""""""""""""
When a message is sent containing one or more subreddits (e.g. "``/r/Python`` is the best subreddit!"), Wumbot will generate and respond with a ``discord.Embed`` object that links to the subreddit(s).


v.Reddit ``DashPlaylist.mpd`` Detection
"""""""""""""""""""""""""""""""""""""""
Detect if Reddit's image/video hosting has added ``DashPlaylist.mpd`` to the end of the URL, which links to a direct download (of nothing) rather than the web content. 

Wumbot will strip ``DashPlaylist.mpd`` and respond with the corrected link:

.. code-block:: none

    [13:37] ELA: https://v.redd.it/k32sq2cwmdi01/DASHPlaylist.mpd
    [13:37] Wumbot: Here ELA, let me fix that v.redd.it link for you: https://v.redd.it/k32sq2cwmdi01/

Class Reference
---------------

.. class:: reddit.RedditPost(**kwargs)

    Helper class to generate an object from Reddit JSON

    .. attribute:: kind(str)

        Submission kind

        Defined per `Reddit's API documentation <https://www.reddit.com/dev/api/>`_

    .. attribute:: id(str)

        Unique submission ID

        `Base36 <https://en.wikipedia.org/wiki/Base36>`_ encoded

    .. attribute:: subreddit(str)

        Submission subreddit

    .. attribute:: title(str)

        Submission title

    .. attribute:: createdUTC(datetime)

        Post creation date (UTC)

    .. attribute:: contentURL(str)

        Submission permalink

    .. staticmethod:: fromJSON(jsonURL: str=None) -> typing.List

        Return a list of ``reddit.RedditPost`` objects from an input Reddit JSON URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported

    .. staticmethod:: fromURL(inURL: str=None) -> typing.List:

        Return a list of ``reddit.RedditPost`` objects from an input Reddit URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported

    .. comethod:: asyncfromURL(inURL: str=None) -> typing.List:
        :staticmethod:

        Return a list of ``reddit.RedditPost`` objects from an input Reddit URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported
