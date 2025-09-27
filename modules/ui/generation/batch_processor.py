"""
Módulo de Procesamiento de Lotes
Sistema modular para procesamiento de lotes de imágenes
"""

import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
import logging
import json
import os

# Imports de módulos de optimización
try:
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType, UIComponentType
    from modules.ui.validation import get_parameter_validator, GenerationValidationParams
    from modules.ui.utils import get_progress_manager, get_file_manager, get_error_handler
    from modules.ui.generation import GeneticGenerator, PassportGenerator
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

@dataclass
class BatchConfig:
    """Configuración de procesamiento de lotes"""
    batch_size: int = 1
    max_concurrent: int = 1
    retry_attempts: int = 3
    timeout_seconds: int = 300
    memory_optimization: bool = True
    progress_reporting: bool = True
    error_handling: str = "continue"  # continue, stop, retry
    output_format: str = "png"
    quality: int = 95

@dataclass
class BatchItem:
    """Elemento individual del lote"""
    id: str
    type: str  # genetic, passport
    parameters: Dict[str, Any]
    priority: int = 0
    retry_count: int = 0
    status: str = "pending"  # pending, processing, completed, failed, cancelled
    result: Optional[Any] = None
    error_message: str = ""
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""

@dataclass
class BatchResult:
    """Resultado del procesamiento de lotes"""
    success: bool
    total_items: int = 0
    processed_items: int = 0
    failed_items: int = 0
    cancelled_items: int = 0
    processing_time: float = 0.0
    error_message: str = ""
    results: List[BatchItem] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)

