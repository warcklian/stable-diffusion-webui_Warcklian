#!/usr/bin/env python3
"""
Gestor de Errores Modular
Sistema modular para manejo de errores y recuperación
"""

import traceback
import sys
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

class ErrorSeverity(Enum):
    """Severidad del error"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorType(Enum):
    """Tipo de error"""
    GENERATION_ERROR = "generation_error"
    VALIDATION_ERROR = "validation_error"
    FILE_ERROR = "file_error"
    MEMORY_ERROR = "memory_error"
    NETWORK_ERROR = "network_error"
    SYSTEM_ERROR = "system_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class ErrorInfo:
    """Información detallada de un error"""
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    details: str = ""
    timestamp: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    stack_trace: str = ""
    recovery_suggestions: List[str] = field(default_factory=list)
    is_recoverable: bool = True

@dataclass
class ErrorRecoveryResult:
    """Resultado de recuperación de error"""
    success: bool
    recovered_data: Any = None
    error_message: str = ""
    recovery_time: float = 0.0
    actions_taken: List[str] = field(default_factory=list)

class ErrorHandler:
    """Gestor de errores para generación de imágenes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history: List[ErrorInfo] = []
        self.recovery_strategies = self._initialize_recovery_strategies()
        
    def handle_generation_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
        """
        Maneja errores de generación
        
        Args:
            error: Excepción capturada
            context: Contexto adicional del error
            
        Returns:
            ErrorInfo: Información detallada del error
        """
        try:
            # Determinar tipo y severidad del error
            error_type, severity = self._classify_error(error)
            
            # Crear información del error
            error_info = ErrorInfo(
                error_type=error_type,
                severity=severity,
                message=str(error),
                details=self._extract_error_details(error),
                timestamp=datetime.now().isoformat(),
                context=context or {},
                stack_trace=traceback.format_exc(),
                recovery_suggestions=self._get_recovery_suggestions(error_type, severity),
                is_recoverable=self._is_recoverable(error_type, severity)
            )
            
            # Loggear el error
            self._log_error(error_info)
            
            # Agregar al historial
            self.error_history.append(error_info)
            
            # Intentar recuperación automática si es posible
            if error_info.is_recoverable:
                recovery_result = self._attempt_automatic_recovery(error_info)
                if recovery_result.success:
                    error_info.recovery_suggestions.append("Recuperación automática exitosa")
                    self.logger.info(f"Recuperación automática exitosa para error: {error_info.message}")
                else:
                    error_info.recovery_suggestions.append(f"Recuperación automática falló: {recovery_result.error_message}")
            
            return error_info
            
        except Exception as e:
            # Error en el manejo de errores
            self.logger.critical(f"Error crítico en ErrorHandler: {e}")
            return ErrorInfo(
                error_type=ErrorType.SYSTEM_ERROR,
                severity=ErrorSeverity.CRITICAL,
                message=f"Error en ErrorHandler: {str(e)}",
                timestamp=datetime.now().isoformat(),
                is_recoverable=False
            )
    
    def log_error(self, error_info: ErrorInfo, additional_context: Dict[str, Any] = None) -> None:
        """
        Loggea un error con información detallada
        
        Args:
            error_info: Información del error
            additional_context: Contexto adicional
        """
        try:
            # Combinar contextos
            full_context = {**error_info.context, **(additional_context or {})}
            
            # Formatear mensaje de log
            log_message = self._format_log_message(error_info, full_context)
            
            # Loggear según severidad
            if error_info.severity == ErrorSeverity.CRITICAL:
                self.logger.critical(log_message)
            elif error_info.severity == ErrorSeverity.HIGH:
                self.logger.error(log_message)
            elif error_info.severity == ErrorSeverity.MEDIUM:
                self.logger.warning(log_message)
            else:
                self.logger.info(log_message)
            
            # Loggear stack trace si es crítico o alto
            if error_info.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
                self.logger.debug(f"Stack trace: {error_info.stack_trace}")
            
        except Exception as e:
            self.logger.critical(f"Error loggeando error: {e}")
    
    def format_error_message(self, error_info: ErrorInfo, user_friendly: bool = True) -> str:
        """
        Formatea un mensaje de error para el usuario
        
        Args:
            error_info: Información del error
            user_friendly: Si usar formato amigable al usuario
            
        Returns:
            str: Mensaje de error formateado
        """
        try:
            if user_friendly:
                return self._format_user_friendly_message(error_info)
            else:
                return self._format_technical_message(error_info)
        except Exception as e:
            return f"Error formateando mensaje: {str(e)}"
    
    def recover_from_error(self, error_info: ErrorInfo, recovery_data: Any = None) -> ErrorRecoveryResult:
        """
        Intenta recuperar de un error
        
        Args:
            error_info: Información del error
            recovery_data: Datos para recuperación
            
        Returns:
            ErrorRecoveryResult: Resultado de la recuperación
        """
        start_time = time.time()
        
        try:
            if not error_info.is_recoverable:
                return ErrorRecoveryResult(
                    success=False,
                    error_message="Error no es recuperable",
                    recovery_time=time.time() - start_time
                )
            
            # Obtener estrategia de recuperación
            strategy = self.recovery_strategies.get(error_info.error_type)
            if not strategy:
                return ErrorRecoveryResult(
                    success=False,
                    error_message=f"No hay estrategia de recuperación para {error_info.error_type.value}",
                    recovery_time=time.time() - start_time
                )
            
            # Ejecutar estrategia de recuperación
            result = strategy(error_info, recovery_data)
            
            recovery_time = time.time() - start_time
            
            return ErrorRecoveryResult(
                success=result.get("success", False),
                recovered_data=result.get("data"),
                error_message=result.get("error_message", ""),
                recovery_time=recovery_time,
                actions_taken=result.get("actions", [])
            )
            
        except Exception as e:
            self.logger.error(f"Error en recuperación: {e}")
            return ErrorRecoveryResult(
                success=False,
                error_message=f"Error en recuperación: {str(e)}",
                recovery_time=time.time() - start_time
            )
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de errores"""
        try:
            if not self.error_history:
                return {"total_errors": 0, "message": "No hay errores registrados"}
            
            # Contar por tipo
            error_types = {}
            error_severities = {}
            
            for error in self.error_history:
                error_type = error.error_type.value
                severity = error.severity.value
                
                error_types[error_type] = error_types.get(error_type, 0) + 1
                error_severities[severity] = error_severities.get(severity, 0) + 1
            
            # Errores recientes (últimas 24 horas)
            recent_errors = [
                error for error in self.error_history
                if (datetime.now() - datetime.fromisoformat(error.timestamp)).total_seconds() < 86400
            ]
            
            return {
                "total_errors": len(self.error_history),
                "recent_errors": len(recent_errors),
                "error_types": error_types,
                "error_severities": error_severities,
                "recoverable_errors": len([e for e in self.error_history if e.is_recoverable]),
                "critical_errors": len([e for e in self.error_history if e.severity == ErrorSeverity.CRITICAL])
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
    
    def clear_error_history(self) -> None:
        """Limpia el historial de errores"""
        self.error_history.clear()
        self.logger.info("Historial de errores limpiado")
    
    def _classify_error(self, error: Exception) -> Tuple[ErrorType, ErrorSeverity]:
        """Clasifica un error por tipo y severidad"""
        error_str = str(error).lower()
        
        # Clasificar por tipo
        if "generation" in error_str or "model" in error_str:
            error_type = ErrorType.GENERATION_ERROR
        elif "validation" in error_str or "invalid" in error_str:
            error_type = ErrorType.VALIDATION_ERROR
        elif "file" in error_str or "path" in error_str or "directory" in error_str:
            error_type = ErrorType.FILE_ERROR
        elif "memory" in error_str or "out of memory" in error_str:
            error_type = ErrorType.MEMORY_ERROR
        elif "network" in error_str or "connection" in error_str:
            error_type = ErrorType.NETWORK_ERROR
        elif "system" in error_str or "os" in error_str:
            error_type = ErrorType.SYSTEM_ERROR
        else:
            error_type = ErrorType.UNKNOWN_ERROR
        
        # Clasificar por severidad
        if isinstance(error, (MemoryError, OSError, SystemError)):
            severity = ErrorSeverity.CRITICAL
        elif "critical" in error_str or "fatal" in error_str:
            severity = ErrorSeverity.CRITICAL
        elif "error" in error_str or "failed" in error_str:
            severity = ErrorSeverity.HIGH
        elif "warning" in error_str or "caution" in error_str:
            severity = ErrorSeverity.MEDIUM
        else:
            severity = ErrorSeverity.LOW
        
        return error_type, severity
    
    def _extract_error_details(self, error: Exception) -> str:
        """Extrae detalles específicos del error"""
        try:
            if hasattr(error, 'args') and error.args:
                return f"Args: {error.args}"
            elif hasattr(error, 'errno'):
                return f"Errno: {error.errno}"
            else:
                return f"Type: {type(error).__name__}"
        except:
            return "No se pudieron extraer detalles"
    
    def _get_recovery_suggestions(self, error_type: ErrorType, severity: ErrorSeverity) -> List[str]:
        """Obtiene sugerencias de recuperación"""
        suggestions = []
        
        if error_type == ErrorType.MEMORY_ERROR:
            suggestions.extend([
                "Reducir el tamaño del lote",
                "Limpiar memoria del sistema",
                "Cerrar otras aplicaciones",
                "Reiniciar el generador"
            ])
        elif error_type == ErrorType.FILE_ERROR:
            suggestions.extend([
                "Verificar permisos de archivo",
                "Verificar espacio en disco",
                "Crear directorio manualmente",
                "Verificar ruta del archivo"
            ])
        elif error_type == ErrorType.VALIDATION_ERROR:
            suggestions.extend([
                "Verificar parámetros de entrada",
                "Usar valores por defecto",
                "Validar formato de datos",
                "Revisar configuración"
            ])
        elif error_type == ErrorType.GENERATION_ERROR:
            suggestions.extend([
                "Verificar modelo cargado",
                "Verificar configuración de generación",
                "Reiniciar el proceso de generación",
                "Verificar recursos del sistema"
            ])
        
        if severity == ErrorSeverity.CRITICAL:
            suggestions.append("Contactar soporte técnico")
        
        return suggestions
    
    def _is_recoverable(self, error_type: ErrorType, severity: ErrorSeverity) -> bool:
        """Determina si un error es recuperable"""
        if severity == ErrorSeverity.CRITICAL:
            return False
        elif error_type == ErrorType.SYSTEM_ERROR:
            return False
        else:
            return True
    
    def _log_error(self, error_info: ErrorInfo) -> None:
        """Loggea un error"""
        self.log_error(error_info)
    
    def _format_log_message(self, error_info: ErrorInfo, context: Dict[str, Any]) -> str:
        """Formatea mensaje de log"""
        return f"[{error_info.severity.value.upper()}] {error_info.error_type.value}: {error_info.message}"
    
    def _format_user_friendly_message(self, error_info: ErrorInfo) -> str:
        """Formatea mensaje amigable al usuario"""
        if error_info.severity == ErrorSeverity.CRITICAL:
            return f"🚨 Error crítico: {error_info.message}"
        elif error_info.severity == ErrorSeverity.HIGH:
            return f"❌ Error: {error_info.message}"
        elif error_info.severity == ErrorSeverity.MEDIUM:
            return f"⚠️ Advertencia: {error_info.message}"
        else:
            return f"ℹ️ Información: {error_info.message}"
    
    def _format_technical_message(self, error_info: ErrorInfo) -> str:
        """Formatea mensaje técnico"""
        return f"[{error_info.timestamp}] {error_info.severity.value.upper()} - {error_info.error_type.value}: {error_info.message}"
    
    def _attempt_automatic_recovery(self, error_info: ErrorInfo) -> ErrorRecoveryResult:
        """Intenta recuperación automática"""
        try:
            if error_info.error_type == ErrorType.MEMORY_ERROR:
                return self._recover_memory_error(error_info)
            elif error_info.error_type == ErrorType.FILE_ERROR:
                return self._recover_file_error(error_info)
            elif error_info.error_type == ErrorType.VALIDATION_ERROR:
                return self._recover_validation_error(error_info)
            else:
                return ErrorRecoveryResult(success=False, error_message="No hay recuperación automática disponible")
        except Exception as e:
            return ErrorRecoveryResult(success=False, error_message=f"Error en recuperación automática: {str(e)}")
    
    def _recover_memory_error(self, error_info: ErrorInfo) -> ErrorRecoveryResult:
        """Recupera errores de memoria"""
        try:
            # Limpiar memoria si está disponible
            if OPTIMIZATION_MODULES_AVAILABLE:
                from modules.memory_optimizer import get_memory_optimizer
                memory_optimizer = get_memory_optimizer()
                memory_optimizer.cleanup_memory(force=True)
                return ErrorRecoveryResult(success=True, actions_taken=["Limpieza de memoria"])
            else:
                return ErrorRecoveryResult(success=False, error_message="Módulo de optimización de memoria no disponible")
        except Exception as e:
            return ErrorRecoveryResult(success=False, error_message=f"Error en recuperación de memoria: {str(e)}")
    
    def _recover_file_error(self, error_info: ErrorInfo) -> ErrorRecoveryResult:
        """Recupera errores de archivo"""
        try:
            # Crear directorios si no existen
            if "path" in error_info.context:
                path = error_info.context["path"]
                from pathlib import Path
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                return ErrorRecoveryResult(success=True, actions_taken=["Directorio creado"])
            else:
                return ErrorRecoveryResult(success=False, error_message="No hay información de ruta para recuperar")
        except Exception as e:
            return ErrorRecoveryResult(success=False, error_message=f"Error en recuperación de archivo: {str(e)}")
    
    def _recover_validation_error(self, error_info: ErrorInfo) -> ErrorRecoveryResult:
        """Recupera errores de validación"""
        try:
            # Usar valores por defecto si están disponibles
            if "default_values" in error_info.context:
                return ErrorRecoveryResult(
                    success=True, 
                    recovered_data=error_info.context["default_values"],
                    actions_taken=["Valores por defecto aplicados"]
                )
            else:
                return ErrorRecoveryResult(success=False, error_message="No hay valores por defecto disponibles")
        except Exception as e:
            return ErrorRecoveryResult(success=False, error_message=f"Error en recuperación de validación: {str(e)}")
    
    def _initialize_recovery_strategies(self) -> Dict[ErrorType, callable]:
        """Inicializa estrategias de recuperación"""
        return {
            ErrorType.MEMORY_ERROR: self._recover_memory_error,
            ErrorType.FILE_ERROR: self._recover_file_error,
            ErrorType.VALIDATION_ERROR: self._recover_validation_error,
        }

# Instancia global del gestor de errores
error_handler = ErrorHandler()

def get_error_handler() -> ErrorHandler:
    """Obtiene la instancia global del gestor de errores"""
    return error_handler

def handle_error(error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
    """Función de conveniencia para manejar errores"""
    return error_handler.handle_generation_error(error, context)
