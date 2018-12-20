import logging
import typing

from bot.utils.SpaceX import SpaceXAPI


class _SpaceXBase:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    async def _async_from_API(
        endpoint: str = "", method: str = "", query: typing.Dict = {}
    ) -> typing.List:
        r_json = await SpaceXAPI.async_get(endpoint, method, query)[0]

        return _SpaceXBase._gen_obj_list(r_json)

    @staticmethod
    def _from_API(
        endpoint: str = "", method: str = "", query: typing.Dict = {}
    ) -> typing.List:
        r_json = SpaceXAPI.get(endpoint, method, query)[0]

        return _SpaceXBase._gen_obj_list(r_json)

    @classmethod
    def _gen_obj_list(cls: typing.Type, in_json: typing.Dict) -> typing.List:
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
    """A class that represents a SpaceX Capsule

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    =========================  ==============   ==========================================
    Attribute                  Type             Description
    =========================  ==============   ==========================================
    ``capsule_serial``         ``str``          Capsule serial number
    ``capsule_id``             ``str``          Capsule ID
    ``status``                 ``str``          Capsule status
    ``original_launch``        ``str``          Original launch datetime, UTC, ISO 8601
    ``original_launch_unix``   ``int``          Original launch datetime, Unix epoch
    ``missions``               ``list[dict]``   List of missions the capsule has flown on
    ``landings``               ``int``          Landings
    ``type``                   ``str``          Capsule type
    ``details``                ``str``          Capsule details
    ``reuse_count``            ``int``          Capsule reuses
    =========================  ===============  ==========================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#d65a7f85-e0c7-41ce-b41d-9ad20a238d90

    """

    API_endpoint = "capsules"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, capsule_serial: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(
            endpoint=API_endpoint, method=capsule_serial, query=query
        )

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(
        cls: typing.Type, capsule_serial: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=capsule_serial, query=query)


class Core(_SpaceXBase):
    """A class that represents a SpaceX Core

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    =======================  ===============   ==========================================
    Attribute                Type              Description
    =======================  ===============   ==========================================
    ``core_serial``          ``str``           Core serial number
    ``block``                ``int``           Core block
    ``status``               ``str``           Core status
    ``original_launch``      ``str``           Original launch datetime, UTC, ISO 8601
    ``original_launch_unix   ``int``           Original launch datetime, Unix epoch
    ``missions``             ``list[dict]``    List of missions the capsule has flown on
    ``reuse_count``          ``int`            Core reuses
    ``rtls_attempts``        ``int`            RTLS landing attempts
    ``rtls_landings``        ``int`            Successful RTLS landings
    ``asds_attempts``        ``int`            ASDS landing attempts
    ``asds_landings``        ``int`            Successful ASDS landings
    ``water_landing``        ``bool``          Water landing
    ``details``              ``str``           Core details
    =======================  ===============   ==========================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#1a1acb6e-0f15-437b-ae16-dcabf24dec9f

    """

    API_endpoint = "cores"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, core_serial: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(
            endpoint=API_endpoint, method=core_serial, query=query
        )

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(
        cls: typing.Type, core_serial: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=core_serial, query=query)


class Dragon(_SpaceXBase):
    """A class that represents a SpaceX Dragon spacecraft

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ========================  ==============  ============================
    Attribute                 Type            Description
    ========================  ==============  ============================
    ``id``                   ``str``          Dragon ID
    ``name``                 ``str``          Dragon name
    ``type``                 ``str``          Dragon type
    ``active``               ``bool``         Dragon status
    ``crew_capacity``        ``int``          Dragon crew capacity
    ``sidewall_angle_deg``   ``int``          Sidewall angle, degree
    ``orbit_duration_yr"``   ``int``          Orbit duration, year
    ``dry_mass_kg``          ``int``          Dragon dry mass, kilogram
    ``dry_mass_lb``          ``int``          Dragon dry mass, pound
    ``first_flight``         ``str``          Date of first flight
    ``heat_shield``          ``dict``         Heat shield details
    ``thrusters``            ``list[dict]``   Thruster details
    ``launch_payload_mass``  ``dict``         Launch payload mass
    ``launch_payload_vol``   ``dict``         Launch payload volume
    ``return_payload_mass``  ``dict``         Return payload mass
    ``return_payload_vol``   ``dict``         Return payload volume
    ``pressurized_capsule``  ``dict[dict]``   Pressurized capsule details
    ``trunk``                ``dict[dict]``   Trunk details
    ``cargo``                ``dict[dict]``   Cargo details
    ``height_w_trunk``       ``dict``         Dragon height with trunk
    ``diameter``             ``dict``         Dragon diameter
    ``wikipedia``            ``str``          Wikipedia permalink
    ``description``          ``str``          Dragon description
    ========================  ==============  ============================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#3d6e6f8a-a459-4265-84b1-e2b288a58537

    """

    API_endpoint = "dragons"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method=id, query=query)

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(cls: typing.Type, id: str, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=id, query=query)


