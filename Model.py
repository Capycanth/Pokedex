from dataclasses import dataclass
from enum import Enum

class BallType(Enum):
    POKE = "Poke Ball"
    GREAT = "Great Ball"
    ULTRA = "Ultra Ball"
    MASTER = "Master Ball"
    LOVE = "Love Ball"
    PARK = "Park Ball"
    NONE = "None"

@dataclass
class Addition:
    name: str
    form: str | None

@dataclass
class SuccessUpdate:
    name: str
    form: str | None
    ball: BallType
    index: int

@dataclass
class ErrorUpdate:
    name: str
    form: str | None
    msg: str

@dataclass
class PokedexEntry:
    number: int
    name: str
    form: str | None
    ball: BallType
    count: int
    added: bool = False

@dataclass
class DatabaseEntry:
    number: int
    name: str
    form: str | None
