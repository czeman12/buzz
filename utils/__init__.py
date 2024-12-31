# utils/__init__.py

from .db_utils import (
    get_db_connection,
    release_db_connection,
    initialize_connection_pool,
)
from .style_loader import load_stylesheet, apply_stylesheet
from .scalable_widget import ScalableWidget  # Import ScalableWidget
from .scaling_helper import ScalingHelper  # Optional: Import ScalingHelper if needed
from .matplotlib_style import apply_dark_theme  # Ensure this is necessary
from .assets import get_icon_path, load_application_icon, load_titlebar_icon

__all__ = [
    "get_db_connection",
    "release_db_connection",
    "initialize_connection_pool",
    "load_stylesheet",
    "apply_stylesheet",
    "ScalableWidget",  # Include ScalableWidget in __all__
    "apply_dark_theme",
    "get_icon_path",
    "load_application_icon",
    "load_titlebar_icon",
    # Include if you want to expose it
    # "ScalingHelper",     # Include if you want to expose it
]
