"""
Módulo de Controles Genéticos
Sistema modular para controles de generación genética
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
class GeneticControlConfig:
    """Configuración de controles genéticos"""
    beauty_control: str = "aleatorio"
    skin_control: str = "aleatorio"
    hair_control: str = "aleatorio"
    eye_control: str = "aleatorio"
    background_control: str = "aleatorio"
    region_control: str = "aleatorio"
    edad_min: int = 18
    edad_max: int = 65
    genero: str = "aleatorio"
    nacionalidad: str = "venezolana"

@dataclass
class GeneticControlResult:
    """Resultado de controles genéticos"""
    success: bool
    controls_created: int = 0
    error_message: str = ""
    controls_info: Dict[str, Any] = field(default_factory=dict)

class GeneticControls:
    """Controlador de controles genéticos"""
    
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
    
    def create_genetic_ui(self, config: Optional[GeneticControlConfig] = None) -> GeneticControlResult:
        """Crea la interfaz de controles genéticos"""
        try:
            if config is None:
                config = GeneticControlConfig()
            
            # Crear controles genéticos
            controls = self._create_genetic_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_genetic_controls(controls)
            
            return GeneticControlResult(
                success=True,
                controls_created=len(controls),
                controls_info={"controls": controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles genéticos: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating genetic controls"})
            
            return GeneticControlResult(
                success=False,
                error_message=f"Error creando controles genéticos: {str(e)}"
            )
    
    def create_advanced_controls(self, config: Optional[GeneticControlConfig] = None) -> GeneticControlResult:
        """Crea controles genéticos avanzados"""
        try:
            if config is None:
                config = GeneticControlConfig()
            
            # Crear controles avanzados
            advanced_controls = self._create_advanced_genetic_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_advanced_controls(advanced_controls)
            
            return GeneticControlResult(
                success=True,
                controls_created=len(advanced_controls),
                controls_info={"advanced_controls": advanced_controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles genéticos avanzados: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating advanced genetic controls"})
            
            return GeneticControlResult(
                success=False,
                error_message=f"Error creando controles genéticos avanzados: {str(e)}"
            )
    
    def create_balancing_controls(self, config: Optional[GeneticControlConfig] = None) -> GeneticControlResult:
        """Crea controles de balanceo inteligente"""
        try:
            if config is None:
                config = GeneticControlConfig()
            
            # Crear controles de balanceo
            balancing_controls = self._create_balancing_controls(config)
            
            # Registrar en controlador de UI si está disponible
            if self.ui_controller:
                self._register_balancing_controls(balancing_controls)
            
            return GeneticControlResult(
                success=True,
                controls_created=len(balancing_controls),
                controls_info={"balancing_controls": balancing_controls}
            )
            
        except Exception as e:
            self.logger.error(f"Error creando controles de balanceo: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating balancing controls"})
            
            return GeneticControlResult(
                success=False,
                error_message=f"Error creando controles de balanceo: {str(e)}"
            )
    
    def _create_genetic_controls(self, config: GeneticControlConfig) -> List[Dict[str, Any]]:
        """Crea controles genéticos básicos"""
        controls = []
        
        # Control de belleza
        beauty_control = {
            "id": "beauty_control",
            "type": "dropdown",
            "label": "💎 Nivel de Belleza",
            "choices": ["aleatorio", "muy_bajo", "bajo", "medio", "alto", "muy_alto"],
            "value": config.beauty_control,
            "info": "Controla el nivel de belleza facial"
        }
        controls.append(beauty_control)
        
        # Control de tono de piel
        skin_control = {
            "id": "skin_control",
            "type": "dropdown",
            "label": "🎨 Tono de Piel",
            "choices": ["aleatorio", "muy_claro", "claro", "medio", "oscuro", "muy_oscuro"],
            "value": config.skin_control,
            "info": "Controla el tono de piel"
        }
        controls.append(skin_control)
        
        # Control de color de cabello
        hair_control = {
            "id": "hair_control",
            "type": "dropdown",
            "label": "💇 Color de Cabello",
            "choices": ["aleatorio", "negro", "castaño", "rubio", "pelirrojo", "gris", "blanco"],
            "value": config.hair_control,
            "info": "Controla el color del cabello"
        }
        controls.append(hair_control)
        
        # Control de color de ojos
        eye_control = {
            "id": "eye_control",
            "type": "dropdown",
            "label": "👁️ Color de Ojos",
            "choices": ["aleatorio", "marrón", "azul", "verde", "gris", "negro"],
            "value": config.eye_control,
            "info": "Controla el color de los ojos"
        }
        controls.append(eye_control)
        
        # Control de fondo
        background_control = {
            "id": "background_control",
            "type": "dropdown",
            "label": "🖼️ Fondo",
            "choices": ["aleatorio", "neutro", "blanco", "gris", "azul", "verde"],
            "value": config.background_control,
            "info": "Controla el color del fondo"
        }
        controls.append(background_control)
        
        return controls
    
    def _create_advanced_genetic_controls(self, config: GeneticControlConfig) -> List[Dict[str, Any]]:
        """Crea controles genéticos avanzados"""
        controls = []
        
        # Control de región
        region_control = {
            "id": "region_control",
            "type": "dropdown",
            "label": "🏙️ Región",
            "choices": ["aleatorio", "caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"],
            "value": config.region_control,
            "info": "Región específica (aleatorio = automático para máxima diversidad)"
        }
        controls.append(region_control)
        
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
        
        # Control de nacionalidad
        nacionalidad_control = {
            "id": "nacionalidad_control",
            "type": "dropdown",
            "label": "🌍 Nacionalidad",
            "choices": ["venezolana", "colombiana", "peruana", "ecuatoriana", "boliviana", "chilena", "argentina", "brasileña", "mexicana", "española", "italiana", "francesa", "alemana", "inglesa", "estadounidense", "canadiense", "australiana", "japonesa", "china", "coreana", "india", "árabe", "africana", "mixta"],
            "value": config.nacionalidad,
            "info": "Nacionalidad para la generación"
        }
        controls.append(nacionalidad_control)
        
        return controls
    
    def _create_balancing_controls(self, config: GeneticControlConfig) -> List[Dict[str, Any]]:
        """Crea controles de balanceo inteligente"""
        controls = []
        
        # Control de balanceo automático
        balancing_control = {
            "id": "balancing_control",
            "type": "checkbox",
            "label": "⚖️ Balanceo Automático",
            "value": True,
            "info": "Activa el balanceo automático de características"
        }
        controls.append(balancing_control)
        
        # Control de diversidad
        diversity_control = {
            "id": "diversity_control",
            "type": "slider",
            "label": "🌈 Nivel de Diversidad",
            "minimum": 1,
            "maximum": 10,
            "value": 7,
            "info": "Controla el nivel de diversidad en la generación"
        }
        controls.append(diversity_control)
        
        # Control de repetición
        repetition_control = {
            "id": "repetition_control",
            "type": "slider",
            "label": "🔄 Tolerancia a Repetición",
            "minimum": 1,
            "maximum": 10,
            "value": 3,
            "info": "Controla la tolerancia a características repetidas"
        }
        controls.append(repetition_control)
        
        return controls
    
    def _register_genetic_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles genéticos en el controlador de UI"""
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
            self.logger.error(f"Error registrando controles genéticos: {e}")
    
    def _register_advanced_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles avanzados en el controlador de UI"""
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
            self.logger.error(f"Error registrando controles avanzados: {e}")
    
    def _register_balancing_controls(self, controls: List[Dict[str, Any]]):
        """Registra controles de balanceo en el controlador de UI"""
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
            self.logger.error(f"Error registrando controles de balanceo: {e}")
    
    def save_genetic_config(self, config: GeneticControlConfig) -> bool:
        """Guarda la configuración genética"""
        try:
            config_data = {
                "beauty_control": config.beauty_control,
                "skin_control": config.skin_control,
                "hair_control": config.hair_control,
                "eye_control": config.eye_control,
                "background_control": config.background_control,
                "region_control": config.region_control,
                "edad_min": config.edad_min,
                "edad_max": config.edad_max,
                "genero": config.genero,
                "nacionalidad": config.nacionalidad
            }
            
            # Guardar en archivo JSON
            config_path = Path("config/genetic_config.json")
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuración genética guardada en {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración genética: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "saving genetic config"})
            return False
    
    def load_genetic_config(self) -> Optional[GeneticControlConfig]:
        """Carga la configuración genética"""
        try:
            config_path = Path("config/genetic_config.json")
            
            if not config_path.exists():
                return None
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            return GeneticControlConfig(**config_data)
            
        except Exception as e:
            self.logger.error(f"Error cargando configuración genética: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "loading genetic config"})
            return None

# Instancia global
_genetic_controls_instance: Optional[GeneticControls] = None

def get_genetic_controls() -> GeneticControls:
    """Obtiene la instancia global de GeneticControls"""
    global _genetic_controls_instance
    if _genetic_controls_instance is None:
        _genetic_controls_instance = GeneticControls()
    return _genetic_controls_instance
