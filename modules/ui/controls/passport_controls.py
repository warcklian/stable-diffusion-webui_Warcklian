"""
Módulo de Controles de Pasaporte
Sistema modular para controles de generación de pasaportes SAIME
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
class PassportControlConfig:
    """Configuración de controles de pasaporte"""
    nacionalidad: str = "venezolana"
    genero: str = "aleatorio"
    edad_min: int = 18
    edad_max: int = 65
    region: str = "aleatorio"
    width: int = 512
    height: int = 768
    cfg_scale: float = 7.0
    steps: int = 20
    batch_size: int = 1
    sampler: str = "DPM++ 2M Karras"
    scheduler: str = "karras"

@dataclass
class PassportControlResult:
    """Resultado de controles de pasaporte"""
    success: bool
    controls_created: int = 0
    error_message: str = ""
    controls_info: Dict[str, Any] = field(default_factory=dict)

class PassportControls:
    """Controlador de controles de pasaporte"""
    
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
    
    def create_passport_ui(self, config: Optional[PassportControlConfig] = None) -> PassportControlResult:
        """Crea la interfaz de controles de pasaporte"""
        try:
            if config is None:
                config = PassportControlConfig()
            
            # Crear controles de pasaporte
            controls = self._create_passport_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_passport_controls(controls)
            
            return PassportControlResult(
                success=True,
                controls_created=len(controls),
                controls_info={"controls": controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles de pasaporte: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating passport controls"})
            
            return PassportControlResult(
                success=False,
                error_message=f"Error creando controles de pasaporte: {str(e)}"
            )
    
    def create_saime_controls(self, config: Optional[PassportControlConfig] = None) -> PassportControlResult:
        """Crea controles específicos de SAIME"""
        try:
            if config is None:
                config = PassportControlConfig()
            
            # Crear controles SAIME
            saime_controls = self._create_saime_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_saime_controls(saime_controls)
            
            return PassportControlResult(
                success=True,
                controls_created=len(saime_controls),
                controls_info={"saime_controls": saime_controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles SAIME: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating SAIME controls"})
            
            return PassportControlResult(
                success=False,
                error_message=f"Error creando controles SAIME: {str(e)}"
            )
    
    def create_validation_controls(self, config: Optional[PassportControlConfig] = None) -> PassportControlResult:
        """Crea controles de validación SAIME"""
        try:
            if config is None:
                config = PassportControlConfig()
            
            # Crear controles de validación
            validation_controls = self._create_validation_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_validation_controls(validation_controls)
            
            return PassportControlResult(
                success=True,
                controls_created=len(validation_controls),
                controls_info={"validation_controls": validation_controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles de validación: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating validation controls"})
            
            return PassportControlResult(
                success=False,
                error_message=f"Error creando controles de validación: {str(e)}"
            )
    
    def _create_passport_controls(self, config: PassportControlConfig) -> List[Dict[str, Any]]:
        """Crea controles básicos de pasaporte"""
        controls = []
        
        # Control de nacionalidad
        nacionalidad_control = {
            "id": "nacionalidad_control",
            "type": "dropdown",
            "label": "🌍 Nacionalidad",
            "choices": ["venezolana", "colombiana", "peruana", "ecuatoriana", "boliviana", "chilena", "argentina", "brasileña", "mexicana", "española", "italiana", "francesa", "alemana", "inglesa", "estadounidense", "canadiense", "australiana", "japonesa", "china", "coreana", "india", "árabe", "africana", "mixta"],
            "value": config.nacionalidad,
            "info": "Nacionalidad para la generación de pasaportes"
        }
        controls.append(nacionalidad_control)
        
        # Control de género
        genero_control = {
            "id": "genero_control",
            "type": "dropdown",
            "label": "⚥ Género",
            "choices": ["aleatorio", "masculino", "femenino"],
            "value": config.genero,
            "info": "Género para la generación"
        }
        controls.append(genero_control)
        
        # Control de edad mínima
        edad_min_control = {
            "id": "edad_min_control",
            "type": "slider",
            "label": "👶 Edad Mínima",
            "minimum": 18,
            "maximum": 65,
            "value": config.edad_min,
            "info": "Edad mínima para la generación"
        }
        controls.append(edad_min_control)
        
        # Control de edad máxima
        edad_max_control = {
            "id": "edad_max_control",
            "type": "slider",
            "label": "👴 Edad Máxima",
            "minimum": 18,
            "maximum": 65,
            "value": config.edad_max,
            "info": "Edad máxima para la generación"
        }
        controls.append(edad_max_control)
        
        # Control de región
        region_control = {
            "id": "region_control",
            "type": "dropdown",
            "label": "🏙️ Región",
            "choices": ["aleatorio", "caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"],
            "value": config.region,
            "info": "Región específica (aleatorio = automático para máxima diversidad)"
        }
        controls.append(region_control)
        
        return controls
    
    def _create_saime_controls(self, config: PassportControlConfig) -> List[Dict[str, Any]]:
        """Crea controles específicos de SAIME"""
        controls = []
        
        # Control de dimensiones SAIME
        width_control = {
            "id": "width_control",
            "type": "slider",
            "label": "📐 Ancho (SAIME)",
            "minimum": 512,
            "maximum": 512,
            "value": config.width,
            "info": "Ancho fijo para cumplir estándares SAIME (512px)"
        }
        controls.append(width_control)
        
        height_control = {
            "id": "height_control",
            "type": "slider",
            "label": "📏 Alto (SAIME)",
            "minimum": 768,
            "maximum": 768,
            "value": config.height,
            "info": "Alto fijo para cumplir estándares SAIME (768px)"
        }
        controls.append(height_control)
        
        # Control de CFG Scale
        cfg_scale_control = {
            "id": "cfg_scale_control",
            "type": "slider",
            "label": "🎯 CFG Scale",
            "minimum": 1.0,
            "maximum": 20.0,
            "value": config.cfg_scale,
            "info": "Controla qué tan cerca sigue el prompt"
        }
        controls.append(cfg_scale_control)
        
        # Control de pasos
        steps_control = {
            "id": "steps_control",
            "type": "slider",
            "label": "🔄 Pasos",
            "minimum": 1,
            "maximum": 150,
            "value": config.steps,
            "info": "Número de pasos de denoising"
        }
        controls.append(steps_control)
        
        # Control de batch size
        batch_size_control = {
            "id": "batch_size_control",
            "type": "slider",
            "label": "📦 Batch Size",
            "minimum": 1,
            "maximum": 8,
            "value": config.batch_size,
            "info": "Número de imágenes por lote"
        }
        controls.append(batch_size_control)
        
        # Control de sampler
        sampler_control = {
            "id": "sampler_control",
            "type": "dropdown",
            "label": "🎲 Sampler",
            "choices": ["DPM++ 2M Karras", "DPM++ SDE Karras", "Euler a", "Euler", "LMS", "Heun", "DPM2", "DPM2 a", "DPM++ 2S a", "DPM++ 2M", "DPM++ SDE", "DPM++ 2M SDE", "DPM++ 2M SDE Heun", "DPM++ 2M SDE Heun Karras", "DPM++ 2M SDE Heun Exponential", "DPM++ 2M SDE Heun Exponential Karras", "DPM++ 2M SDE Heun Exponential Karras", "DPM++ 2M SDE Heun Exponential Karras", "DPM++ 2M SDE Heun Exponential Karras", "DPM++ 2M SDE Heun Exponential Karras"],
            "value": config.sampler,
            "info": "Algoritmo de muestreo"
        }
        controls.append(sampler_control)
        
        # Control de scheduler
        scheduler_control = {
            "id": "scheduler_control",
            "type": "dropdown",
            "label": "⏰ Scheduler",
            "choices": ["karras", "exponential", "polyexponential", "sigmoid", "cosine", "cosine_restart", "linear", "linear_restart", "polynomial", "polynomial_restart", "logit", "logit_restart", "sqrt", "sqrt_restart", "reciprocal", "reciprocal_restart", "sine", "sine_restart", "cosine_annealing", "cosine_annealing_restart", "polynomial_annealing", "polynomial_annealing_restart", "linear_annealing", "linear_annealing_restart", "exponential_annealing", "exponential_annealing_restart", "sigmoid_annealing", "sigmoid_annealing_restart", "cosine_annealing_warm_restarts", "cosine_annealing_warm_restarts_restart", "polynomial_annealing_warm_restarts", "polynomial_annealing_warm_restarts_restart", "linear_annealing_warm_restarts", "linear_annealing_warm_restarts_restart", "exponential_annealing_warm_restarts", "exponential_annealing_warm_restarts_restart", "sigmoid_annealing_warm_restarts", "sigmoid_annealing_warm_restarts_restart"],
            "value": config.scheduler,
            "info": "Programador de ruido"
        }
        controls.append(scheduler_control)
        
        return controls
    
    def _create_validation_controls(self, config: PassportControlConfig) -> List[Dict[str, Any]]:
        """Crea controles de validación SAIME"""
        controls = []
        
        # Control de validación automática
        auto_validation_control = {
            "id": "auto_validation_control",
            "type": "checkbox",
            "label": "✅ Validación Automática SAIME",
            "value": True,
            "info": "Activa la validación automática de estándares SAIME"
        }
        controls.append(auto_validation_control)
        
        # Control de validación de dimensiones
        dimension_validation_control = {
            "id": "dimension_validation_control",
            "type": "checkbox",
            "label": "📐 Validar Dimensiones",
            "value": True,
            "info": "Valida que las dimensiones cumplan estándares SAIME"
        }
        controls.append(dimension_validation_control)
        
        # Control de validación de fondo
        background_validation_control = {
            "id": "background_validation_control",
            "type": "checkbox",
            "label": "🖼️ Validar Fondo",
            "value": True,
            "info": "Valida que el fondo sea neutro"
        }
        controls.append(background_validation_control)
        
        # Control de validación de expresión
        expression_validation_control = {
            "id": "expression_validation_control",
            "type": "checkbox",
            "label": "😐 Validar Expresión",
            "value": True,
            "info": "Valida que la expresión sea neutra"
        }
        controls.append(expression_validation_control)
        
        # Control de validación de iluminación
        lighting_validation_control = {
            "id": "lighting_validation_control",
            "type": "checkbox",
            "label": "💡 Validar Iluminación",
            "value": True,
            "info": "Valida que la iluminación sea uniforme"
        }
        controls.append(lighting_validation_control)
        
        return controls
    
    def _register_passport_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles de pasaporte en el controlador de UI"""
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
            self.logger.error(f"Error registrando controles de pasaporte: {e}")
    
    def _register_saime_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles SAIME en el controlador de UI"""
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
            self.logger.error(f"Error registrando controles SAIME: {e}")
    
    def _register_validation_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles de validación en el controlador de UI"""
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
            self.logger.error(f"Error registrando controles de validación: {e}")
    
    def save_passport_config(self, config: PassportControlConfig) -> bool:
        """Guarda la configuración de pasaporte"""
        try:
            config_data = {
                "nacionalidad": config.nacionalidad,
                "genero": config.genero,
                "edad_min": config.edad_min,
                "edad_max": config.edad_max,
                "region": config.region,
                "width": config.width,
                "height": config.height,
                "cfg_scale": config.cfg_scale,
                "steps": config.steps,
                "batch_size": config.batch_size,
                "sampler": config.sampler,
                "scheduler": config.scheduler
            }
            
            # Guardar en archivo JSON
            config_path = Path("config/passport_config.json")
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuración de pasaporte guardada en {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración de pasaporte: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "saving passport config"})
            return False
    
    def load_passport_config(self) -> Optional[PassportControlConfig]:
        """Carga la configuración de pasaporte"""
        try:
            config_path = Path("config/passport_config.json")
            
            if not config_path.exists():
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            return PassportControlConfig(**config_data)
            
        except Exception as e:
            self.logger.error(f"Error cargando configuración de pasaporte: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "loading passport config"})
            return None

# Instancia global
_passport_controls_instance: Optional[PassportControls] = None

def get_passport_controls() -> PassportControls:
    """Obtiene la instancia global de PassportControls"""
    global _passport_controls_instance
    if _passport_controls_instance is None:
        _passport_controls_instance = PassportControls()
    return _passport_controls_instance
