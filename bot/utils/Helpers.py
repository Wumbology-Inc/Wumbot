import discord


def isOwner(user: discord.User) -> bool:
    """
    Check to see if the input User's ID matches the Owner ID
    """
    ownerID = 129606635545952258
    return user.id == ownerID


def isDM(channel: discord.TextChannel) -> bool:
    """
    Check to see if a channel is a DM

    A DM is either an instance of DMChannel or GroupChannel
    """
    return isinstance(channel, (discord.DMChannel, discord.GroupChannel))


def isWumbologist(member: discord.Member) -> bool:
    """
    Check to see if a discord.Member has the 'Wumbologists' role
    """
    return "Wumbologists" in [str(role) for role in member.roles]
