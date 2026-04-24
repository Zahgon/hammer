from enum import Enum
from typing import Callable, NamedTuple, Optional, TYPE_CHECKING
__all__ = ['HammerStepFunction', 'HammerToolStep', 'HookLocation', 'HammerToolHookAction']
if TYPE_CHECKING:
    from .hammer_tool import HammerTool
HammerStepFunction = Callable[['HammerTool'], bool]
HammerToolStep = NamedTuple('HammerToolStep', [('func', HammerStepFunction), ('name', str)])
HammerStartStopStep = NamedTuple('HammerStartStopStep', [('step', Optional[str]), ('inclusive', bool)])

class HookLocation(Enum):
    InsertPreStep = 1
    InsertPostStep = 2
    ReplaceStep = 10
    ResumePreStep = 20
    ResumePostStep = 21
    PausePreStep = 30
    PausePostStep = 31
    PersistentStep = 40
    PersistentPreStep = 41
    PersistentPostStep = 42
HammerToolHookAction = NamedTuple('HammerToolHookAction', [('location', HookLocation), ('target_name', str), ('step', Optional[HammerToolStep])])
