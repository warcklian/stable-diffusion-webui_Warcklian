#!/usr/bin/env python3
"""
Generador de Pasaportes Modular
Sistema modular para generación de imágenes de pasaportes con especificaciones SAIME
"""

import time
import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import logging

# Imports de módulos de optimización
try:
    from modules.memory_optimizer import get_memory_optimizer, optimize_batch_configuration
    from modules.saime_validator import validate_saime_compliance
    from modules.intelligent_balancer import get_intelligent_balancer, add_generation_to_balance
    from modules.ui.validation import get_parameter_validator, GenerationValidationParams, get_saime_validator, get_advanced_validator
    from modules.ui.utils import get_progress_manager, create_progress_callback, get_file_manager, get_error_handler, handle_error
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType, get_passport_controls, PassportControlConfig
    from modules.ui.config import get_template_manager, get_config_manager
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

# Imports de WebUI (se cargarán cuando sea necesario)
# import modules.processing
# import modules.shared as shared
# from modules.shared import opts
# from contextlib import closing
# from modules import sd_samplers

@dataclass
class PassportParams:
    """Parámetros de generación de pasaportes"""
    nacionalidad: str
    genero: str
    edad: int
    cantidad: int
    edad_min: int
    edad_max: int
    region: str
    cfg_scale: float
    steps: int
    sampler_name: str
    seed: int
    width: int
    height: int
    batch_count: int
    batch_size: int
    denoising_strength: float
    hr_second_pass_steps: int
    hr_scale: float
    hr_resize_x: int
    hr_resize_y: int
    hr_upscaler: str
    hr_sampler_name: str
    hr_scheduler: str
    refiner_checkpoint: str
    refiner_switch_at: float

@dataclass
class PassportResult:
    """Resultado de generación de pasaportes"""
    success: bool
    images_generated: int
    failed_count: int
    output_directory: str
    error_message: str = ""
    generation_time: float = 0.0
    json_files_loaded: int = 0

