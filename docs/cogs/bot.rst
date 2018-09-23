Basic Bot Commands
==================================

Command Reference
-----------------
Commands are prefixed with ``~``

.. function:: ~ver

    Replies with the current version number provided by the most recent tag on the ``master`` branch.

    For example:

    .. code-block:: none

        [13:37] ELA: ~ver
        [13:37] Wumbot: Current Version: v0.7.1

    .. note::
        This command utilizes GitPython's ``git.describe()``, which will throw an exception if there are no tags present. This exception is handled:

        .. code-block:: none

            [13:37] ELA: ~ver
            [13:37] Wumbot: No tags found on current branch

        To fix this error, ensure that the tags are being pulled or fetched on deployment.

.. function:: ~uptime

    Replies with Wumbot's current uptime.

    .. code-block:: none

        [13:37] ELA: ~uptime
        [13:37] Wumbot: Wumbot has been up for: 1d 2h 13m 37s

.. function:: ~kill

    Disconnects Wumbot from the server.

    .. code-block:: none

        [13:37] ELA: ~kill
        [13:37] Wumbot: Shutting down... :wave:

    .. note::
        This command is only enabled for the server owner via DM.

        .. code-block:: none

            [13:37] notELA: ~kill
            [13:37] Wumbot: You are not authorized to perform this operation

.. function:: ~reactmessage messageID message

    Applies a reaction message to a message, as specified by the message's integer ID.

    .. code-block:: none

        [13:37] ELA: ~reactmessage 492366085232787467 Hype

    ``reactionmessage`` is constrained as follows:

    * Command may only be invoked by the 'Wumbologists' role
    * Message must be alphabetic (includes space)
    * Message must not contain repeat characters

    .. note:: 
        If the reaction message is successful, the invoking command is automatically deleted after 10 seconds.

        Any feedback on incorrectly formed input or permission restriction is also automatically deleted after 10 seconds.