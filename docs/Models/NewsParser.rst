Abstract News Parser
========================

Class Reference
---------------


Function Reference
------------------

.. class:: NewsParser

    Abstract news parser base class

    .. note::
        All attributes are defined at the child parser level

    .. attribute:: bot

        ``discord.commands.Bot`` instance

    .. attribute:: postednews

        List containing posted information.

        Format of list entries is defined at the child parser level

    .. attribute:: _parsername

        Descriptive parser shortname

    .. attribute:: _loadconverter

        Function that accepts externally saved posts and formats them for ``postednews``

    .. attribute:: _saveconverter

        Function that accepts entries from ``postednews`` and formats them for external saving

    .. attribute:: _comparator

        Model attribute (as ``str``) used to compare posts to the list of posted news as a new post check

    .. method:: loadposted

        Load saved information from the child class-specified JSON file into ``self.loadposted``

        JSON data is assumed to be stored as a list. ``self._loadconverter`` is run for each JSON list entry

    .. method:: saveposted

        Dump information from ``self.postednews`` into a child class-specified JSON file

        ``self.postednews`` is assumed to be a list. ``self._saveconverter`` is run for each list entry prior to the JSON dump

    .. comethod:: patchcheck(posts: typing.List)

        Abstract patch checking method.

        On invocation:
            #. Load saved posts using ``NewsParser.loadposted``
            #. Check ``posts`` against loaded posts using ``self._comparator`` to get the appropriate comparison attribute
            #. If new posts are present, call the child class' ``postembed`` method to generate & send Discord embed
            #. Save posted news using ``NewsParser.saveposted``

Function Reference
------------------

.. cofunction:: patchchecktimer(client, parsers: typing.Tuple = (), sleepseconds: int = 3600)

    Abstract patch checking event loadposted

    Invoke the input ``parsers`` every ``sleepseconds``