class BatchProcessor:
    """Procesador de lotes de imágenes"""
    
    def __init__(self, config: Optional[BatchConfig] = None):
        self.config = config if config else BatchConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ui_controller = None
        self.parameter_validator = None
        self.progress_manager = None
        self.file_manager = None
        self.error_handler = None
        self.genetic_generator = None
        self.passport_generator = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self.ui_controller = get_ui_controller()
            self.parameter_validator = get_parameter_validator()
            self.progress_manager = get_progress_manager()
            self.file_manager = get_file_manager()
            self.error_handler = get_error_handler()
            self.genetic_generator = GeneticGenerator()
            self.passport_generator = PassportGenerator()
        
        self._batch_queue: List[BatchItem] = []
        self._processing_lock = threading.Lock()
        self._is_processing = False
        self._cancelled = False
    
    def process_batch(self, items: List[BatchItem], progress_callback: Optional[Callable] = None) -> BatchResult:
        """Procesa un lote de elementos"""
        start_time = time.time()
        self._cancelled = False
        
        try:
            # Configurar gestor de progreso
            if self.progress_manager and self.config.progress_reporting:
                self.progress_manager.create_progress_ui(len(items), f"Procesando lote de {len(items)} elementos...")
            
            # Procesar elementos
            result = self._process_batch_items(items, progress_callback)
            
            # Calcular tiempo total
            processing_time = time.time() - start_time
            result.processing_time = processing_time
            
            # Completar progreso
            if self.progress_manager:
                self.progress_manager.update_progress(len(items), "Procesamiento de lote completado", force_update=True)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error procesando lote: {e}")
            if self.progress_manager:
                self.progress_manager.handle_cancellation()
            
            # Manejar error con ErrorHandler si está disponible
            if self.error_handler:
                error_info = self.error_handler.handle_generation_error(e, {
                    "generation_type": "batch",
                    "items_count": len(items),
                    "config": self.config.__dict__
                })
                error_message = self.error_handler.format_error_message(error_info, user_friendly=True)
            else:
                error_message = f"Error crítico: {str(e)}"
            
            return BatchResult(
                success=False,
                total_items=len(items),
                error_message=error_message
            )
    
    def handle_batch_events(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja eventos de procesamiento de lotes"""
        try:
            if event_type == "start_batch":
                return self._handle_start_batch(data)
            elif event_type == "cancel_batch":
                return self._handle_cancel_batch(data)
            elif event_type == "pause_batch":
                return self._handle_pause_batch(data)
            elif event_type == "resume_batch":
                return self._handle_resume_batch(data)
            elif event_type == "get_batch_status":
                return self._handle_get_batch_status(data)
            else:
                return {"success": False, "error": f"Evento desconocido: {event_type}"}
                
        except Exception as e:
            self.logger.error(f"Error manejando evento de lote: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "handling batch event", "event_type": event_type})
            return {"success": False, "error": str(e)}
    
    def optimize_batch_performance(self, items: List[BatchItem]) -> Dict[str, Any]:
        """Optimiza el rendimiento del procesamiento de lotes"""
        try:
            # Analizar tipos de elementos
            genetic_count = sum(1 for item in items if item.type == "genetic")
            passport_count = sum(1 for item in items if item.type == "passport")
            
            # Optimizar configuración de lote
            optimized_config = self._optimize_batch_config(genetic_count, passport_count)
            
            # Optimizar memoria si está habilitado
            if self.config.memory_optimization and OPTIMIZATION_MODULES_AVAILABLE:
                self._optimize_memory_usage()
            
            return {
                "success": True,
                "optimized_config": optimized_config,
                "genetic_count": genetic_count,
                "passport_count": passport_count,
                "recommendations": self._get_performance_recommendations(genetic_count, passport_count)
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizando rendimiento de lote: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "optimizing batch performance"})
            return {"success": False, "error": str(e)}
    
    def _process_batch_items(self, items: List[BatchItem], progress_callback: Optional[Callable] = None) -> BatchResult:
        """Procesa los elementos del lote"""
        processed_items = 0
        failed_items = 0
        cancelled_items = 0
        results = []
        
        try:
            total_items = len(items)
            
            for i, item in enumerate(items):
                if self._cancelled:
                    item.status = "cancelled"
                    cancelled_items += 1
                    results.append(item)
                    continue
                
                try:
                    # Procesar elemento individual
                    result = self._process_single_item(item)
                    
                    if result["success"]:
                        item.status = "completed"
                        item.result = result["result"]
                        processed_items += 1
                    else:
                        item.status = "failed"
                        item.error_message = result["error"]
                        failed_items += 1
                    
                    results.append(item)
                    
                    # Actualizar progreso
                    if progress_callback:
                        progress_callback((i + 1) / total_items, f"Procesando elemento {i+1}/{total_items}...")
                    
                    if self.progress_manager:
                        self.progress_manager.update_progress(i + 1, f"Procesando elemento {i+1}/{total_items}...")
                    
                except Exception as e:
                    self.logger.error(f"Error procesando elemento {item.id}: {e}")
                    item.status = "failed"
                    item.error_message = str(e)
                    failed_items += 1
                    results.append(item)
            
            return BatchResult(
                success=failed_items == 0,
                total_items=total_items,
                processed_items=processed_items,
                failed_items=failed_items,
                cancelled_items=cancelled_items,
                results=results,
                statistics=self._calculate_batch_statistics(results)
            )
            
        except Exception as e:
            self.logger.error(f"Error procesando elementos del lote: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "processing batch items"})
            raise
    
    def _process_single_item(self, item: BatchItem) -> Dict[str, Any]:
        """Procesa un elemento individual del lote"""
        try:
            if item.type == "genetic":
                return self._process_genetic_item(item)
            elif item.type == "passport":
                return self._process_passport_item(item)
            else:
                return {"success": False, "error": f"Tipo de elemento no soportado: {item.type}"}
                
        except Exception as e:
            self.logger.error(f"Error procesando elemento {item.id}: {e}")
            return {"success": False, "error": str(e)}
    
    def _process_genetic_item(self, item: BatchItem) -> Dict[str, Any]:
        """Procesa un elemento genético"""
        try:
            if not self.genetic_generator:
                return {"success": False, "error": "GeneticGenerator no disponible"}
            
            # Convertir parámetros a formato de GeneticGenerator
            from modules.ui.generation.genetic_generator import GenerationParams
            
            params = GenerationParams(
                cantidad=1,
                edad_min=item.parameters.get("edad_min", 18),
                edad_max=item.parameters.get("edad_max", 65),
                width=item.parameters.get("width", 512),
                height=item.parameters.get("height", 768),
                nacionalidad=item.parameters.get("nacionalidad", "venezolana"),
                genero=item.parameters.get("genero", "aleatorio"),
                region=item.parameters.get("region", "aleatorio"),
                cfg_scale=item.parameters.get("cfg_scale", 7.0),
                steps=item.parameters.get("steps", 20),
                batch_size=1
            )
            
            # Generar imagen
            result = self.genetic_generator.generate_batch(params)
            
            if result.success:
                return {"success": True, "result": result}
            else:
                return {"success": False, "error": result.error_message}
                
        except Exception as e:
            self.logger.error(f"Error procesando elemento genético {item.id}: {e}")
            return {"success": False, "error": str(e)}
    
    def _process_passport_item(self, item: BatchItem) -> Dict[str, Any]:
        """Procesa un elemento de pasaporte"""
        try:
            if not self.passport_generator:
                return {"success": False, "error": "PassportGenerator no disponible"}
            
            # Convertir parámetros a formato de PassportGenerator
            from modules.ui.generation.passport_generator import PassportParams
            
            params = PassportParams(
                cantidad=1,
                nacionalidad=item.parameters.get("nacionalidad", "venezolana"),
                genero=item.parameters.get("genero", "aleatorio"),
                edad_min=item.parameters.get("edad_min", 18),
                edad_max=item.parameters.get("edad_max", 65),
                region=item.parameters.get("region", "aleatorio"),
                width=item.parameters.get("width", 512),
                height=item.parameters.get("height", 768),
                cfg_scale=item.parameters.get("cfg_scale", 7.0),
                steps=item.parameters.get("steps", 20),
                batch_size=1
            )
            
            # Generar imagen
            result = self.passport_generator.generate_passport_batch(params)
            
            if result.success:
                return {"success": True, "result": result}
            else:
                return {"success": False, "error": result.error_message}
                
        except Exception as e:
            self.logger.error(f"Error procesando elemento de pasaporte {item.id}: {e}")
            return {"success": False, "error": str(e)}
    
    def _optimize_batch_config(self, genetic_count: int, passport_count: int) -> Dict[str, Any]:
        """Optimiza la configuración del lote"""
        total_items = genetic_count + passport_count
        
        # Ajustar batch_size basado en el número de elementos
        if total_items <= 10:
            recommended_batch_size = 1
        elif total_items <= 50:
            recommended_batch_size = 2
        else:
            recommended_batch_size = 4
        
        # Ajustar max_concurrent basado en el tipo de elementos
        if genetic_count > passport_count:
            recommended_concurrent = 2  # Genéticos son más rápidos
        else:
            recommended_concurrent = 1  # Pasaportes requieren más recursos
        
        return {
            "batch_size": recommended_batch_size,
            "max_concurrent": recommended_concurrent,
            "memory_optimization": total_items > 20,
            "progress_reporting": True
        }
    
    def _optimize_memory_usage(self):
        """Optimiza el uso de memoria"""
        try:
            if OPTIMIZATION_MODULES_AVAILABLE:
                from modules.memory_optimizer import get_memory_optimizer
                memory_optimizer = get_memory_optimizer()
                memory_optimizer.cleanup_memory(force=True)
        except Exception as e:
            self.logger.warning(f"Error optimizando memoria: {e}")
    
    def _get_performance_recommendations(self, genetic_count: int, passport_count: int) -> List[str]:
        """Obtiene recomendaciones de rendimiento"""
        recommendations = []
        
        if genetic_count > 100:
            recommendations.append("Considerar procesar elementos genéticos en lotes más pequeños")
        
        if passport_count > 50:
            recommendations.append("Considerar procesar elementos de pasaporte en lotes más pequeños")
        
        if genetic_count + passport_count > 200:
            recommendations.append("Considerar habilitar optimización de memoria")
        
        return recommendations
    
    def _calculate_batch_statistics(self, results: List[BatchItem]) -> Dict[str, Any]:
        """Calcula estadísticas del lote"""
        total = len(results)
        completed = sum(1 for item in results if item.status == "completed")
        failed = sum(1 for item in results if item.status == "failed")
        cancelled = sum(1 for item in results if item.status == "cancelled")
        
        return {
            "total_items": total,
            "completed_items": completed,
            "failed_items": failed,
            "cancelled_items": cancelled,
            "success_rate": (completed / total * 100) if total > 0 else 0,
            "failure_rate": (failed / total * 100) if total > 0 else 0,
            "cancellation_rate": (cancelled / total * 100) if total > 0 else 0
        }
    
    def _handle_start_batch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el evento de inicio de lote"""
        try:
            items = data.get("items", [])
            if not items:
                return {"success": False, "error": "No hay elementos para procesar"}
            
            # Iniciar procesamiento
            self._is_processing = True
            self._cancelled = False
            
            return {"success": True, "message": f"Lote iniciado con {len(items)} elementos"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_cancel_batch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el evento de cancelación de lote"""
        try:
            self._cancelled = True
            self._is_processing = False
            
            return {"success": True, "message": "Lote cancelado"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_pause_batch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el evento de pausa de lote"""
        try:
            self._is_processing = False
            
            return {"success": True, "message": "Lote pausado"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_resume_batch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el evento de reanudación de lote"""
        try:
            self._is_processing = True
            
            return {"success": True, "message": "Lote reanudado"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_get_batch_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el evento de obtención de estado de lote"""
        try:
            return {
                "success": True,
                "is_processing": self._is_processing,
                "is_cancelled": self._cancelled,
                "queue_size": len(self._batch_queue)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Instancia global
_batch_processor_instance: Optional[BatchProcessor] = None

def get_batch_processor() -> BatchProcessor:
    """Obtiene la instancia global de BatchProcessor"""
    global _batch_processor_instance
    if _batch_processor_instance is None:
        _batch_processor_instance = BatchProcessor()
    return _batch_processor_instance
