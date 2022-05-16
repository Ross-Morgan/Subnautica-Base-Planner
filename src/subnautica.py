from collections import Counter
from enum import Enum, auto
from typing import Iterable, TypeVar, Type, Union


class MaterialType(Enum):
    base_piece = auto()
    raw_material = auto()
    constructed_material = auto()


class Material:
    _name = None
    _is_raw = False
    _type = None

    def __init__(self, name: str) -> None:
        self._name = name

    def __hash__(self) -> int:
        return hash(self._name)

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    @property
    @classmethod
    def type(cls) -> MaterialType:
        return cls._type

    @property
    @classmethod
    def is_raw(cls):
        return cls._is_raw


M = TypeVar("M", bound=Material)
KT = TypeVar("KT")
VT = TypeVar("VT")


class RawMaterial(Material):
    _type = MaterialType.raw_material
    _is_raw = True


class ConstMaterial(Material):
    _type = MaterialType.constructed_material


class BuildingPiece(Material):
    _type = MaterialType.base_piece


class PowerPiece(Material):
    _type = MaterialType.base_piece

    def __init__(self, name: str, power: int = 0) -> None:
        self._power = power
        super().__init__(name)

    @property
    def power(self):
        return self._power


class BasePiece(Material):
    _depth = 0.0
    _multiplier = 1.0
    _type = MaterialType.base_piece

    def __init__(self, name: str, si: float = 0):
        self._struct_integrity = si
        super().__init__(name)

    @property
    @classmethod
    def multiplier(cls):
        return cls._multiplier

    @property
    @classmethod
    def depth(cls):
        return cls._depth

    @depth.setter
    @classmethod
    def depth(cls, depth: int):
        cls._depth = depth

        if depth <= 0:
            cls._multiplier = 0.0

        if 0 < depth < 100:
            cls._multiplier = 1.0

        if depth >= 100:
            cls._multiplier = ((depth - 100) / 1000) + 1.0

        cls._multiplier = min(0, cls._multiplier)
        cls._multiplier = max(3.94, cls._multiplier)

    @property
    def structural_integrity(self):
        return self._struct_integrity


class Item:
    """Base Class for Items"""


class Materials(Item):
    # Limestone
    titanium = RawMaterial("titanium")
    copper = RawMaterial("copper")

    # Sandstone
    gold = RawMaterial("gold")
    silver = RawMaterial("silver")
    lead = RawMaterial("lead")

    # Shale
    lithium = RawMaterial("lithium")
    diamond = RawMaterial("diamond")
    uranium = RawMaterial("uranium")

    # Other Minerals
    magnetite = RawMaterial("magnetite")
    ruby = RawMaterial("ruby")
    nickel = RawMaterial("nickel")
    sulphur = RawMaterial("sulphur")
    kyanite = RawMaterial("kyanite")
    quartz = RawMaterial("quartz")
    salt = RawMaterial("salt")
    gel_sack = RawMaterial("gel_sack")
    creepvine_sample = RawMaterial("creepvine_sample")
    creepvine_seed_cluster = RawMaterial("creepvine_seed_cluster")
    table_coral_sample = RawMaterial("table_coral_sample")
    stalker_tooth = RawMaterial("stalker_tooth")
    acid_mushroom = RawMaterial("acid_mushroom")

    # Constructed Materials
    aerogel = ConstMaterial("aerogel")
    fiber_mesh = ConstMaterial("fiber_mesh")
    glass = ConstMaterial("glass")
    enamaled_glass = ConstMaterial("enamaled_glass")
    lubricant = ConstMaterial("lubricant")
    plasteel_ingot = ConstMaterial("plasteel_ingot")
    titanium_ingot = ConstMaterial("titanium_ingot")
    silicone_rubber = ConstMaterial("silicone_rubber")

    # Electronics
    computer_chip = ConstMaterial("computer_chip")
    copper_wire = ConstMaterial("copper_wire")
    wiring_kit = ConstMaterial("wiring_kit")
    advanced_wiring_kit = ConstMaterial("advanced_wiring_kit")
    battery = ConstMaterial("battery")
    power_cell = ConstMaterial("power_cell")


