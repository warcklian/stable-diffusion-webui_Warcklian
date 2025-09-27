#!/usr/bin/env python3
"""
Sistema de Optimización de Memoria para Generación Masiva
Módulo para gestionar eficientemente la memoria durante la generación de múltiples imágenes
"""

import gc
import psutil
import torch
import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager
import time

class MemoryOptimizer:
    """Optimizador de memoria para generación masiva"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memory_threshold = 0.85  # 85% de uso de memoria
        self.cleanup_threshold = 0.75  # 75% para limpieza automática
        self.last_cleanup = 0
        self.cleanup_interval = 30  # segundos entre limpiezas
        
    def get_memory_usage(self) -> Dict[str, float]:
        """Obtiene el uso actual de memoria"""
        try:
            # Memoria del sistema
            system_memory = psutil.virtual_memory()
            system_usage = system_memory.percent / 100.0
            
            # Memoria de GPU si está disponible
            gpu_usage = 0.0
            if torch.cuda.is_available():
                gpu_memory = torch.cuda.memory_allocated()
                gpu_total = torch.cuda.get_device_properties(0).total_memory
                gpu_usage = gpu_memory / gpu_total
            
            return {
                "system_usage": system_usage,
                "gpu_usage": gpu_usage,
                "system_available": system_memory.available,
                "gpu_allocated": gpu_memory if torch.cuda.is_available() else 0,
                "gpu_total": gpu_total if torch.cuda.is_available() else 0
            }
        except Exception as e:
            self.logger.warning(f"Error obteniendo uso de memoria: {e}")
            return {"system_usage": 0.0, "gpu_usage": 0.0, "system_available": 0, "gpu_allocated": 0, "gpu_total": 0}
    
    def should_cleanup(self) -> bool:
        """Determina si se debe realizar limpieza de memoria"""
        memory_info = self.get_memory_usage()
        current_time = time.time()
        
        # Limpieza por umbral de memoria
        if memory_info["system_usage"] > self.cleanup_threshold:
            return True
            
        # Limpieza por intervalo de tiempo
        if current_time - self.last_cleanup > self.cleanup_interval:
            return True
            
        return False
    
    def cleanup_memory(self, force: bool = False) -> Dict[str, Any]:
        """Realiza limpieza de memoria"""
        if not force and not self.should_cleanup():
            return {"cleaned": False, "reason": "No cleanup needed"}
        
        start_time = time.time()
        memory_before = self.get_memory_usage()
        
        try:
            # Limpieza de Python
            gc.collect()
            
            # Limpieza de GPU si está disponible
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
            
            # Limpieza adicional del sistema
            if hasattr(torch, 'cuda'):
                torch.cuda.empty_cache()
            
            self.last_cleanup = time.time()
            
            memory_after = self.get_memory_usage()
            cleanup_time = time.time() - start_time
            
            return {
                "cleaned": True,
                "cleanup_time": cleanup_time,
                "memory_before": memory_before,
                "memory_after": memory_after,
                "system_freed": memory_before["system_usage"] - memory_after["system_usage"],
                "gpu_freed": memory_before["gpu_usage"] - memory_after["gpu_usage"]
            }
            
        except Exception as e:
            self.logger.error(f"Error en limpieza de memoria: {e}")
            return {"cleaned": False, "error": str(e)}
    
    @contextmanager
    def memory_managed_generation(self, batch_size: int = 1):
        """Context manager para generación con gestión de memoria"""
        try:
            # Limpieza inicial
            self.cleanup_memory(force=True)
            
            yield self
            
        finally:
            # Limpieza final
            self.cleanup_memory(force=True)
    
    def optimize_for_batch(self, total_images: int, batch_size: int) -> Dict[str, Any]:
        """Optimiza la configuración para un lote de imágenes"""
        memory_info = self.get_memory_usage()
        
        # Ajustar batch_size basado en memoria disponible
        if memory_info["system_usage"] > 0.8:
            recommended_batch_size = max(1, batch_size // 2)
        elif memory_info["system_usage"] > 0.6:
            recommended_batch_size = max(1, batch_size - 1)
        else:
            recommended_batch_size = batch_size
        
        # Calcular número de iteraciones
        iterations = (total_images + recommended_batch_size - 1) // recommended_batch_size
        
        return {
            "recommended_batch_size": recommended_batch_size,
            "iterations": iterations,
            "memory_usage": memory_info,
            "optimization_applied": recommended_batch_size != batch_size
        }
    
    def monitor_generation(self, current_image: int, total_images: int) -> Optional[Dict[str, Any]]:
        """Monitorea la generación y sugiere optimizaciones"""
        if current_image % 10 == 0:  # Cada 10 imágenes
            memory_info = self.get_memory_usage()
            
            if memory_info["system_usage"] > self.memory_threshold:
                return {
                    "action": "cleanup",
                    "reason": "High memory usage",
                    "memory_usage": memory_info["system_usage"]
                }
        
        return None

# Instancia global del optimizador
memory_optimizer = MemoryOptimizer()

def get_memory_optimizer() -> MemoryOptimizer:
    """Obtiene la instancia global del optimizador de memoria"""
    return memory_optimizer

def cleanup_memory_if_needed() -> bool:
    """Limpia la memoria si es necesario"""
    return memory_optimizer.cleanup_memory()["cleaned"]

def optimize_batch_configuration(total_images: int, batch_size: int) -> Dict[str, Any]:
    """Optimiza la configuración de lote"""
    return memory_optimizer.optimize_for_batch(total_images, batch_size)
