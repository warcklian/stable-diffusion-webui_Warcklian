#!/usr/bin/env python3
"""
Generador Genético Modular
Sistema modular para generación de imágenes con motor genético dinámico
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
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType, get_genetic_controls, GeneticControlConfig
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
class GenerationParams:
    """Parámetros de generación genética"""
    nacionalidad: str
    genero: str
    edad: int
    cantidad: int
    region: str
    edad_min: int
    edad_max: int
    beauty_control: str
    skin_control: str
    hair_control: str
    eye_control: str
    background_control: str
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
class GenerationResult:
    """Resultado de generación genética"""
    success: bool
    images_generated: int
    failed_count: int
    output_directory: str
    error_message: str = ""
    generation_time: float = 0.0

class GeneticGenerator:
    """Generador de imágenes con motor genético dinámico"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.generation_cancelled = False
        
    def generate_batch(self, params: GenerationParams, progress_callback=None) -> GenerationResult:
        """
        Genera un lote de imágenes genéticas
        
        Args:
            params: Parámetros de generación
            progress_callback: Callback para actualizar progreso
            
        Returns:
            GenerationResult: Resultado de la generación
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
            progress_manager.create_progress_ui(int(params.cantidad), f"Iniciando generación genética de {params.cantidad} imágenes...")
            
            # Configurar gestor de archivos
            file_manager = get_file_manager()
            
            # Configurar gestor de errores
            error_handler = get_error_handler()
            
            # Configurar controlador de UI
            ui_controller = get_ui_controller()
            
            # Configurar controles genéticos
            genetic_controls = get_genetic_controls()
            
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
                return GenerationResult(
                    success=False,
                    images_generated=0,
                    failed_count=0,
                    output_directory="",
                    error_message=validation_result["error"]
                )
            
            # 2. Optimización de memoria
            if OPTIMIZATION_MODULES_AVAILABLE:
                self._optimize_memory(params)
            
            # 3. Configurar directorios
            output_dir = self._setup_directories(params)
            
            # 4. Generar imágenes
            result = self._process_images(params, output_dir, progress_callback, progress_manager, file_manager, error_handler, ui_controller)
            
            # 5. Calcular tiempo total
            generation_time = time.time() - start_time
            result.generation_time = generation_time
            
            # 6. Completar progreso
            if progress_manager:
                progress_manager.update_progress(int(params.cantidad), "Generación genética completada", force_update=True)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error en generación genética: {e}")
            if progress_manager:
                progress_manager.handle_cancellation()
            
            # Manejar error con ErrorHandler si está disponible
            if error_handler:
                error_info = error_handler.handle_generation_error(e, {
                    "generation_type": "genetic",
                    "params": params.__dict__,
                    "output_dir": str(output_dir) if 'output_dir' in locals() else "unknown"
                })
                error_message = error_handler.format_error_message(error_info, user_friendly=True)
            else:
                error_message = f"Error crítico: {str(e)}"
            
            return GenerationResult(
                success=False,
                images_generated=0,
                failed_count=0,
                output_directory="",
                error_message=error_message
            )
    
    def _validate_parameters(self, params: GenerationParams) -> Dict[str, Any]:
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
                    is_saime=False  # Generación genética no es SAIME
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
            
            # Validar dimensiones
            if params.width <= 0 or params.height <= 0:
                return {
                    "valid": False,
                    "error": f"❌ Error: Las dimensiones deben ser mayores que 0"
                }
            
            return {"valid": True}
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"❌ Error de validación: {str(e)}"
            }
    
    def _optimize_memory(self, params: GenerationParams) -> None:
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
    
    def _setup_directories(self, params: GenerationParams) -> Path:
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
            
            # Crear directorio para generación genética
            batch_dir = output_dir / model_name_clean / "genetico_premium" / f"genetic_{params.nacionalidad}_{params.region}_{params.genero}_{timestamp}"
            batch_dir.mkdir(parents=True, exist_ok=True)
            
            return batch_dir
            
        except Exception as e:
            self.logger.error(f"Error configurando directorios: {e}")
            # Fallback a directorio por defecto
            return Path("outputs/genetic_generation")
    
    def _generate_genetic_profile(self, params: GenerationParams, image_index: int) -> Dict[str, Any]:
        """Genera perfil genético único para una imagen"""
        try:
            # Importar motor genético avanzado
            from modules.ui import AdvancedGeneticDiversityEngine
            
            genetic_engine = AdvancedGeneticDiversityEngine()
            
            # Generar edad aleatoria dentro del rango
            edad_aleatoria = random.randint(params.edad_min, params.edad_max)
            
            # Usar región aleatoria para máxima diversidad
            regiones_disponibles = [
                "caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", 
                "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz",
                "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua",
                "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas",
                "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua",
                "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique",
                "araure", "turen", "guanarito", "santa_elena", "el_venado",
                "san_rafael", "san_antonio", "la_fria", "rubio", "colon",
                "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro",
                "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui",
                "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida",
                "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda",
                "vargas", "distrito_capital"
            ]
            region_genetica = random.choice(regiones_disponibles)
            
            # Generar perfil genético avanzado
            genetic_profile = genetic_engine.generate_advanced_genetic_profile(
                nationality=params.nacionalidad,
                region=region_genetica,
                gender=params.genero,
                age=edad_aleatoria,
                beauty_control=params.beauty_control,
                skin_control=params.skin_control,
                hair_control=params.hair_control,
                eye_control=params.eye_control
            )
            
            return {
                "profile": genetic_profile,
                "region": region_genetica,
                "age": edad_aleatoria
            }
            
        except Exception as e:
            self.logger.error(f"Error generando perfil genético: {e}")
            # Fallback a perfil básico
            return {
                "profile": None,
                "region": params.region,
                "age": random.randint(params.edad_min, params.edad_max)
            }
    
    def _process_images(self, params: GenerationParams, output_dir: Path, progress_callback=None, progress_manager=None, file_manager=None, error_handler=None, ui_controller=None) -> GenerationResult:
        """Procesa las imágenes del lote"""
        images_generated = 0
        failed_count = 0
        
        try:
            cantidad_int = int(params.cantidad)
            
            for i in range(cantidad_int):
                # Verificar si la generación fue cancelada
                if self.generation_cancelled:
                    return GenerationResult(
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
                    progress_callback((i + 1) / cantidad_int, f"Generando imagen {i+1}/{cantidad_int} con perfil genético único...")
                
                # Actualizar gestor de progreso
                if progress_manager:
                    progress_manager.update_progress(i + 1, f"Generando imagen {i+1}/{cantidad_int} con perfil genético único...")
                
                # Generar perfil genético
                genetic_data = self._generate_genetic_profile(params, i)
                
                # Procesar imagen individual
                success = self._process_single_image(params, genetic_data, output_dir, i)
                
                if success:
                    images_generated += 1
                else:
                    failed_count += 1
            
            return GenerationResult(
                success=True,
                images_generated=images_generated,
                failed_count=failed_count,
                output_directory=str(output_dir)
            )
            
        except Exception as e:
            self.logger.error(f"Error procesando imágenes: {e}")
            return GenerationResult(
                success=False,
                images_generated=images_generated,
                failed_count=failed_count,
                output_directory=str(output_dir),
                error_message=f"Error procesando imágenes: {str(e)}"
            )
    
    def _process_single_image(self, params: GenerationParams, genetic_data: Dict[str, Any], output_dir: Path, image_index: int) -> bool:
        """Procesa una imagen individual"""
        try:
            # TODO: Implementar procesamiento de imagen individual
            # Esta es la parte más compleja que necesita ser extraída de la función original
            # Por ahora, retornar True para mantener compatibilidad
            return True
            
        except Exception as e:
            self.logger.error(f"Error procesando imagen {image_index}: {e}")
            return False
    
    def cancel_generation(self) -> None:
        """Cancela la generación en curso"""
        self.generation_cancelled = True
        self.logger.info("Generación cancelada por el usuario")

# Instancia global del generador
genetic_generator = GeneticGenerator()

def get_genetic_generator() -> GeneticGenerator:
    """Obtiene la instancia global del generador genético"""
    return genetic_generator