class Buildings(Item):
    # Base Pieces

    foundation = BasePiece("foundation", +2)
    bulkhead = BasePiece("bulkhead", +3)
    i_compartment = BasePiece("i_compartment", -1)
    l_compartment = BasePiece("l_compartment", -1)
    t_compartment = BasePiece("t_compartment", -1)
    x_compartment = BasePiece("x_compartment", -1)
    glass_i_compartment = BasePiece("glass_i_compartment", -2)
    glass_l_compartment = BasePiece("glass_l_compartment", -2)
    vertical_connector = BasePiece("vertical_connector", -0.5)
    multipurpose_room = BasePiece("multipurpose_room", -1.25)
    scanner_room = BasePiece("scanner_room", -1)
    moonpool = BasePiece("moonpool", -5)
    observatory = BasePiece("observatory", -3)
    hatch = BasePiece("hatch", -1)
    window = BasePiece("window", -1)
    reinforcement = BasePiece("reinforcement", +7)

    # Power

    bioreactor = PowerPiece("bioreactor", 500)
    nuclear_reactor = PowerPiece("nuclear_reactor", 2500)
    solar_panel = PowerPiece("solar_panel", 75)
    thermal_plant = PowerPiece("thermal_plant", 250)
    power_transmitter = PowerPiece("power_transmitter", 0)

    # Building Pieces

    class Exterior:
        floodlight = BuildingPiece("floodlight")
        spotlight = BuildingPiece("spotlight")
        exterior_growbed = BuildingPiece("exterior_growbed")
        base_air_pump = BuildingPiece("base_air_pump")

    class Interior:
        class Pieces:
            ladder = BuildingPiece("ladder")
            water_filtration_pump = BuildingPiece("water_filtration_pump")
            vehicle_upgrade_console = BuildingPiece("vehicle_upgrade_console")
            alien_containment = BuildingPiece("alien_containment")

        class Modules:
            fabricator = BuildingPiece("fabricator")
            radio = BuildingPiece("radio")
            med_kit_fabricator = BuildingPiece("med_kit_fabricator")
            wall_locker = BuildingPiece("wall_locker")
            locker = BuildingPiece("locker")
            battery_charger = BuildingPiece("battery_charger")
            power_cell_charger = BuildingPiece("power_cell_charger")
            aquarium = BuildingPiece("aquarium")
            modification_station = BuildingPiece("modification_station")
            plant_pot = BuildingPiece("plant_pot")
            indoor_growbed = BuildingPiece("indoor_growbed")
            plant_shelf = BuildingPiece("plant_shelf")


class Vehicles(Item):
    seamoth = ConstMaterial("seamoth")
    prawn_suit = ConstMaterial("prawn_suit")


