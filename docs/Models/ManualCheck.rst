Manual Patch Check Abstract Helper
======================================

Class Reference
---------------
.. class:: ManualCheck

    .. comethod:: check(ctx: commands.Context, toinvoke: typing.Callable, commandstr: str)
        :staticmethod:

        Helper method for manual patch check invocation commands

        ``toinvoke`` is the parser-specific patch check function to invoke

        ``commandstr`` is a descriptive string to use for logging & bot feedback messages

        .. note::
            ``bot.Helpers.isDM`` and ``bot.Helpers.isOwner`` checks are run prior to invoking the patch check function