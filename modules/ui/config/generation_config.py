"""
Configuración de Generación
Configuraciones centralizadas para generación de imágenes
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path

@dataclass
class GenerationConfig:
    """Configuración base para generación de imágenes"""
    
    # Configuración SAIME
    saime_width: int = 512
    saime_height: int = 768
    saime_aspect_ratio: float = 512 / 768
    
    # Configuración por defecto
    default_width: int = 512
    default_height: int = 768
    default_steps: int = 35
    default_cfg_scale: float = 12.0
    default_sampler: str = "DPM++ 2M Karras"
    
    # Configuración de memoria
    memory_cleanup_interval: int = 5  # Cada 5 imágenes
    max_batch_size: int = 8
    memory_threshold: float = 0.85
    
    # Configuración de archivos
    output_base_dir: str = "outputs"
    temp_dir: str = "temp"
    backup_dir: str = "backups"
    
    # Configuración de validación
    saime_validation_enabled: bool = True
    parameter_validation_enabled: bool = True
    
    # Configuración de balanceo
    intelligent_balancing_enabled: bool = True
    max_repetitions: int = 3
    diversity_threshold: float = 0.7
    
    def get_saime_dimensions(self) -> Dict[str, int]:
        """Obtiene dimensiones SAIME"""
        return {
            "width": self.saime_width,
            "height": self.saime_height,
            "aspect_ratio": self.saime_aspect_ratio
        }
    
    def get_default_params(self) -> Dict[str, Any]:
        """Obtiene parámetros por defecto"""
        return {
            "width": self.default_width,
            "height": self.default_height,
            "steps": self.default_steps,
            "cfg_scale": self.default_cfg_scale,
            "sampler": self.default_sampler
        }
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Obtiene configuración de memoria"""
        return {
            "cleanup_interval": self.memory_cleanup_interval,
            "max_batch_size": self.max_batch_size,
            "threshold": self.memory_threshold
        }
    
    def get_validation_config(self) -> Dict[str, bool]:
        """Obtiene configuración de validación"""
        return {
            "saime_enabled": self.saime_validation_enabled,
            "parameter_enabled": self.parameter_validation_enabled
        }
    
    def get_balancing_config(self) -> Dict[str, Any]:
        """Obtiene configuración de balanceo"""
        return {
            "enabled": self.intelligent_balancing_enabled,
            "max_repetitions": self.max_repetitions,
            "diversity_threshold": self.diversity_threshold
        }

# Instancia global de configuración
generation_config = GenerationConfig()

def get_generation_config() -> GenerationConfig:
    """Obtiene la configuración global de generación"""
    return generation_config

def update_generation_config(**kwargs) -> None:
    """Actualiza la configuración de generación"""
    global generation_config
    for key, value in kwargs.items():
        if hasattr(generation_config, key):
            setattr(generation_config, key, value)
