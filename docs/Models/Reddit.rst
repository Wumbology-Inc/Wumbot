Reddit Abstract Models
==================================

Class Reference
---------------

.. class:: Reddit.RedditPost(self, subreddit: str=None, id: str=None, created_utc: float=None, title: str=None, url: str=None, permalink: str=None, author: str=None, **kwargs)

    Helper object to represent a Reddit Submission

    .. note::
        To simplify construction from Reddit's JSON return, additional keyword arguments are accepted but discarded

    .. attribute:: subreddit(str)

        Submission subreddit
    
    .. attribute:: id(str)

        Unique submission ID

        `Base36 <https://en.wikipedia.org/wiki/Base36>`_ encoded

    .. attribute:: created_utc(datetime)

        Post creation date (UTC)

    .. attribute:: title(str)

        Submission title

    .. attribute:: url(yarl.URL)

        Content URL

    .. attribute:: permalink(yarl.URL)

        Submission permalink

    .. attribute:: author(str)

        Submission author

    .. staticmethod:: fromJSON(inJSON: dict) -> RedditPost

        Generate ``Reddit.RedditPost`` from a Reddit submission JSON (as dict)

    .. staticmethod:: fromPRAW(inSub: praw.Submission) -> RedditPost

        Generate ``Reddit.RedditPost`` from a ``praw.Submission`` object


.. class:: RedditPRAW(credentialJSON: Path=Path('./credentials.JSON'))

    Helper class for PRAW instance

    .. note:: 
        On instantiation, an attempt is made to authenticate using the input ``credentialJSON``
        
        ``credentialJSON`` should contain a ``'RedditOAuth'`` key with an ``(ID, secret)`` tuple

        The ``isauthenticated`` attribute can be queried to determine authentication status

    .. method:: getnewusersubmissions(self, username: str, limit: int=25) -> praw.models.ListingGenerator

        Return a ``praw.ListingGenerator`` of ``username``'s newest Reddit submissions

        API call can be limited to a number of submissions, as specified by ``limit``


.. class:: RedditJSON

    Helper class for Reddit JSON methods

    .. comethod:: asyncfromJSON(jsonURL: typing.Union[str, URL]=None, skipvalidation: bool=False) -> typing.List:
        :staticmethod:

        Return a list of ``Reddit.RedditPost`` objects from an input Reddit JSON URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/).json
            https://old.reddit.com/r/subreddit(/).json
            https://old.reddit.com/r/subreddit/comments/*.json

        Other input URL formats are not supported

        The skipvalidation flag allows you to skip the URL validation if it has already been validated

    .. staticmethod:: fromJSON(jsonURL: typing.Union[str, URL]=None, skipvalidation: bool=False) -> typing.List:

        *This function is blocking*

        Return a list of ``Reddit.RedditPost`` objects from an input Reddit JSON URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/).json
            https://old.reddit.com/r/subreddit(/).json
            https://old.reddit.com/r/subreddit/comments/*.json

        Other input URL formats are not supported

        The skipvalidation flag allows you to skip the URL validation if it has already been validated

    .. comethod:: asyncfromURL(inURL: typing.Union[str, yarl.URL]=None) -> typing.List:
        :staticmethod:

        Return a list of ``reddit.RedditPost`` objects from an input Reddit URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported

    .. staticmethod:: fromURL(inURL: typing.Union[str, yarl.URL]=None) -> typing.List:

        *This function is blocking*

        Return a list of ``reddit.RedditPost`` objects from an input Reddit URL

        Supported URL schemas are:

        .. code-block:: none

            https://old.reddit.com/u(ser)/username/submitted(/)
            https://old.reddit.com/r/subreddit(/)
            https://old.reddit.com/r/subreddit/comments/*

        Other input URL formats are not supported