class Recipe:
    _mats = Materials

    _craft_dict: dict[Type[M], dict[Type[M], int]] = {
        # Constructed Materials

        Materials.aerogel: {_mats.ruby: 1, _mats.gel_sack: 1},
        Materials.fiber_mesh: {_mats.creepvine_sample: 2},
        Materials.glass: {_mats.quartz: 2},
        Materials.enamaled_glass: {_mats.glass: 1, _mats.stalker_tooth: 1},
        Materials.lubricant: {_mats.creepvine_seed_cluster: 1},
        Materials.plasteel_ingot: {_mats.titanium_ingot: 1, _mats.lithium: 2},
        Materials.titanium_ingot: {_mats.titanium: 10},
        Materials.silicone_rubber: {_mats.creepvine_seed_cluster: 1},

        # Electronics

        Materials.computer_chip: {_mats.table_coral_sample: 2, _mats.gold: 1, _mats.copper_wire: 1},
        Materials.copper_wire: {_mats.copper: 2},
        Materials.wiring_kit: {_mats.silver: 2},
        Materials.advanced_wiring_kit: {_mats.wiring_kit: 1, _mats.gold: 2, _mats.computer_chip: 1},
        Materials.battery: {_mats.acid_mushroom: 2, _mats.copper: 1},
        Materials.power_cell: {_mats.battery: 2, _mats.silicone_rubber: 1},

        # Base Pieces

        Buildings.foundation: {_mats.lead: 2, _mats.titanium: 2},
        Buildings.i_compartment: {_mats.titanium: 2},
        Buildings.l_compartment: {_mats.titanium: 2},
        Buildings.t_compartment: {_mats.titanium: 3},
        Buildings.x_compartment: {_mats.titanium: 3},
        Buildings.glass_i_compartment: {_mats.glass: 2},
        Buildings.glass_l_compartment: {_mats.glass: 2},
        Buildings.vertical_connector: {_mats.titanium: 2},
        Buildings.multipurpose_room: {_mats.titanium: 6},
        Buildings.scanner_room: {_mats.titanium: 5, _mats.copper: 2, _mats.gold: 1, _mats.table_coral_sample: 1},
        Buildings.moonpool: {_mats.titanium_ingot: 2, _mats.lubricant: 1, _mats.lead: 2},
        Buildings.observatory: {_mats.enamaled_glass: 2, _mats.titanium: 1},
        Buildings.hatch: {_mats.titanium: 2, _mats.quartz: 1},
        Buildings.window: {_mats.glass: 1},
        Buildings.reinforcement: {_mats.titanium: 3, _mats.lithium: 1},

        # Power Pieces

        Buildings.bioreactor: {_mats.titanium: 3, _mats.wiring_kit: 1, _mats.lubricant: 1},
        Buildings.nuclear_reactor: {_mats.plasteel_ingot: 1, _mats.advanced_wiring_kit: 1, _mats.lead: 3},
        Buildings.solar_panel: {_mats.quartz: 2, _mats.titanium: 2, _mats.copper: 1},
        Buildings.thermal_plant: {_mats.titanium: 5, _mats.magnetite: 2, _mats.aerogel: 1},
        Buildings.power_transmitter: {_mats.gold: 1, _mats.titanium: 1},

        # Building Pieces

        Buildings.Exterior.floodlight: {_mats.glass: 1, _mats.titanium: 1},
        Buildings.Exterior.spotlight: {_mats.glass: 1, _mats.titanium: 2},
        Buildings.Exterior.exterior_growbed: {_mats.titanium: 2},
        Buildings.Exterior.base_air_pump: {_mats.titanium: 2},

        Buildings.Interior.Pieces.ladder: {_mats.titanium: 2},
        Buildings.Interior.Pieces.water_filtration_pump: {_mats.titanium: 3, _mats.copper_wire: 1, _mats.aerogel: 1},
        Buildings.Interior.Pieces.vehicle_upgrade_console: {_mats.titanium: 3, _mats.computer_chip: 1, _mats.copper_wire: 1},
        Buildings.Interior.Pieces.alien_containment: {_mats.glass: 5, _mats.titanium: 2},

        Buildings.Interior.Modules.fabricator: {_mats.titanium: 1, _mats.gold: 1, _mats.table_coral_sample: 1},
        Buildings.Interior.Modules.radio: {_mats.titanium: 1, _mats.copper: 1},
        Buildings.Interior.Modules.med_kit_fabricator: {_mats.computer_chip: 1, _mats.fiber_mesh: 1, _mats.silver: 1, _mats.titanium: 1},
        Buildings.Interior.Modules.wall_locker: {_mats.titanium: 2},
        Buildings.Interior.Modules.locker: {_mats.quartz: 1, _mats.titanium: 2},
        Buildings.Interior.Modules.battery_charger: {_mats.wiring_kit: 1, _mats.copper_wire: 1, _mats.titanium: 1},
        Buildings.Interior.Modules.power_cell_charger: {_mats.advanced_wiring_kit: 1, _mats.ruby: 2, _mats.titanium: 2},
        Buildings.Interior.Modules.aquarium: {_mats.glass: 2, _mats.titanium: 1},
        Buildings.Interior.Modules.modification_station: {_mats.computer_chip: 1, _mats.titanium: 1, _mats.diamond: 1, _mats.lead: 1},
        Buildings.Interior.Modules.plant_pot: {_mats.titanium: 2},
        Buildings.Interior.Modules.indoor_growbed: {_mats.titanium: 4},
        Buildings.Interior.Modules.plant_shelf: {_mats.titanium: 1},

        # Vehicles

        Vehicles.seamoth: {_mats.titanium_ingot: 1, _mats.power_cell: 1, _mats.glass: 2, _mats.lubricant: 1, _mats.lead: 1},
        Vehicles.prawn_suit: {_mats.plasteel_ingot: 2, _mats.aerogel: 2, _mats.enamaled_glass: 1, _mats.diamond: 2, _mats.lead: 2},
    }


