"""
Módulo de Gestión de Plantillas
Sistema modular para gestión de plantillas de configuración
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
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
class TemplateInfo:
    """Información de una plantilla"""
    name: str
    file_path: str
    created_at: str
    description: str = ""
    version: str = "1.0"
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TemplateManagerConfig:
    """Configuración del gestor de plantillas"""
    templates_dir: str = "outputs/templates"
    max_name_length: int = 50
    allowed_characters: str = r'^[a-zA-Z0-9\s\-_áéíóúñÁÉÍÓÚÑ]+$'
    auto_backup: bool = True
    backup_dir: str = "outputs/templates/backups"
    max_templates: int = 100
    default_version: str = "1.0"

class TemplateManager:
    """Gestor de plantillas de configuración"""
    
    def __init__(self, config: Optional[TemplateManagerConfig] = None):
        self.config = config if config else TemplateManagerConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_handler = None
        self.file_manager = None
        self.ui_controller = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self.error_handler = get_error_handler()
            self.file_manager = get_file_manager()
            self.ui_controller = get_ui_controller()
        
        # Crear directorio de plantillas
        self._ensure_templates_directory()
    
    def load_template(self, template_path: str) -> Dict[str, Any]:
        """Carga una plantilla desde un archivo"""
        try:
            if not template_path or not Path(template_path).exists():
                return {
                    "success": False,
                    "error": "Archivo de plantilla no encontrado",
                    "template": None
                }
            
            # Leer plantilla
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # Validar estructura de plantilla
            if not self._validate_template_structure(template_data):
                return {
                    "success": False,
                    "error": "Estructura de plantilla inválida",
                    "template": None
                }
            
            return {
                "success": True,
                "template": template_data,
                "file_path": template_path
            }
            
        except Exception as e:
            self.logger.error(f"Error cargando plantilla: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "loading template", "template_path": template_path})
            
            return {
                "success": False,
                "error": f"Error cargando plantilla: {str(e)}",
                "template": None
            }
    
    def save_template(self, template_name: str, parameters: Dict[str, Any], description: str = "") -> Dict[str, Any]:
        """Guarda una plantilla con los parámetros dados"""
        try:
            # Validar nombre de plantilla
            validation_result = self._validate_template_name(template_name)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "file_path": None
                }
            
            # Crear información de plantilla
            template_info = {
                "nombre": template_name,
                "fecha_creacion": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": self.config.default_version,
                "descripcion": description or f"Plantilla personalizada creada el {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "configuracion": parameters,
                "metadata": {
                    "created_by": "TemplateManager",
                    "total_parameters": len(parameters),
                    "template_type": "ui_configuration"
                }
            }
            
            # Crear nombre de archivo seguro
            safe_filename = self._create_safe_filename(template_name)
            file_path = Path(self.config.templates_dir) / f"{safe_filename}.json"
            
            # Verificar si ya existe
            if file_path.exists():
                return {
                    "success": False,
                    "error": f"Ya existe una plantilla con el nombre '{template_name}'. Elige otro nombre.",
                    "file_path": None
                }
            
            # Crear backup si está habilitado
            if self.config.auto_backup:
                self._create_backup(file_path)
            
            # Guardar plantilla
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template_info, f, indent=2, ensure_ascii=False)
            
            # Actualizar UI si está disponible
            if self.ui_controller:
                event = create_ui_event(
                    UIEventType.CHANGE,
                    "template_saved",
                    {"template_name": template_name, "file_path": str(file_path)}
                )
                self.ui_controller.handle_event(event)
            
            return {
                "success": True,
                "file_path": str(file_path),
                "template_info": template_info
            }
            
        except Exception as e:
            self.logger.error(f"Error guardando plantilla: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "saving template", "template_name": template_name})
            
            return {
                "success": False,
                "error": f"Error guardando plantilla: {str(e)}",
                "file_path": None
            }
    
    def delete_template(self, template_path: str) -> Dict[str, Any]:
        """Elimina una plantilla"""
        try:
            if not template_path or not Path(template_path).exists():
                return {
                    "success": False,
                    "error": "Archivo de plantilla no encontrado"
                }
            
            # Leer información de la plantilla antes de eliminar
            template_name = "Plantilla sin nombre"
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                template_name = template_data.get('nombre', Path(template_path).stem)
            except:
                template_name = Path(template_path).stem
            
            # Crear backup si está habilitado
            if self.config.auto_backup:
                self._create_backup(Path(template_path))
            
            # Eliminar archivo
            Path(template_path).unlink()
            
            # Actualizar UI si está disponible
            if self.ui_controller:
                event = create_ui_event(
                    UIEventType.CHANGE,
                    "template_deleted",
                    {"template_name": template_name, "file_path": template_path}
                )
                self.ui_controller.handle_event(event)
            
            return {
                "success": True,
                "template_name": template_name,
                "deleted_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.logger.error(f"Error eliminando plantilla: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "deleting template", "template_path": template_path})
            
            return {
                "success": False,
                "error": f"Error eliminando plantilla: {str(e)}"
            }
    
    def list_templates(self) -> Dict[str, Any]:
        """Lista todas las plantillas disponibles"""
        try:
            templates_dir = Path(self.config.templates_dir)
            if not templates_dir.exists():
                return {
                    "success": True,
                    "templates": [],
                    "count": 0
                }
            
            templates = []
            for file_path in templates_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    
                    template_info = TemplateInfo(
                        name=template_data.get("nombre", file_path.stem),
                        file_path=str(file_path),
                        created_at=template_data.get("fecha_creacion", "Desconocida"),
                        description=template_data.get("descripcion", ""),
                        version=template_data.get("version", self.config.default_version),
                        parameters=template_data.get("configuracion", {}),
                        metadata=template_data.get("metadata", {})
                    )
                    templates.append(template_info)
                    
                except Exception as e:
                    self.logger.warning(f"Error leyendo plantilla {file_path}: {e}")
                    continue
            
            # Ordenar por fecha de creación (más recientes primero)
            templates.sort(key=lambda x: x.created_at, reverse=True)
            
            return {
                "success": True,
                "templates": templates,
                "count": len(templates)
            }
            
        except Exception as e:
            self.logger.error(f"Error listando plantillas: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "listing templates"})
            
            return {
                "success": False,
                "error": f"Error listando plantillas: {str(e)}",
                "templates": [],
                "count": 0
            }
    
    def get_template_info(self, template_path: str) -> Dict[str, Any]:
        """Obtiene información detallada de una plantilla"""
        try:
            if not template_path or not Path(template_path).exists():
                return {
                    "success": False,
                    "error": "Archivo de plantilla no encontrado",
                    "info": None
                }
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            template_info = TemplateInfo(
                name=template_data.get("nombre", Path(template_path).stem),
                file_path=template_path,
                created_at=template_data.get("fecha_creacion", "Desconocida"),
                description=template_data.get("descripcion", ""),
                version=template_data.get("version", self.config.default_version),
                parameters=template_data.get("configuracion", {}),
                metadata=template_data.get("metadata", {})
            )
            
            return {
                "success": True,
                "info": template_info
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo información de plantilla: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "getting template info", "template_path": template_path})
            
            return {
                "success": False,
                "error": f"Error obteniendo información: {str(e)}",
                "info": None
            }
    
    def update_template(self, template_path: str, parameters: Dict[str, Any], description: str = None) -> Dict[str, Any]:
        """Actualiza una plantilla existente"""
        try:
            if not template_path or not Path(template_path).exists():
                return {
                    "success": False,
                    "error": "Archivo de plantilla no encontrado"
                }
            
            # Cargar plantilla existente
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # Actualizar datos
            template_data["configuracion"] = parameters
            if description:
                template_data["descripcion"] = description
            template_data["fecha_modificacion"] = time.strftime("%Y-%m-%d %H:%M:%S")
            template_data["metadata"]["last_modified"] = time.strftime("%Y-%m-%d %H:%M:%S")
            template_data["metadata"]["total_parameters"] = len(parameters)
            
            # Crear backup si está habilitado
            if self.config.auto_backup:
                self._create_backup(Path(template_path))
            
            # Guardar plantilla actualizada
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "template_data": template_data
            }
            
        except Exception as e:
            self.logger.error(f"Error actualizando plantilla: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "updating template", "template_path": template_path})
            
            return {
                "success": False,
                "error": f"Error actualizando plantilla: {str(e)}"
            }
    
    def _validate_template_name(self, name: str) -> Dict[str, Any]:
        """Valida el nombre de una plantilla"""
        try:
            if not name or not name.strip():
                return {"valid": False, "error": "El nombre de la plantilla no puede estar vacío"}
            
            name = name.strip()
            
            # Validar caracteres permitidos
            if not re.match(self.config.allowed_characters, name):
                return {"valid": False, "error": "El nombre solo puede contener letras, números, espacios, guiones y guiones bajos"}
            
            # Validar longitud
            if len(name) > self.config.max_name_length:
                return {"valid": False, "error": f"El nombre no puede tener más de {self.config.max_name_length} caracteres"}
            
            return {"valid": True}
            
        except Exception as e:
            return {"valid": False, "error": f"Error validando nombre: {str(e)}"}
    
    def _create_safe_filename(self, name: str) -> str:
        """Crea un nombre de archivo seguro"""
        # Reemplazar caracteres no seguros
        safe_name = re.sub(r'[^\w\-_áéíóúñÁÉÍÓÚÑ]', '_', name)
        # Limitar longitud
        if len(safe_name) > 50:
            safe_name = safe_name[:50]
        return safe_name
    
    def _validate_template_structure(self, template_data: Dict[str, Any]) -> bool:
        """Valida la estructura de una plantilla"""
        try:
            required_fields = ["nombre", "configuracion"]
            for field in required_fields:
                if field not in template_data:
                    return False
            
            # Validar que configuracion es un diccionario
            if not isinstance(template_data["configuracion"], dict):
                return False
            
            return True
            
        except Exception:
            return False
    
    def _ensure_templates_directory(self):
        """Asegura que el directorio de plantillas existe"""
        try:
            templates_dir = Path(self.config.templates_dir)
            templates_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear directorio de backups si está habilitado
            if self.config.auto_backup:
                backup_dir = Path(self.config.backup_dir)
                backup_dir.mkdir(parents=True, exist_ok=True)
                
        except Exception as e:
            self.logger.error(f"Error creando directorio de plantillas: {e}")
    
    def _create_backup(self, file_path: Path):
        """Crea un backup de un archivo"""
        try:
            if not self.config.auto_backup:
                return
            
            backup_dir = Path(self.config.backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name
            
            # Copiar archivo
            import shutil
            shutil.copy2(file_path, backup_path)
            
        except Exception as e:
            self.logger.warning(f"Error creando backup de {file_path}: {e}")

# Instancia global
_template_manager_instance: Optional[TemplateManager] = None

def get_template_manager() -> TemplateManager:
    """Obtiene la instancia global de TemplateManager"""
    global _template_manager_instance
    if _template_manager_instance is None:
        _template_manager_instance = TemplateManager()
    return _template_manager_instance
