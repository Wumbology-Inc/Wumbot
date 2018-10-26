Overwatch Abstract Models
==================================

Class Reference
---------------
.. class:: Overwatch.OWPatch(**kwargs)

    Helper class to generate an object from Blizzard's Patch Notes

    .. attribute:: patchref(str)

        Patch reference ID

        e.g. ``'patch-50148'``

    .. attribute:: ver(str)

        Patch version number

        e.g. ``'1.28.0.1'``

    .. attribute:: verpatch(str)

        Combined version & patch number

        e.g. ``'1.28.0.1.50148'``

    .. attribute:: patchdate(datetime)

        Patch date (UTC)

        e.g. ``dt.strptime('09/11/2018', '%m/%d/%Y')``

    .. attribute:: patchURL(yarl.URL)

        Patch notes permalink

        Patch note permalink is provided by `BlizzTrack <https://blizztrack.com/patch_notes/overwatch/latest>`_

    .. attribute:: bannerURL(yarl.URL)

        Blizzard patch banner URL permalink

    .. comethod:: asyncfromURL(inURL: typing.Union[str, URL]) -> typing.List
        :staticmethod:

        Return a list of Overwatch.OWPatch objects parsed from inURL.

        Default URL is Blizzard's Overwatch PC patch notes. Other URLs are not explicitly supported

    .. staticmethod:: fromURL(inURL: typing.Union[str, URL]) -> typing.List

        *This function is blocking*

        Return a list of Overwatch.OWPatch objects parsed from inURL.

        Default URL is Blizzard's Overwatch PC patch notes. Other URLs are not explicitly supported

    .. staticmethod:: getblizztrack(patchref:str) -> yarl.URL

        Build a ``yarl.URL`` object from a patch reference ID

        .. code-block:: python3

            >>> from cogs import overwatch
            >>> patchURL = overwatch.PatchNotesParser.getblizztrack('50148')
            >>> print(patchURL)
            https://blizztrack.com/patch_notes/overwatch/50148
