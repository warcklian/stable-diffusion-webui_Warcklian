"""
Módulo de Configuración
Sistema modular para configuración de UI y generación
"""

from .ui_config import UIConfig, get_ui_config, update_ui_config
from .generation_config import GenerationConfig, get_generation_config, update_generation_config
from .template_manager import TemplateManager, TemplateInfo, TemplateManagerConfig, get_template_manager
from .config_manager import ConfigManager, ConfigSection, ConfigManagerConfig, get_config_manager

__all__ = [
    "UIConfig",
    "GenerationConfig",
    "get_ui_config",
    "update_ui_config", 
    "get_generation_config",
    "update_generation_config",
    "TemplateManager",
    "TemplateInfo",
    "TemplateManagerConfig",
    "get_template_manager",
    "ConfigManager",
    "ConfigSection",
    "ConfigManagerConfig",
    "get_config_manager",
]
