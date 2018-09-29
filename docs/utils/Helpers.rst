Wumbot Helper Utilities
==================================

Function reference
-----------------

.. function:: isOwner(user: discord.User) -> bool

    Return ``True`` if the input ``discord.User``'s ID matches the bot owner's ID, otherwise return ``False``

    Owner ID is hardcoded

.. function:: isDM(channel: discord.TextChannel) -> bool

    Return ``True`` if the input ``discord.TextChannel`` is a DM, otherwise return ``False``

    .. note::
        A DM is an instance of either ``discord.DMChannel`` or ``discord.GroupChannel``

.. function:: isWumbologist(member: discord.Member) -> bool

    Return ``True`` if the input ``discord.Member`` has the 'Wumbologists' role, otherwise return ``False``