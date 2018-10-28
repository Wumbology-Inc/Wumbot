import logging
import typing

from bot.utils.SpaceX import SpaceXAPI


class _SpaceXBase:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    async def async_from_API(
        cls: typing.Type, method: str = "", query: typing.Dict = {}
    ) -> typing.List:
        r_json = await SpaceXAPI.async_get(cls.API_endpoint, method, query)[0]

        return _SpaceXBase._gen_obj_list(r_json)

    @classmethod
    def from_API(
        cls: typing.Type, method: str = "", query: typing.Dict = {}
    ) -> typing.List:
        r_json = SpaceXAPI.get(cls.API_endpoint, method, query)[0]

        return _SpaceXBase._gen_obj_list(r_json)

    @classmethod
    def _gen_obj_list(cls, in_json) -> typing.List:
        objlist = []
        if isinstance(in_json, list):
            logging.info(f"{len(in_json)} objects retured by API")
            for entry in in_json:
                objlist.append(cls(**entry))
        elif isinstance(in_json, dict):
            logging.info("Single object returned by API")
            objlist.append(cls(**in_json))
        else:
            raise TypeError(f"Unsupported response type: '{type(in_json)}'")

        return objlist


class Capsule(_SpaceXBase):
    API_endpoint = "capsules"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Core(_SpaceXBase):
    API_endpoint = "cores"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Dragon(_SpaceXBase):
    API_endpoint = "dragons"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class History(_SpaceXBase):
    API_endpoint = "history"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Info(_SpaceXBase):
    API_endpoint = "info"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Launch(_SpaceXBase):
    API_endpoint = "launches"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Launchpad(_SpaceXBase):
    API_endpoint = "launchpads"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Mission(_SpaceXBase):
    API_endpoint = "missions"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Payload(_SpaceXBase):
    API_endpoint = "payloads"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Rocket(_SpaceXBase):
    API_endpoint = "rockets"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Roadster(_SpaceXBase):
    API_endpoint = "roadster"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Ship(_SpaceXBase):
    API_endpoint = "ships"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