class History(_SpaceXBase):
    """A class that represents a SpaceX news event

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ====================  =========  ====================================
    Attribute             Type       Description
    ====================  =========  ====================================
    ``id``                ``int``    News ID
    ``title``             ``str``    News title
    ``event_date_utc``    ``str``    News posted datetime, UTC, ISO 8601
    ``event_date_unix``   ``int``    News posted datetime, Unix epoch
    ``flight_number``     ``int``    SpaceX flight number
    ``details``           ``str``    Event details
    ``links``             ``dict``   News permalink(s)
    ====================  =========  ====================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#ead57e9b-70db-432d-9923-4bf4b881cfd0

    """

    API_endpoint = "history"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, id: int, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method=id, query=query)

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(cls: typing.Type, id: int, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=id, query=query)


class CompanyInfo(_SpaceXBase):
    """A class that represents SpaceX company info

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ===================  =========  ==========================
    Attribute            Type       Description
    ===================  =========  ==========================
    ``name``             ``str``    Company name
    ``founder``          ``str``    Company founder
    ``founded``          ``int``    Year company was founded
    ``employees``        ``int``    Number of employees
    ``vehicles``         ``int``    Number of launch vehicles
    ``launch_sites``     ``int``    Number of launch sites
    ``test_sites``       ``int``    Number of test sites
    ``ceo``              ``str``    CEO
    ``cto``              ``str``    CTO
    ``coo``              ``str``    COO
    ``cto_propulsion``   ``str``    CTO of Propulsion
    ``valuation``        ``int``    Valuation, USD
    ``headquarters``     ``dict``   Headquarters location
    ``summary``          ``str``    Company summary
    ===================  =========  ==========================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#9b8b053e-cb75-400c-9635-5fe1c771d8a3

    """

    API_endpoint = "info"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_info(cls: typing.Type) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint)

    @classmethod
    def get_info(cls: typing.Type) -> typing.List:
        return cls._from_API(endpoint=API_endpoint)


class APIInfo(_SpaceXBase):
    """A class that represents the /r/SpaceX API info

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ======================  ========  =======================================
    Attribute               Type      Description
    ======================  ========  =======================================
    ``project_name``        ``str``   API project name
    ``version``             ``str``   API version number
    ``project_link``        ``str``   API source permalink
    ``organization``        ``str``   API development organization
    ``organization_link``   ``str``   API development organization permalink
    ``description``         ``str``   API permalink
    ======================  ========  =======================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#30c2d33b-4943-43ae-a98a-5ede3ece6388

    """

    API_endpoint = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_info(cls: typing.Type) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint)

    @classmethod
    def get_info(cls: typing.Type) -> typing.List:
        return cls._from_API(endpoint=API_endpoint)


class Launch(_SpaceXBase):
    """A class that represents a SpaceX launch

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ==========================  =========  ====================================
    Attribute                   Type       Description
    ==========================  =========  ====================================
    ``flight_number``           ``int``    Flight number
    ``mission_name``            ``str``    Mission name
    ``mission_id``              ``list``   Mission ID
    ``launch_year``             ``str``    Mission launch year
    ``launch_date_unix``        ``int``    Launch datetime, Unix epoch
    ``launch_date_utc``         ``str``    Launch datetime, UTC, ISO 8601
    ``launch_date_local``       ``str``    Launch datetime, local, ISO 8601
    ``is_tentative"``           ``bool``   Is the launch tentatitve?
    ``tentative_max_precision   ``str``    Precision of launch date
    ``rocket``                  ``dict``   Rocket information
    ``ships``                   ``list``   Ship(s) being launched
    ``telemetry``               ``dict``   Telemetry permalink(s)
    ``launch_site``             ``dict``   Launch site information
    ``launch_success``          ``bool``   Launch success status
    ``links``                   ``dict``   Launch permalink(s)
    ``details``                 ``str``    Launch details
    ``upcoming``                ``bool``   Upcoming launch?
    ``static_fire_date_utc``    ``str``    Static fire datetime, UTC, ISO 8601
    ``static_fire_date_unix``   ``int``    Static fire datetime, Unix epoch
    ==========================  =========  ====================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#bc65ba60-decf-4289-bb04-4ca9df01b9c1

    """

    API_endpoint = "launches"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, flight_number: int, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(
            endpoint=API_endpoint, method=flight_number, query=query
        )

    @classmethod
    async def async_get_past(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method="past", query=query)

    @classmethod
    async def async_get_upcoming(
        cls: typing.Type, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(
            endpoint=API_endpoint, method="upcoming", query=query
        )

    @classmethod
    async def async_get_latest(
        cls: typing.Type, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method="latest")

    @classmethod
    async def async_get_next(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method="next")

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(
        cls: typing.Type, flight_number: int, query: typing.Dict = {}
    ) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=flight_number, query=query)

    @classmethod
    async def get_past(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method="past", query=query)

    @classmethod
    async def get_upcoming(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method="upcoming", query=query)

    @classmethod
    async def get_latest(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method="latest")

    @classmethod
    async def get_next(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method="next")