material_dict = dict[Type[M], Union[int, "material_dict"]]


def flatten_dict(d: material_dict, *, first_step: bool = True) -> list[tuple[KT, VT]]:
    tuples = []

    for k, v in d.items():
        if isinstance(v, dict):
            tuples.extend(flatten_dict(v, first_step=False))
        else:
            tuples.append((k, v))

    return tuples if not first_step else sum_tuples(tuples)


def sum_tuples(tuples: Iterable[tuple[M, int]]):
    counters = [Counter({k: v}) for (k, v) in tuples]

    return dict(sum(counters, start=Counter()))


def recipe_for(item: Type[M], *, stages: bool = True, flatten: bool = False):
    """Crafting Materials for an item"""
    cls = Recipe

    recipe = cls._craft_dict[item]

    if not (flatten or stages):
        return recipe

    for material in recipe:
        if not material._is_raw:
            recipe[material] = recipe_for(material, flatten=True)

    if not flatten:
        return recipe

    return flatten_dict(recipe)


base_pieces = {
    "Foundation": Buildings.foundation,
    "Multipurpose Room": Buildings.multipurpose_room,
    "I-compartment": Buildings.i_compartment,
    "L-compartment": Buildings.l_compartment,
    "T-compartment": Buildings.t_compartment,
    "X-compartment": Buildings.x_compartment,
    "Glass I-compartment": Buildings.glass_i_compartment,
    "Glass L-compartment": Buildings.glass_l_compartment,
    "Vertical Connector": Buildings.vertical_connector,
    "Scanner Room": Buildings.scanner_room,
    "Moonpool": Buildings.moonpool,
    "Observatory": Buildings.observatory,
    "Window": Buildings.window,
    "Bulkhead": Buildings.bulkhead,
    "Reinforcement": Buildings.reinforcement,
    "Hatch": Buildings.hatch,
}


interior_pieces = {
    "Alien Containment": Buildings.Interior.Pieces.alien_containment,
    "Ladder": Buildings.Interior.Pieces.ladder,
    "Vehicle Upgrade Console": Buildings.Interior.Pieces.vehicle_upgrade_console,
    "Water Filtration Pump": Buildings.Interior.Pieces.water_filtration_pump,
}


interior_modules = {
    "Fabricator": Buildings.Interior.Modules.fabricator,
    "Radio": Buildings.Interior.Modules.radio,
    "Medkit Fabricator": Buildings.Interior.Modules.med_kit_fabricator,
    "Wall Locker": Buildings.Interior.Modules.wall_locker,
    "Locker": Buildings.Interior.Modules.locker,
    "Battery Charger": Buildings.Interior.Modules.battery_charger,
    "Power Cell Charger": Buildings.Interior.Modules.power_cell_charger,
    "Aquarium": Buildings.Interior.Modules.aquarium,
    "Modification Station": Buildings.Interior.Modules.modification_station,
    "Plant Pot": Buildings.Interior.Modules.plant_pot,
    "Interior Growbed": Buildings.Interior.Modules.indoor_growbed,
    "Plant Shelf": Buildings.Interior.Modules.plant_shelf,
}


power_sources = {
    "Bioreactor": Buildings.bioreactor,
    "Nuclear Reactor": Buildings.nuclear_reactor,
    "Solar Panel": Buildings.solar_panel,
    "Thermal Plant": Buildings.thermal_plant,
    "Power Transmitter": Buildings.power_transmitter,
}

# flake8: noqa