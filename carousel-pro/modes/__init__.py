"""
Carousel Pro Modes Package
Multi-Mode Design System for Instagram Carousels
"""

from .base_mode import BaseMode
from .corporate_mode import CorporateMode
from .startup_mode import StartupMode
from .lifestyle_mode import LifestyleMode
from .wellness_mode import WellnessMode
from .creator_mode import CreatorMode

__all__ = [
    'BaseMode',
    'CorporateMode',
    'StartupMode',
    'LifestyleMode',
    'WellnessMode',
    'CreatorMode',
]

# Mode registry for easy access
MODES = {
    'corporate': CorporateMode,
    'startup': StartupMode,
    'lifestyle': LifestyleMode,
    'wellness': WellnessMode,
    'creator': CreatorMode,
}

def get_mode(mode_name: str):
    """Get mode class by name"""
    mode_class = MODES.get(mode_name.lower())
    if mode_class:
        return mode_class()
    return None

def list_modes():
    """List all available modes"""
    return {
        name: {
            'name': mode_class.name,
            'description': mode_class.description,
            'audience': mode_class.audience
        }
        for name, mode_class in MODES.items()
    }