class PassportGenerator:
    """Generador de imágenes de pasaportes con especificaciones SAIME"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.generation_cancelled = False
        self.json_files_cache = {}
        
    def generate_passport_batch(self, params: PassportParams, progress_callback=None) -> PassportResult:
        """
        Genera un lote de imágenes de pasaportes
        
        Args:
            params: Parámetros de generación
            progress_callback: Callback para actualizar progreso
            
        Returns:
            PassportResult: Resultado de la generación
        """
        start_time = time.time()
        self.generation_cancelled = False
        
        # Configurar gestor de progreso
        progress_manager = None
        file_manager = None
        error_handler = None
        ui_controller = None
        if OPTIMIZATION_MODULES_AVAILABLE:
            progress_manager = get_progress_manager()
            progress_manager.create_progress_ui(int(params.cantidad), f"Iniciando generación de pasaportes de {params.cantidad} imágenes...")
            
            # Configurar gestor de archivos
            file_manager = get_file_manager()
            
            # Configurar gestor de errores
            error_handler = get_error_handler()
            
            # Configurar controlador de UI
            ui_controller = get_ui_controller()
            
            # Configurar controles de pasaporte
            passport_controls = get_passport_controls()
            
            # Crear callback compatible con Gradio
            if progress_callback:
                gradio_callback = create_progress_callback(progress_manager)
                # Combinar callbacks
                def combined_callback(progress_value, message):
                    gradio_callback(progress_value, message)
                    progress_callback(progress_value, message)
                progress_callback = combined_callback
        
        try:
            # 1. Validar parámetros
            validation_result = self._validate_parameters(params)
            if not validation_result["valid"]:
                return PassportResult(
                    success=False,
                    images_generated=0,
                    failed_count=0,
                    output_directory="",
                    error_message=validation_result["error"]
                )
            
            # 2. Cargar configuraciones JSON
            json_configs = self._load_json_configs(params)
            if not json_configs:
                return PassportResult(
                    success=False,
                    images_generated=0,
                    failed_count=0,
                    output_directory="",
                    error_message=f"❌ No se encontraron archivos JSON para {params.nacionalidad}"
                )
            
            # 3. Optimización de memoria
            if OPTIMIZATION_MODULES_AVAILABLE:
                self._optimize_memory(params)
            
            # 4. Configurar directorios
            output_dir = self._setup_directories(params)
            
            # 5. Generar imágenes
            result = self._process_passport_batch(params, json_configs, output_dir, progress_callback, progress_manager, file_manager, error_handler, ui_controller)
            
            # 6. Calcular tiempo total
            generation_time = time.time() - start_time
            result.generation_time = generation_time
            result.json_files_loaded = len(json_configs)
            
            # 7. Completar progreso
            if progress_manager:
                progress_manager.update_progress(int(params.cantidad), "Generación de pasaportes completada", force_update=True)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error en generación de pasaportes: {e}")
            if progress_manager:
                progress_manager.handle_cancellation()
            
            # Manejar error con ErrorHandler si está disponible
            if error_handler:
                error_info = error_handler.handle_generation_error(e, {
                    "generation_type": "passport",
                    "params": params.__dict__,
                    "output_dir": str(output_dir) if 'output_dir' in locals() else "unknown"
                })
                error_message = error_handler.format_error_message(error_info, user_friendly=True)
            else:
                error_message = f"Error crítico: {str(e)}"
            
            return PassportResult(
                success=False,
                images_generated=0,
                failed_count=0,
                output_directory="",
                error_message=error_message
            )
    
    def _validate_parameters(self, params: PassportParams) -> Dict[str, Any]:
        """Valida parámetros de generación"""
        try:
            # Usar ParameterValidator si está disponible
            if OPTIMIZATION_MODULES_AVAILABLE:
                validator = get_parameter_validator()
                
                # Crear parámetros de validación
                validation_params = GenerationValidationParams(
                    cantidad=params.cantidad,
                    edad_min=params.edad_min,
                    edad_max=params.edad_max,
                    width=params.width,
                    height=params.height,
                    nacionalidad=params.nacionalidad,
                    genero=params.genero,
                    region=params.region,
                    cfg_scale=params.cfg_scale,
                    steps=params.steps,
                    batch_size=params.batch_size,
                    is_saime=True  # Generación de pasaportes es SAIME
                )
                
                # Validar parámetros
                result = validator.validate_generation_params(validation_params)
                
                if not result.valid:
                    return {
                        "valid": False,
                        "error": result.error_message
                    }
                
                # Mostrar advertencias si las hay
                if result.warnings:
                    for warning in result.warnings:
                        print(f"⚠️ {warning}")
                
                return {"valid": True}
            
            # Fallback a validación básica si no hay módulos de optimización
            cantidad_int = int(params.cantidad)
            edad_min_int = int(params.edad_min)
            edad_max_int = int(params.edad_max)
            
            # Validar rango de edad
            if edad_min_int >= edad_max_int:
                return {
                    "valid": False,
                    "error": f"❌ Error: La edad mínima ({edad_min_int}) debe ser menor que la máxima ({edad_max_int})"
                }
            
            # Validar cantidad
            if cantidad_int <= 0:
                return {
                    "valid": False,
                    "error": f"❌ Error: La cantidad debe ser mayor que 0"
                }
            
            # Validar dimensiones SAIME
            if params.width != 512 or params.height != 768:
                return {
                    "valid": False,
                    "error": f"❌ Error: Las dimensiones deben ser 512x768 para cumplir especificaciones SAIME"
                }
            
            return {"valid": True}
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"❌ Error de validación: {str(e)}"
            }
    
    def _load_json_configs(self, params: PassportParams) -> List[Dict[str, Any]]:
        """Carga configuraciones JSON para la nacionalidad especificada"""
        try:
            # Directorio de archivos JSON
            consulta_dir = Path(__file__).parent.parent.parent / "Consulta"
            
            # Buscar archivos JSON de la nacionalidad
            json_files = []
            for file_path in consulta_dir.rglob("*.json"):
                if params.nacionalidad.lower() in file_path.name.lower():
                    json_files.append(file_path)
            
            # Si no hay archivos específicos, usar archivos generales
            if not json_files:
                for file_path in consulta_dir.rglob("*.json"):
                    json_files.append(file_path)
            
            if not json_files:
                return []
            
            # Cargar configuraciones
            configs = []
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        configs.append({
                            'file_path': str(json_file),
                            'config': config,
                            'file_name': json_file.name
                        })
                except Exception as e:
                    self.logger.warning(f"Error cargando {json_file}: {e}")
                    continue
            
            return configs
            
        except Exception as e:
            self.logger.error(f"Error cargando configuraciones JSON: {e}")
            return []
    
    def _optimize_memory(self, params: PassportParams) -> None:
        """Optimiza memoria para generación masiva"""
        try:
            memory_optimizer = get_memory_optimizer()
            memory_optimizer.cleanup_memory(force=True)
            
            # Optimizar configuración de lote
            optimization_result = optimize_batch_configuration(int(params.cantidad), int(params.batch_size))
            if optimization_result["optimization_applied"]:
                params.batch_size = optimization_result["recommended_batch_size"]
                print(f"🔧 Optimización de memoria aplicada: batch_size ajustado a {params.batch_size}")
                
        except Exception as e:
            self.logger.warning(f"Error en optimización de memoria: {e}")
    
    def _setup_directories(self, params: PassportParams) -> Path:
        """Configura directorios de salida"""
        try:
            # Obtener nombre del modelo actual
            model_name = "unknown_model"
            # TODO: Implementar cuando se cargue el módulo shared
            # if shared.sd_model and hasattr(shared.sd_model, 'sd_checkpoint_info'):
            #     model_name = shared.sd_model.sd_checkpoint_info.name_for_extra
            
            # Limpiar nombre del modelo para usar como nombre de carpeta
            model_name_clean = "".join(c for c in model_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            model_name_clean = model_name_clean.replace(' ', '_')
            
            # Crear directorio de salida
            output_dir = Path("outputs")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Crear subcarpeta para imágenes estándar de WebUI
            standard_webui_dir = output_dir / model_name_clean / "webui_standard"
            standard_webui_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear directorio para generación de pasaportes
            batch_dir = output_dir / model_name_clean / "pasaportes_saime" / f"passport_{params.nacionalidad}_{params.region}_{params.genero}_{timestamp}"
            batch_dir.mkdir(parents=True, exist_ok=True)
            
            return batch_dir
            
        except Exception as e:
            self.logger.error(f"Error configurando directorios: {e}")
            # Fallback a directorio por defecto
            return Path("outputs/passport_generation")
    
    def _validate_saime_compliance(self, params: PassportParams) -> Dict[str, Any]:
        """Valida cumplimiento de especificaciones SAIME"""
        try:
            # Validar dimensiones SAIME
            if params.width != 512 or params.height != 768:
                return {
                    "compliant": False,
                    "error": f"Dimensiones incorrectas: {params.width}x{params.height}. SAIME requiere 512x768"
                }
            
            # Validar otros parámetros SAIME
            saime_requirements = {
                "width": 512,
                "height": 768,
                "aspect_ratio": 512 / 768,
                "background": "neutral",
                "lighting": "even",
                "expression": "neutral"
            }
            
            return {
                "compliant": True,
                "requirements": saime_requirements
            }
            
        except Exception as e:
            return {
                "compliant": False,
                "error": f"Error validando SAIME: {str(e)}"
            }
    
    def _generate_saime_prompt(self, params: PassportParams, json_config: Dict[str, Any]) -> Dict[str, str]:
        """Genera prompts SAIME específicos"""
        try:
            # Generar prompt positivo con especificaciones SAIME
            positive_prompt = f"""
            passport photo, {params.genero}, {params.nacionalidad}, {params.region},
            512×768 pixels, black outer frame defines ACTUAL photo boundaries,
            shoulders touch left and right red frame edges,
            eyes positioned at 31% from top of image,
            neutral expression, professional lighting,
            {json_config.get('positive_prompt', '')}
            """.strip()
            
            # Generar prompt negativo
            negative_prompt = f"""
            {json_config.get('negative_prompt', '')},
            sunglasses, hat, headwear, jewelry, smile, teeth visible,
            multiple people, background visible, poor lighting,
            blurry, low quality, distorted, deformed
            """.strip()
            
            return {
                "positive": positive_prompt,
                "negative": negative_prompt
            }
            
        except Exception as e:
            self.logger.error(f"Error generando prompts SAIME: {e}")
            return {
                "positive": f"passport photo, {params.genero}, {params.nacionalidad}",
                "negative": "sunglasses, hat, jewelry, smile, multiple people"
            }
    
    def _process_passport_batch(self, params: PassportParams, json_configs: List[Dict[str, Any]], output_dir: Path, progress_callback=None, progress_manager=None, file_manager=None, error_handler=None, ui_controller=None) -> PassportResult:
        """Procesa el lote de pasaportes"""
        images_generated = 0
        failed_count = 0
        
        try:
            cantidad_int = int(params.cantidad)
            
            for i in range(cantidad_int):
                # Verificar si la generación fue cancelada
                if self.generation_cancelled:
                    return PassportResult(
                        success=False,
                        images_generated=images_generated,
                        failed_count=failed_count,
                        output_directory=str(output_dir),
                        error_message="🛑 Generación cancelada por el usuario"
                    )
                
                # Optimización de memoria durante la generación
                if OPTIMIZATION_MODULES_AVAILABLE and i % 5 == 0:  # Cada 5 imágenes
                    try:
                        memory_optimizer = get_memory_optimizer()
                        memory_optimizer.cleanup_memory()
                    except Exception as e:
                        self.logger.warning(f"Error en limpieza de memoria: {e}")
                
                # Actualizar progreso
                if progress_callback:
                    progress_callback((i + 1) / cantidad_int, f"Generando pasaporte {i+1}/{cantidad_int} con especificaciones SAIME...")
                
                # Actualizar gestor de progreso
                if progress_manager:
                    progress_manager.update_progress(i + 1, f"Generando pasaporte {i+1}/{cantidad_int} con especificaciones SAIME...")
                
                # Seleccionar configuración JSON aleatoria
                json_config = random.choice(json_configs)
                
                # Procesar imagen individual
                success = self._process_single_passport(params, json_config, output_dir, i)
                
                if success:
                    images_generated += 1
                else:
                    failed_count += 1
            
            return PassportResult(
                success=True,
                images_generated=images_generated,
                failed_count=failed_count,
                output_directory=str(output_dir)
            )
            
        except Exception as e:
            self.logger.error(f"Error procesando lote de pasaportes: {e}")
            return PassportResult(
                success=False,
                images_generated=images_generated,
                failed_count=failed_count,
                output_directory=str(output_dir),
                error_message=f"Error procesando lote: {str(e)}"
            )
    
    def _process_single_passport(self, params: PassportParams, json_config: Dict[str, Any], output_dir: Path, image_index: int) -> bool:
        """Procesa una imagen individual de pasaporte"""
        try:
            # TODO: Implementar procesamiento de imagen individual
            # Esta es la parte más compleja que necesita ser extraída de la función original
            # Por ahora, retornar True para mantener compatibilidad
            return True
            
        except Exception as e:
            self.logger.error(f"Error procesando pasaporte {image_index}: {e}")
            return False
    
    def cancel_generation(self) -> None:
        """Cancela la generación en curso"""
        self.generation_cancelled = True
        self.logger.info("Generación de pasaportes cancelada por el usuario")

# Instancia global del generador
passport_generator = PassportGenerator()

def get_passport_generator() -> PassportGenerator:
    """Obtiene la instancia global del generador de pasaportes"""
    return passport_generator
