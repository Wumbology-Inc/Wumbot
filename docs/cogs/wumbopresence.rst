Wumbo Presence
==================================

Function Reference
------------------

.. function:: randWumbo(wumboJSON=None) -> str

    Load a list of Wumboisms from input ``wumboJSON`` file & return a random string from the list

    If no JSON is input, return defaults to ``'The Game of Wumbo'``

.. cofunction:: randWumboTimer(client, sleepseconds=3600, wumboJSON=None)

    Async sleep timer to automatically update the bot's Now Playing status