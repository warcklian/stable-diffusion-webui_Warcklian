"""
Módulo de Gestión de Configuración
Sistema modular para gestión de configuración del sistema
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
import logging

# Imports de módulos de optimización
try:
    from modules.ui.utils import get_error_handler, get_file_manager
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

@dataclass
class ConfigSection:
    """Sección de configuración"""
    name: str
    description: str = ""
    settings: Dict[str, Any] = field(default_factory=dict)
    is_required: bool = False
    validation_rules: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConfigManagerConfig:
    """Configuración del gestor de configuración"""
    config_file: str = "outputs/config/system_config.json"
    backup_dir: str = "outputs/config/backups"
    auto_backup: bool = True
    auto_save: bool = True
    validation_enabled: bool = True
    max_backups: int = 10
    default_sections: List[str] = field(default_factory=lambda: [
        "ui", "generation", "validation", "performance", "templates"
    ])

class ConfigManager:
    """Gestor de configuración del sistema"""
    
    def __init__(self, config: Optional[ConfigManagerConfig] = None):
        self.config = config if config else ConfigManagerConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_handler = None
        self.file_manager = None
        self.ui_controller = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self.error_handler = get_error_handler()
            self.file_manager = get_file_manager()
            self.ui_controller = get_ui_controller()
        
        # Cargar configuración existente
        self._load_config()
    
    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene la configuración del sistema"""
        try:
            if section:
                if section not in self.config_data:
                    return {
                        "success": False,
                        "error": f"Sección '{section}' no encontrada",
                        "config": None
                    }
                
                return {
                    "success": True,
                    "config": {section: self.config_data[section]},
                    "section": section
                }
            
            return {
                "success": True,
                "config": self.config_data,
                "sections": list(self.config_data.keys())
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo configuración: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "getting config", "section": section})
            
            return {
                "success": False,
                "error": f"Error obteniendo configuración: {str(e)}",
                "config": None
            }
    
    def update_config(self, section: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza la configuración de una sección"""
        try:
            if not section:
                return {
                    "success": False,
                    "error": "Sección no especificada"
                }
            
            # Validar configuración si está habilitado
            if self.config.validation_enabled:
                validation_result = self._validate_config_section(section, settings)
                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "error": f"Configuración inválida: {validation_result['error']}"
                    }
            
            # Crear backup si está habilitado
            if self.config.auto_backup:
                self._create_config_backup()
            
            # Actualizar configuración
            if section not in self.config_data:
                self.config_data[section] = {}
            
            self.config_data[section].update(settings)
            self.config_data[section]["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Guardar configuración si está habilitado
            if self.config.auto_save:
                save_result = self._save_config()
                if not save_result["success"]:
                    return {
                        "success": False,
                        "error": f"Error guardando configuración: {save_result['error']}"
                    }
            
            # Actualizar UI si está disponible
            if self.ui_controller:
                event = create_ui_event(
                    UIEventType.CHANGE,
                    "config_updated",
                    {"section": section, "settings": settings}
                )
                self.ui_controller.handle_event(event)
            
            return {
                "success": True,
                "section": section,
                "updated_settings": settings
            }
            
        except Exception as e:
            self.logger.error(f"Error actualizando configuración: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "updating config", "section": section})
            
            return {
                "success": False,
                "error": f"Error actualizando configuración: {str(e)}"
            }
    
    def validate_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """Valida la configuración del sistema"""
        try:
            if not self.config.validation_enabled:
                return {
                    "success": True,
                    "valid": True,
                    "message": "Validación deshabilitada"
                }
            
            validation_results = {}
            is_valid = True
            
            sections_to_validate = [section] if section else self.config_data.keys()
            
            for sec in sections_to_validate:
                if sec in self.config_data:
                    result = self._validate_config_section(sec, self.config_data[sec])
                    validation_results[sec] = result
                    if not result["valid"]:
                        is_valid = False
            
            return {
                "success": True,
                "valid": is_valid,
                "validation_results": validation_results,
                "sections_validated": sections_to_validate
            }
            
        except Exception as e:
            self.logger.error(f"Error validando configuración: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "validating config", "section": section})
            
            return {
                "success": False,
                "error": f"Error validando configuración: {str(e)}",
                "valid": False
            }
    
    def reset_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """Resetea la configuración a valores por defecto"""
        try:
            # Crear backup antes de resetear
            if self.config.auto_backup:
                self._create_config_backup()
            
            if section:
                # Resetear sección específica
                if section in self.config_data:
                    self.config_data[section] = self._get_default_section_config(section)
                else:
                    return {
                        "success": False,
                        "error": f"Sección '{section}' no encontrada"
                    }
            else:
                # Resetear toda la configuración
                self.config_data = self._get_default_config()
            
            # Guardar configuración
            save_result = self._save_config()
            if not save_result["success"]:
                return {
                    "success": False,
                    "error": f"Error guardando configuración: {save_result['error']}"
                }
            
            # Actualizar UI si está disponible
            if self.ui_controller:
                event = create_ui_event(
                    UIEventType.CHANGE,
                    "config_reset",
                    {"section": section}
                )
                self.ui_controller.handle_event(event)
            
            return {
                "success": True,
                "reset_section": section,
                "reset_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.logger.error(f"Error reseteando configuración: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "resetting config", "section": section})
            
            return {
                "success": False,
                "error": f"Error reseteando configuración: {str(e)}"
            }
    
    def add_config_section(self, section: str, description: str = "", is_required: bool = False) -> Dict[str, Any]:
        """Añade una nueva sección de configuración"""
        try:
            if section in self.config_data:
                return {
                    "success": False,
                    "error": f"La sección '{section}' ya existe"
                }
            
            # Crear nueva sección
            self.config_data[section] = {
                "description": description,
                "is_required": is_required,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "settings": {}
            }
            
            # Guardar configuración
            save_result = self._save_config()
            if not save_result["success"]:
                return {
                    "success": False,
                    "error": f"Error guardando configuración: {save_result['error']}"
                }
            
            return {
                "success": True,
                "section": section,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.logger.error(f"Error añadiendo sección de configuración: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "adding config section", "section": section})
            
            return {
                "success": False,
                "error": f"Error añadiendo sección: {str(e)}"
            }
    
    def remove_config_section(self, section: str) -> Dict[str, Any]:
        """Elimina una sección de configuración"""
        try:
            if section not in self.config_data:
                return {
                    "success": False,
                    "error": f"La sección '{section}' no existe"
                }
            
            # Verificar si es requerida
            if self.config_data[section].get("is_required", False):
                return {
                    "success": False,
                    "error": f"No se puede eliminar la sección '{section}' porque es requerida"
                }
            
            # Crear backup antes de eliminar
            if self.config.auto_backup:
                self._create_config_backup()
            
            # Eliminar sección
            del self.config_data[section]
            
            # Guardar configuración
            save_result = self._save_config()
            if not save_result["success"]:
                return {
                    "success": False,
                    "error": f"Error guardando configuración: {save_result['error']}"
                }
            
            return {
                "success": True,
                "removed_section": section,
                "removed_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.logger.error(f"Error eliminando sección de configuración: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "removing config section", "section": section})
            
            return {
                "success": False,
                "error": f"Error eliminando sección: {str(e)}"
            }
    
    def _load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            config_file = Path(self.config.config_file)
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
            else:
                # Crear configuración por defecto
                self.config_data = self._get_default_config()
                self._save_config()
                
        except Exception as e:
            self.logger.error(f"Error cargando configuración: {e}")
            self.config_data = self._get_default_config()
    
    def _save_config(self) -> Dict[str, Any]:
        """Guarda la configuración en el archivo"""
        try:
            config_file = Path(self.config.config_file)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            return {"success": True}
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Obtiene la configuración por defecto"""
        return {
            "ui": {
                "theme": "default",
                "language": "es",
                "auto_save": True,
                "show_advanced_controls": True,
                "default_width": 512,
                "default_height": 768
            },
            "generation": {
                "default_steps": 20,
                "default_cfg_scale": 7.0,
                "default_sampler": "Euler a",
                "default_scheduler": "karras",
                "max_batch_size": 10,
                "memory_optimization": True
            },
            "validation": {
                "saime_validation": True,
                "advanced_validation": True,
                "auto_validate": True,
                "strict_mode": False
            },
            "performance": {
                "memory_optimization": True,
                "batch_optimization": True,
                "progress_reporting": True,
                "error_handling": "continue"
            },
            "templates": {
                "auto_backup": True,
                "max_templates": 100,
                "default_version": "1.0"
            }
        }
    
    def _get_default_section_config(self, section: str) -> Dict[str, Any]:
        """Obtiene la configuración por defecto de una sección"""
        default_config = self._get_default_config()
        return default_config.get(section, {})
    
    def _validate_config_section(self, section: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Valida una sección de configuración"""
        try:
            # Reglas de validación básicas
            validation_rules = {
                "ui": {
                    "required_fields": ["theme", "language"],
                    "field_types": {
                        "theme": str,
                        "language": str,
                        "auto_save": bool,
                        "show_advanced_controls": bool,
                        "default_width": int,
                        "default_height": int
                    }
                },
                "generation": {
                    "required_fields": ["default_steps", "default_cfg_scale"],
                    "field_types": {
                        "default_steps": int,
                        "default_cfg_scale": float,
                        "default_sampler": str,
                        "default_scheduler": str,
                        "max_batch_size": int,
                        "memory_optimization": bool
                    }
                },
                "validation": {
                    "required_fields": ["saime_validation", "advanced_validation"],
                    "field_types": {
                        "saime_validation": bool,
                        "advanced_validation": bool,
                        "auto_validate": bool,
                        "strict_mode": bool
                    }
                },
                "performance": {
                    "required_fields": ["memory_optimization"],
                    "field_types": {
                        "memory_optimization": bool,
                        "batch_optimization": bool,
                        "progress_reporting": bool,
                        "error_handling": str
                    }
                },
                "templates": {
                    "required_fields": ["auto_backup"],
                    "field_types": {
                        "auto_backup": bool,
                        "max_templates": int,
                        "default_version": str
                    }
                }
            }
            
            if section not in validation_rules:
                return {"valid": True, "message": f"No hay reglas de validación para la sección '{section}'"}
            
            rules = validation_rules[section]
            
            # Validar campos requeridos
            for field in rules.get("required_fields", []):
                if field not in settings:
                    return {"valid": False, "error": f"Campo requerido '{field}' no encontrado en sección '{section}'"}
            
            # Validar tipos de campos
            field_types = rules.get("field_types", {})
            for field, expected_type in field_types.items():
                if field in settings:
                    if not isinstance(settings[field], expected_type):
                        return {"valid": False, "error": f"Campo '{field}' debe ser de tipo {expected_type.__name__}"}
            
            return {"valid": True, "message": f"Sección '{section}' validada correctamente"}
            
        except Exception as e:
            return {"valid": False, "error": f"Error validando sección: {str(e)}"}
    
    def _create_config_backup(self):
        """Crea un backup de la configuración"""
        try:
            if not self.config.auto_backup:
                return
            
            backup_dir = Path(self.config.backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"config_backup_{timestamp}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            # Limpiar backups antiguos
            self._cleanup_old_backups()
            
        except Exception as e:
            self.logger.warning(f"Error creando backup de configuración: {e}")
    
    def _cleanup_old_backups(self):
        """Limpia backups antiguos"""
        try:
            backup_dir = Path(self.config.backup_dir)
            if not backup_dir.exists():
                return
            
            backup_files = list(backup_dir.glob("config_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Mantener solo los últimos N backups
            for backup_file in backup_files[self.config.max_backups:]:
                backup_file.unlink()
                
        except Exception as e:
            self.logger.warning(f"Error limpiando backups antiguos: {e}")

# Instancia global
_config_manager_instance: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """Obtiene la instancia global de ConfigManager"""
    global _config_manager_instance
    if _config_manager_instance is None:
        _config_manager_instance = ConfigManager()
    return _config_manager_instance
