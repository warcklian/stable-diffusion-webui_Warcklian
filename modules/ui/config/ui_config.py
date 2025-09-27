"""
Configuración de UI
Configuraciones centralizadas para la interfaz de usuario
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path

@dataclass
class UIConfig:
    """Configuración de interfaz de usuario"""
    
    # Configuración de colores y estilos
    left_column_color: str = "rgba(173, 216, 230, 0.2)"
    right_column_color: str = "rgba(144, 238, 144, 0.2)"
    genetic_accordion_color: str = "rgba(138, 43, 226, 0.15)"
    passport_accordion_color: str = "rgba(34, 139, 34, 0.15)"
    gallery_color: str = "rgba(255, 165, 0, 0.15)"
    
    # Configuración de dimensiones por defecto
    default_width: int = 512
    default_height: int = 768
    
    # Configuración de controles
    show_advanced_controls: bool = True
    show_balancing_controls: bool = True
    show_validation_controls: bool = True
    
    # Configuración de progreso
    progress_update_interval: int = 1  # segundos
    show_detailed_progress: bool = True
    
    # Configuración de archivos
    auto_save_config: bool = True
    backup_before_changes: bool = True
    
    def get_css_styles(self) -> str:
        """Obtiene estilos CSS para la interfaz"""
        return f"""
        /* Lado Izquierdo - Configuración Original */
        #left_column_original {{
            background-color: {self.left_column_color} !important;
            border: 3px solid rgba(173, 216, 230, 0.6) !important;
            border-radius: 10px !important;
            padding: 15px !important;
            margin: 10px !important;
        }}
        
        /* Lado Derecho - Pasaportes */
        #right_column_pasaportes {{
            background-color: {self.right_column_color} !important;
            border: 3px solid rgba(144, 238, 144, 0.6) !important;
            border-radius: 10px !important;
            padding: 15px !important;
            margin: 10px !important;
        }}
        
        /* Accordion de Nacionalidad Avanzada */
        .pasaportes_accordion {{
            background-color: {self.passport_accordion_color} !important;
            border: 2px solid rgba(34, 139, 34, 0.5) !important;
            border-radius: 8px !important;
            margin: 8px 0 !important;
        }}
        
        /* Accordion de Controles Genéticos */
        .genetic_accordion {{
            background-color: {self.genetic_accordion_color} !important;
            border: 2px solid rgba(138, 43, 226, 0.5) !important;
            border-radius: 8px !important;
            margin: 8px 0 !important;
        }}
        
        /* Panel de salida (Gallery) */
        .gallery-container {{
            background-color: {self.gallery_color} !important;
            border: 2px solid rgba(255, 165, 0, 0.5) !important;
            border-radius: 8px !important;
            padding: 10px !important;
            margin: 5px !important;
        }}
        """
    
    def get_default_dimensions(self) -> Dict[str, int]:
        """Obtiene dimensiones por defecto"""
        return {
            "width": self.default_width,
            "height": self.default_height
        }
    
    def get_control_config(self) -> Dict[str, bool]:
        """Obtiene configuración de controles"""
        return {
            "advanced": self.show_advanced_controls,
            "balancing": self.show_balancing_controls,
            "validation": self.show_validation_controls
        }
    
    def get_progress_config(self) -> Dict[str, Any]:
        """Obtiene configuración de progreso"""
        return {
            "update_interval": self.progress_update_interval,
            "detailed": self.show_detailed_progress
        }
    
    def get_file_config(self) -> Dict[str, bool]:
        """Obtiene configuración de archivos"""
        return {
            "auto_save": self.auto_save_config,
            "backup": self.backup_before_changes
        }

# Instancia global de configuración UI
ui_config = UIConfig()

def get_ui_config() -> UIConfig:
    """Obtiene la configuración global de UI"""
    return ui_config

def update_ui_config(**kwargs) -> None:
    """Actualiza la configuración de UI"""
    global ui_config
    for key, value in kwargs.items():
        if hasattr(ui_config, key):
            setattr(ui_config, key, value)