class Launchpad(_SpaceXBase):
    """A class that represents a SpaceX launchpad

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ======================  =========  ===================
    Attribute               Type       Description
    ======================  =========  ===================
    ``id``                  ``int``    Launchpad ID
    ``status``              ``str``    Launchpad status
    ``location``            ``dict``   Launchpad location
    ``vehicles_launched``   ``list``   Vehicles launched
    ``details``             ``str``    Launchpad details
    ``site_id``             ``str``    Launchsite ID
    ``site_name_long``      ``str``    Launchsite name
    ======================  =========  ===================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#e232e64a-58a2-4bc0-af42-eb20499425cc

    """

    API_endpoint = "launchpads"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, site_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method=site_id, query=query)

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(cls: typing.Type, site_id: str, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=site_id, query=query)


class Mission(_SpaceXBase):
    """A class that represents a SpaceX mission

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    ==================  ==============   ============================
    Attribute           Type             Description
    ==================  ==============   ============================
    ``mission_name``    ``str``          Mission name
    ``mission_id``      ``str``          Mission ID
    ``manufacturers``   ``list[str]``    Manufacturer(s)
    ``payload_ids``     ``list[str]``    Payload ID(s)
    ``wikipedia``       ``str``          Mission Wikipedia permalink
    ``website``         ``str``          Mission permalink
    ``twitter``         ``str``          Mission Twitter permalink
    ``description``     ``str``          Mission description
    ==================  ==============   ============================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#9211ff07-9f81-41ac-9568-3018dd043e2a

    """

    API_endpoint = "missions"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, mission_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(
            endpoint=API_endpoint, method=mission_id, query=query
        )

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(
        cls: typing.Type, mission_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=mission_id, query=query)


class Payload(_SpaceXBase):
    """A class that represents a SpaceX payload

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    =====================  ==============   =====================
    Attribute              Type             Description
    =====================  ==============   =====================
    ``payload_id``         ``str``          Payload ID
    ``norad_id``           ``list[int]``    NORAD ID
    ``reused``             ``bool``         Payload reused?
    ``customers``          ``list[str]``    Customer(s)
    ``nationality``        ``str``          Payload nationality
    ``manufacturer``       ``str``          Payload manufacturer
    ``payload_type``       ``str``          Payload type
    ``payload_mass_kg``    ``int``          Payload mass, kg
    ``payload_mass_lbs``   ``float``        Payload mass, lb
    ``orbit``              ``str``          Payload orbit
    ``orbit_params``       ``dict``         Orbital parameters
    =====================  ==============   =====================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#2936485d-1d09-464c-a909-1c2041d67c75

    """

    API_endpoint = "payloads"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, payload_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(
            endpoint=API_endpoint, method=payload_id, query=query
        )

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(
        cls: typing.Type, payload_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=payload_id, query=query)


class Rocket(_SpaceXBase):
    """A class that represents a SpaceX rocket

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    =====================  ===============  =========================================
    Attribute              Type             Description
    =====================  ===============  =========================================
    ``id``                 ``int``          Rocket ID, int
    ``active``             ``bool``         Rocket active?
    ``stages``             ``int``          Number of stages
    ``boosters``           ``int``          Number of boosters 0,
    ``cost_per_launch``    ``int``          Cost per launch, USD
    ``success_rate_pct``   ``int``          Success rate, percent
    ``first_flight``       ``str``          Date of first flight
    ``country``            ``str``          Country of origin
    ``company``            ``str``          Company
    ``height``             ``dict``         Rocket height
    ``diameter``           ``dict``         Rocket diameter
    ``mass``               ``dict``         Rocket mass
    ``payload_weights``    ``list[dict]``   Payload weight capability
    ``first_stage``        ``dict``         First stage description
    ``second_stage``       ``dict``         Second stage description
    ``engines``            ``dict``         Engine description
    ``landing_legs``       ``dict``         Landing legs description
    ``wikipedia``          ``str``          Wikipedia permalink
    ``description``        ``str``          Rocket description
    ``rocket_id``          ``str``          Rocket ID, str
    ``rocket_name``        ``str``          Rocket name
    ``rocket_type``        ``str``          Rocket type
    =====================  ===============  =========================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#5fcdb875-914f-4aef-a932-254397cf147a

    """

    API_endpoint = "rockets"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, rocket_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method=rocket_id, query=query)

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(
        cls: typing.Type, rocket_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=rocket_id, query=query)


