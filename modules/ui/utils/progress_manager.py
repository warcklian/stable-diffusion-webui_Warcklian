#!/usr/bin/env python3
"""
Gestor de Progreso Modular
Sistema modular para gestión de progreso y cancelación de generación
"""

import time
import threading
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
import logging

@dataclass
class ProgressStats:
    """Estadísticas de progreso"""
    current_step: int = 0
    total_steps: int = 0
    percentage: float = 0.0
    current_description: str = ""
    start_time: float = 0.0
    elapsed_time: float = 0.0
    estimated_remaining: float = 0.0
    is_cancelled: bool = False
    is_completed: bool = False

@dataclass
class ProgressConfig:
    """Configuración de progreso"""
    update_interval: float = 0.1  # segundos
    show_detailed_progress: bool = True
    show_time_estimates: bool = True
    show_percentage: bool = True
    auto_cancel_timeout: float = 0.0  # 0 = sin timeout

class ProgressManager:
    """Gestor de progreso para generación de imágenes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stats = ProgressStats()
        self.config = ProgressConfig()
        self.callbacks: List[Callable] = []
        self.cancellation_callbacks: List[Callable] = []
        self._lock = threading.Lock()
        self._last_update_time = 0.0
        
    def create_progress_ui(self, total_steps: int, initial_description: str = "Iniciando...") -> None:
        """
        Crea la interfaz de progreso
        
        Args:
            total_steps: Número total de pasos
            initial_description: Descripción inicial
        """
        with self._lock:
            self.stats = ProgressStats(
                current_step=0,
                total_steps=total_steps,
                percentage=0.0,
                current_description=initial_description,
                start_time=time.time(),
                elapsed_time=0.0,
                estimated_remaining=0.0,
                is_cancelled=False,
                is_completed=False
            )
            
        self.logger.info(f"Progreso iniciado: {total_steps} pasos - {initial_description}")
    
    def update_progress(self, step: int, description: str = "", force_update: bool = False) -> bool:
        """
        Actualiza el progreso
        
        Args:
            step: Paso actual (0-based)
            description: Descripción del paso actual
            force_update: Forzar actualización independientemente del intervalo
            
        Returns:
            bool: True si la actualización fue exitosa, False si fue cancelada
        """
        with self._lock:
            # Verificar si fue cancelado
            if self.stats.is_cancelled:
                return False
            
            # Verificar si ya está completado
            if self.stats.is_completed:
                return True
            
            # Verificar intervalo de actualización
            current_time = time.time()
            if not force_update and (current_time - self._last_update_time) < self.config.update_interval:
                return True
            
            # Actualizar estadísticas
            self.stats.current_step = min(step, self.stats.total_steps)
            self.stats.percentage = (self.stats.current_step / self.stats.total_steps) * 100.0
            self.stats.current_description = description or self.stats.current_description
            self.stats.elapsed_time = current_time - self.stats.start_time
            
            # Calcular tiempo estimado restante
            if self.stats.current_step > 0:
                avg_time_per_step = self.stats.elapsed_time / self.stats.current_step
                remaining_steps = self.stats.total_steps - self.stats.current_step
                self.stats.estimated_remaining = avg_time_per_step * remaining_steps
            
            # Verificar si está completado
            if self.stats.current_step >= self.stats.total_steps:
                self.stats.is_completed = True
                self.stats.percentage = 100.0
                self.stats.current_description = "Completado"
            
            self._last_update_time = current_time
            
            # Llamar callbacks
            self._notify_callbacks()
            
            return True
    
    def handle_cancellation(self) -> None:
        """Maneja la cancelación del progreso"""
        with self._lock:
            if not self.stats.is_cancelled:
                self.stats.is_cancelled = True
                self.stats.current_description = "Cancelado por el usuario"
                
                self.logger.info("Progreso cancelado por el usuario")
                
                # Llamar callbacks de cancelación
                self._notify_cancellation_callbacks()
    
    def is_cancelled(self) -> bool:
        """Verifica si el progreso fue cancelado"""
        with self._lock:
            return self.stats.is_cancelled
    
    def is_completed(self) -> bool:
        """Verifica si el progreso está completado"""
        with self._lock:
            return self.stats.is_completed
    
    def get_progress_stats(self) -> ProgressStats:
        """Obtiene las estadísticas de progreso"""
        with self._lock:
            return ProgressStats(
                current_step=self.stats.current_step,
                total_steps=self.stats.total_steps,
                percentage=self.stats.percentage,
                current_description=self.stats.current_description,
                start_time=self.stats.start_time,
                elapsed_time=self.stats.elapsed_time,
                estimated_remaining=self.stats.estimated_remaining,
                is_cancelled=self.stats.is_cancelled,
                is_completed=self.stats.is_completed
            )
    
    def get_progress_summary(self) -> str:
        """Obtiene un resumen del progreso"""
        stats = self.get_progress_stats()
        
        if stats.is_cancelled:
            return f"🛑 Cancelado: {stats.current_description}"
        
        if stats.is_completed:
            return f"✅ Completado: {stats.current_description} (Tiempo total: {stats.elapsed_time:.1f}s)"
        
        # Formatear tiempo
        elapsed_str = self._format_time(stats.elapsed_time)
        remaining_str = self._format_time(stats.estimated_remaining)
        
        summary = f"📊 Progreso: {stats.current_step}/{stats.total_steps} ({stats.percentage:.1f}%)"
        summary += f"\n⏱️ Tiempo transcurrido: {elapsed_str}"
        
        if stats.estimated_remaining > 0:
            summary += f"\n⏳ Tiempo estimado restante: {remaining_str}"
        
        summary += f"\n📝 Estado: {stats.current_description}"
        
        return summary
    
    def add_progress_callback(self, callback: Callable[[ProgressStats], None]) -> None:
        """Añade un callback de progreso"""
        self.callbacks.append(callback)
    
    def add_cancellation_callback(self, callback: Callable[[], None]) -> None:
        """Añade un callback de cancelación"""
        self.cancellation_callbacks.append(callback)
    
    def remove_progress_callback(self, callback: Callable[[ProgressStats], None]) -> None:
        """Remueve un callback de progreso"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def remove_cancellation_callback(self, callback: Callable[[], None]) -> None:
        """Remueve un callback de cancelación"""
        if callback in self.cancellation_callbacks:
            self.cancellation_callbacks.remove(callback)
    
    def _notify_callbacks(self) -> None:
        """Notifica a los callbacks de progreso"""
        stats = self.get_progress_stats()
        for callback in self.callbacks:
            try:
                callback(stats)
            except Exception as e:
                self.logger.error(f"Error en callback de progreso: {e}")
    
    def _notify_cancellation_callbacks(self) -> None:
        """Notifica a los callbacks de cancelación"""
        for callback in self.cancellation_callbacks:
            try:
                callback()
            except Exception as e:
                self.logger.error(f"Error en callback de cancelación: {e}")
    
    def _format_time(self, seconds: float) -> str:
        """Formatea el tiempo en formato legible"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def reset(self) -> None:
        """Resetea el gestor de progreso"""
        with self._lock:
            self.stats = ProgressStats()
            self._last_update_time = 0.0
            
        self.logger.info("Gestor de progreso reseteado")
    
    def configure(self, **kwargs) -> None:
        """Configura el gestor de progreso"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                
        self.logger.info(f"Configuración actualizada: {kwargs}")

# Instancia global del gestor de progreso
progress_manager = ProgressManager()

def get_progress_manager() -> ProgressManager:
    """Obtiene la instancia global del gestor de progreso"""
    return progress_manager

def create_progress_callback(progress_manager: ProgressManager) -> Callable[[float, str], None]:
    """
    Crea un callback de progreso compatible con Gradio
    
    Args:
        progress_manager: Instancia del gestor de progreso
        
    Returns:
        Callable: Callback compatible con Gradio
    """
    def progress_callback(progress_value: float, message: str = ""):
        """Callback de progreso para Gradio"""
        try:
            # Convertir valor de progreso (0.0-1.0) a paso
            total_steps = progress_manager.stats.total_steps
            current_step = int(progress_value * total_steps)
            
            # Actualizar progreso
            progress_manager.update_progress(current_step, message, force_update=True)
            
        except Exception as e:
            progress_manager.logger.error(f"Error en callback de progreso: {e}")
    
    return progress_callback
