Reddit
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