class Roadster(_SpaceXBase):
    """A class that represents the SpaceX Mars Roadster

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    =======================  ==========  ===============================
    Attribute                Type        Description
    =======================  ==========  ===============================
    ``name``                 ``str``     Mars Roadster name
    ``launch_date_utc``      ``str``     Launch datetime, UTC, ISO 8601
    ``launch_date_unix``     ``int``     Launch datetime, Unix epoch
    ``launch_mass_kg``       ``int``     Launch mass, kg
    ``launch_mass_lbs``      ``int``     Launch mass, lb
    ``norad_id``             ``int``     NORAD ID
    ``epoch_jd``             ``float``   Julian epoch
    ``orbit_type``           ``str``     Orbit type
    ``apoapsis_au``          ``float``   Orbit apoapsis, AU
    ``periapsis_au``         ``float``   Orbit periapsis, AU
    ``semi_major_axis_au``   ``float``   Orbit semimajor axis, AU
    ``eccentricity``         ``float``   Orbit eccentricity
    ``inclination``          ``float``   Orbit inclination, degree
    ``longitude``            ``float``   Ecliptic longitude
    ``periapsis_arg``        ``float``   Argument of periapsis, degree
    ``period_days``          ``float``   Orbital period, day
    ``speed_kph``            ``float``   Orbital speed, kph
    ``speed_mph``            ``float``   Orbital speed, mph
    ``earth_distance_km``    ``float``   Distance from Earth, km
    ``earth_distance_mi``    ``float``   Distance from Earth, mi
    ``mars_distance_km``     ``float``   Distance from Mars, km
    ``mars_distance_mi``     ``float``   Distance from Mars, mi
    ``wikipedia``            ``str``     Wikipedia permalink
    ``details``              ``str``     Mission details
    =======================  ==========  ===============================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#46951cda-bdf2-481b-9697-118b1cbccaba

    """

    API_endpoint = "roadster"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_info(cls: typing.Type) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint)

    @classmethod
    def get_info(cls: typing.Type) -> typing.List:
        return cls._from_API(endpoint=API_endpoint)


class Ship(_SpaceXBase):
    """A class that represents a SpaceX ship

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this
    class. Attributes are dynamically provided, so there is no guarantee that 
    all attributes will be present.

    See the `r/SpaceX-API v3 Docs`_ for a comprehensive list of attributes
    =======================  ===============  =========================================
    Attribute                Type             Description
    =======================  ===============  =========================================
    "ship_id``               ``str``          Ship ID
    "ship_name``             ``str``          Ship name
    "ship_model``            ``str``          Ship model
    "ship_type``             ``str``          Ship type
    "roles``                 ``list[str]``    Ship role(s)
    "active``                ``bool``         Is active?
    "imo``                   ``int``          IMO ID
    "mmsi``                  ``int``          MMSI ID
    "abs``                   ``int``          ABS ID
    "class``                 ``int``          Ship class
    "weight_lbs``            ``int``          Ship weight, lb
    "weight_kg``             ``int``          Ship weight, kg
    "year_built``            ``int``          Year built
    "home_port``             ``str``          Home port
    "status``                ``str``          Ship status
    "speed_kn``              ``int``          Current speed
    "course_deg``            ``int``          Current course
    "position``              ``dict``         Current position
    "successful_landings``   ``int``          Successful landings
    "attempted_landings``    ``int``          Attempted landings
    "missions``              ``list[dict]``   Missions supported
    "url``                   ``str``          Ship tracking permalink
    "image``                 ``str``          Ship image permalink
    =======================  ===============  =========================================


    .. _r/SpaceX-API v3 Docs: https://documenter.getpostman.com/view/2025350/RWaEzAiG#c7162816-0560-48ea-84ba-ed8ca4240647

    """

    API_endpoint = "ships"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    async def async_get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, query=query)

    @classmethod
    async def async_get_one(
        cls: typing.Type, ship_id: str, query: typing.Dict = {}
    ) -> typing.List:
        return cls._async_from_API(endpoint=API_endpoint, method=ship_id, query=query)

    @classmethod
    def get_all(cls: typing.Type, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, query=query)

    @classmethod
    def get_one(cls: typing.Type, ship_id: str, query: typing.Dict = {}) -> typing.List:
        return cls._from_API(endpoint=API_endpoint, method=ship_id, query=query)
