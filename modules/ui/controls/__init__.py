"""
Módulo de Controles
Sistema modular para controles de interfaz de usuario
"""

from .ui_controller import UIController, UIComponent, UIEvent, UIState, UIComponentType, UIEventType, get_ui_controller, create_ui_event
from .genetic_controls import GeneticControls, GeneticControlConfig, GeneticControlResult, get_genetic_controls
from .passport_controls import PassportControls, PassportControlConfig, PassportControlResult, get_passport_controls
from .template_controls import TemplateControls, TemplateControlConfig, TemplateControlResult, get_template_controls

__all__ = [
    "UIController",
    "UIComponent",
    "UIEvent",
    "UIState",
    "UIComponentType",
    "UIEventType",
    "get_ui_controller",
    "create_ui_event",
    "GeneticControls",
    "GeneticControlConfig",
    "GeneticControlResult",
    "get_genetic_controls",
    "PassportControls",
    "PassportControlConfig",
    "PassportControlResult",
    "get_passport_controls",
    "TemplateControls",
    "TemplateControlConfig",
    "TemplateControlResult",
    "get_template_controls",
]
