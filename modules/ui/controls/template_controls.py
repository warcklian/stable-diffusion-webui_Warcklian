"""
Módulo de Controles de Plantillas
Sistema modular para controles de plantillas de generación
"""

import gradio as gr
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging

# Imports de módulos de optimización
try:
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType, UIComponentType
    from modules.ui.validation import get_parameter_validator, GenerationValidationParams
    from modules.ui.utils import get_progress_manager, get_file_manager, get_error_handler
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

@dataclass
class TemplateControlConfig:
    """Configuración de controles de plantillas"""
    template_name: str = "Nueva Plantilla"
    template_type: str = "genetic"
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    is_default: bool = False
    created_date: str = ""
    modified_date: str = ""

@dataclass
class TemplateControlResult:
    """Resultado de controles de plantillas"""
    success: bool
    controls_created: int = 0
    error_message: str = ""
    controls_info: Dict[str, Any] = field(default_factory=dict)

class TemplateControls:
    """Controlador de controles de plantillas"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ui_controller = None
        self.parameter_validator = None
        self.progress_manager = None
        self.file_manager = None
        self.error_handler = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self.ui_controller = get_ui_controller()
            self.parameter_validator = get_parameter_validator()
            self.progress_manager = get_progress_manager()
            self.file_manager = get_file_manager()
            self.error_handler = get_error_handler()
    
    def create_template_ui(self, config: Optional[TemplateControlConfig] = None) -> TemplateControlResult:
        """Crea la interfaz de controles de plantillas"""
        try:
            if config is None:
                config = TemplateControlConfig()
            
            # Crear controles de plantillas
            controls = self._create_template_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_template_controls(controls)
            
            return TemplateControlResult(
                success=True,
                controls_created=len(controls),
                controls_info={"controls": controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles de plantillas: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating template controls"})
            
            return TemplateControlResult(
                success=False,
                error_message=f"Error creando controles de plantillas: {str(e)}"
            )
    
    def create_template_selector(self, config: Optional[TemplateControlConfig] = None) -> TemplateControlResult:
        """Crea selector de plantillas"""
        try:
            if config is None:
                config = TemplateControlConfig()
            
            # Crear selector de plantillas
            selector_controls = self._create_template_selector(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_template_selector(selector_controls)
            
            return TemplateControlResult(
                success=True,
                controls_created=len(selector_controls),
                controls_info={"selector_controls": selector_controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando selector de plantillas: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating template selector"})
            
            return TemplateControlResult(
                success=False,
                error_message=f"Error creando selector de plantillas: {str(e)}"
            )
    
    def create_template_editor(self, config: Optional[TemplateControlConfig] = None) -> TemplateControlResult:
        """Crea editor de plantillas"""
        try:
            if config is None:
                config = TemplateControlConfig()
            
            # Crear editor de plantillas
            editor_controls = self._create_template_editor(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_template_editor(editor_controls)
            
            return TemplateControlResult(
                success=True,
                controls_created=len(editor_controls),
                controls_info={"editor_controls": editor_controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando editor de plantillas: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating template editor"})
            
            return TemplateControlResult(
                success=False,
                error_message=f"Error creando editor de plantillas: {str(e)}"
            )
    
    def _create_template_controls(self, config: TemplateControlConfig) -> List[Dict[str, Any]]:
        """Crea controles básicos de plantillas"""
        controls = []
        
        # Control de nombre de plantilla
        name_control = {
            "id": "template_name_control",
            "type": "textbox",
            "label": "📝 Nombre de Plantilla",
            "value": config.template_name,
            "info": "Nombre de la plantilla",
            "required": True,
            "validation_rules": ["not_empty"]
        }
        controls.append(name_control)
        
        # Control de tipo de plantilla
        type_control = {
            "id": "template_type_control",
            "type": "dropdown",
            "label": "🏷️ Tipo de Plantilla",
            "choices": ["genetic", "passport", "mixed"],
            "value": config.template_type,
            "info": "Tipo de plantilla"
        }
        controls.append(type_control)
        
        # Control de descripción
        description_control = {
            "id": "template_description_control",
            "type": "textbox",
            "label": "📄 Descripción",
            "value": config.description,
            "info": "Descripción de la plantilla"
        }
        controls.append(description_control)
        
        # Control de plantilla por defecto
        default_control = {
            "id": "template_default_control",
            "type": "checkbox",
            "label": "⭐ Plantilla por Defecto",
            "value": config.is_default,
            "info": "Marcar como plantilla por defecto"
        }
        controls.append(default_control)
        
        return controls
    
    def _create_template_selector(self, config: TemplateControlConfig) -> List[Dict[str, Any]]:
        """Crea selector de plantillas"""
        controls = []
        
        # Cargar plantillas disponibles
        available_templates = self._get_available_templates()
        
        # Control de selección de plantilla
        template_selector = {
            "id": "template_selector",
            "type": "dropdown",
            "label": "📂 Seleccionar Plantilla",
            "choices": available_templates,
            "value": available_templates[0] if available_templates else "Nueva Plantilla",
            "info": "Selecciona una plantilla guardada"
        }
        controls.append(template_selector)
        
        # Botón de cargar plantilla
        load_button = {
            "id": "load_template_button",
            "type": "button",
            "label": "📂 Cargar Plantilla",
            "value": "Cargar",
            "info": "Cargar la plantilla seleccionada"
        }
        controls.append(load_button)
        
        # Botón de eliminar plantilla
        delete_button = {
            "id": "delete_template_button",
            "type": "button",
            "label": "🗑️ Eliminar Plantilla",
            "value": "Eliminar",
            "info": "Eliminar la plantilla seleccionada"
        }
        controls.append(delete_button)
        
        # Información de plantillas
        info_control = {
            "id": "template_info",
            "type": "markdown",
            "label": "Información de Plantillas",
            "value": "💡 **Sistema de Plantillas**: Guarda y carga configuraciones personalizadas.",
            "info": "Información sobre el sistema de plantillas"
        }
        controls.append(info_control)
        
        return controls
    
    def _create_template_editor(self, config: TemplateControlConfig) -> List[Dict[str, Any]]:
        """Crea editor de plantillas"""
        controls = []
        
        # Control de parámetros de plantilla
        parameters_control = {
            "id": "template_parameters_control",
            "type": "json",
            "label": "⚙️ Parámetros de Plantilla",
            "value": json.dumps(config.parameters, indent=2),
            "info": "Parámetros de la plantilla en formato JSON"
        }
        controls.append(parameters_control)
        
        # Botón de guardar plantilla
        save_button = {
            "id": "save_template_button",
            "type": "button",
            "label": "💾 Guardar Plantilla",
            "value": "Guardar",
            "info": "Guardar la plantilla actual"
        }
        controls.append(save_button)
        
        # Botón de crear nueva plantilla
        new_button = {
            "id": "new_template_button",
            "type": "button",
            "label": "➕ Nueva Plantilla",
            "value": "Nueva",
            "info": "Crear una nueva plantilla"
        }
        controls.append(new_button)
        
        # Botón de duplicar plantilla
        duplicate_button = {
            "id": "duplicate_template_button",
            "type": "button",
            "label": "📋 Duplicar Plantilla",
            "value": "Duplicar",
            "info": "Duplicar la plantilla actual"
        }
        controls.append(duplicate_button)
        
        return controls
    
    def _get_available_templates(self) -> List[str]:
        """Obtiene plantillas disponibles"""
        try:
            templates_dir = Path("templates")
            if not templates_dir.exists():
                return ["Nueva Plantilla"]
            
            template_files = list(templates_dir.glob("*.json"))
            templates = ["Nueva Plantilla"]
            
            for template_file in template_files:
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        if "name" in template_data:
                            templates.append(template_data["name"])
                except Exception as e:
                    self.logger.warning(f"Error cargando plantilla {template_file}: {e}")
            
            return templates
            
        except Exception as e:
            self.logger.error(f"Error obteniendo plantillas disponibles: {e}")
            return ["Nueva Plantilla"]
    
    def _register_template_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles de plantillas en el controlador de UI"""
        try:
            if self.ui_controller:
                for control in controls:
                    component_config = {
                        "id": control["id"],
                        "type": control["type"],
                        "label": control["label"],
                        "value": control.get("value"),
                        "info": control.get("info"),
                        "required": control.get("required", False),
                        "validation_rules": control.get("validation_rules", [])
                    }
                    self.ui_controller.create_ui_components([component_config])
        except Exception as e:
            self.logger.error(f"Error registrando controles de plantillas: {e}")
    
    def _register_template_selector(self, controls: List[Dict[str, Any]]):
        """Registra selector de plantillas en el controlador de UI"""
        try:
            if self.ui_controller:
                for control in controls:
                    component_config = {
                        "id": control["id"],
                        "type": control["type"],
                        "label": control["label"],
                        "value": control.get("value"),
                        "info": control.get("info"),
                        "required": control.get("required", False),
                        "validation_rules": control.get("validation_rules", [])
                    }
                    self.ui_controller.create_ui_components([component_config])
        except Exception as e:
            self.logger.error(f"Error registrando selector de plantillas: {e}")
    
    def _register_template_editor(self, controls: List[Dict[str, Any]]):
        """Registra editor de plantillas en el controlador de UI"""
        try:
            if self.ui_controller:
                for control in controls:
                    component_config = {
                        "id": control["id"],
                        "type": control["type"],
                        "label": control["label"],
                        "value": control.get("value"),
                        "info": control.get("info"),
                        "required": control.get("required", False),
                        "validation_rules": control.get("validation_rules", [])
                    }
                    self.ui_controller.create_ui_components([component_config])
        except Exception as e:
            self.logger.error(f"Error registrando editor de plantillas: {e}")
    
    def save_template(self, config: TemplateControlConfig) -> bool:
        """Guarda una plantilla"""
        try:
            template_data = {
                "name": config.template_name,
                "type": config.template_type,
                "description": config.description,
                "parameters": config.parameters,
                "is_default": config.is_default,
                "created_date": config.created_date,
                "modified_date": config.modified_date
            }
            
            # Crear directorio de plantillas si no existe
            templates_dir = Path("templates")
            templates_dir.mkdir(exist_ok=True)
            
            # Guardar plantilla
            template_file = templates_dir / f"{config.template_name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Plantilla guardada en {template_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando plantilla: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "saving template"})
            return False
    
    def load_template(self, template_name: str) -> Optional[TemplateControlConfig]:
        """Carga una plantilla"""
        try:
            template_file = Path("templates") / f"{template_name}.json"
            
            if not template_file.exists():
                return None
            
            with open(template_file, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            return TemplateControlConfig(
                template_name=template_data.get("name", template_name),
                template_type=template_data.get("type", "genetic"),
                description=template_data.get("description", ""),
                parameters=template_data.get("parameters", {}),
                is_default=template_data.get("is_default", False),
                created_date=template_data.get("created_date", ""),
                modified_date=template_data.get("modified_date", "")
            )
            
        except Exception as e:
            self.logger.error(f"Error cargando plantilla {template_name}: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "loading template"})
            return None
    
    def delete_template(self, template_name: str) -> bool:
        """Elimina una plantilla"""
        try:
            template_file = Path("templates") / f"{template_name}.json"
            
            if template_file.exists():
                template_file.unlink()
                self.logger.info(f"Plantilla {template_name} eliminada")
                return True
            else:
                self.logger.warning(f"Plantilla {template_name} no encontrada")
                return False
                
        except Exception as e:
            self.logger.error(f"Error eliminando plantilla {template_name}: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "deleting template"})
            return False

# Instancia global
_template_controls_instance: Optional[TemplateControls] = None

def get_template_controls() -> TemplateControls:
    """Obtiene la instancia global de TemplateControls"""
    global _template_controls_instance
    if _template_controls_instance is None:
        _template_controls_instance = TemplateControls()
    return _template_controls_instance
