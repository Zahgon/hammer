from enum import Enum
from typing import List, Optional
from pydantic import ConfigDict, BaseModel

class CellType(str, Enum):
    TieHiCell = 'tiehicell'
    TieLoCell = 'tielocell'
    TieHiLoCell = 'tiehilocell'
    EndCap = 'endcap'
    IOFiller = 'iofiller'
    StdFiller = 'stdfiller'
    Decap = 'decap'
    TapCell = 'tapcell'
    Driver = 'driver'
    CTSBuffer = 'ctsbuffer'
    CTSInverter = 'ctsinverter'
    CTSGate = 'ctsgate'
    CTSLogic = 'ctslogic'

class SpecialCell(BaseModel):
    cell_type: CellType
    name: List[str]
    size: Optional[List[str]] = None
    input_ports: Optional[List[str]] = None
    output_ports: Optional[List[str]] = None
    model_config = ConfigDict(use_enum_values=True)
