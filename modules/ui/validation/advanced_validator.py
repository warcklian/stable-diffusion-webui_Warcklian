"""
Módulo de Validación Avanzada
Sistema modular para validación avanzada de parámetros y configuraciones
"""

import logging
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json
import re

# Imports de módulos de optimización
try:
    from modules.ui.utils import get_error_handler, get_file_manager
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

@dataclass
class AdvancedValidationResult:
    """Resultado de validación avanzada"""
    is_valid: bool
    score: float  # 0.0 a 1.0
    violations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validation_details: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0
    timestamp: str = ""

@dataclass
class AdvancedValidationConfig:
    """Configuración de validación avanzada"""
    strict_mode: bool = True
    auto_correct: bool = False
    validate_prompts: bool = True
    validate_parameters: bool = True
    validate_dimensions: bool = True
    validate_quality: bool = True
    validate_performance: bool = True
    max_prompt_length: int = 1000
    min_prompt_length: int = 10
    max_steps: int = 150
    min_steps: int = 1
    max_cfg_scale: float = 20.0
    min_cfg_scale: float = 1.0
    max_batch_size: int = 10
    min_batch_size: int = 1
    max_width: int = 2048
    min_width: int = 64
    max_height: int = 2048
    min_height: int = 64

class AdvancedValidator:
    """Validador avanzado de parámetros y configuraciones"""
    
    def __init__(self, config: Optional[AdvancedValidationConfig] = None):
        self.config = config if config else AdvancedValidationConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_handler = None
        self.file_manager = None
        self.ui_controller = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self.error_handler = get_error_handler()
            self.file_manager = get_file_manager()
            self.ui_controller = get_ui_controller()
    
    def validate_advanced_parameters(self, parameters: Dict[str, Any]) -> AdvancedValidationResult:
        """Valida parámetros avanzados de generación"""
        start_time = time.time()
        
        try:
            violations = []
            recommendations = []
            warnings = []
            validation_details = {}
            
            # 1. Validar prompts
            if self.config.validate_prompts:
                prompt_validation = self._validate_prompts(parameters)
                violations.extend(prompt_validation["violations"])
                recommendations.extend(prompt_validation["recommendations"])
                warnings.extend(prompt_validation["warnings"])
                validation_details["prompts"] = prompt_validation
            
            # 2. Validar parámetros de generación
            if self.config.validate_parameters:
                param_validation = self._validate_generation_parameters(parameters)
                violations.extend(param_validation["violations"])
                recommendations.extend(param_validation["recommendations"])
                warnings.extend(param_validation["warnings"])
                validation_details["parameters"] = param_validation
            
            # 3. Validar dimensiones
            if self.config.validate_dimensions:
                dimension_validation = self._validate_dimensions(parameters)
                violations.extend(dimension_validation["violations"])
                recommendations.extend(dimension_validation["recommendations"])
                warnings.extend(dimension_validation["warnings"])
                validation_details["dimensions"] = dimension_validation
            
            # 4. Validar calidad
            if self.config.validate_quality:
                quality_validation = self._validate_quality_settings(parameters)
                violations.extend(quality_validation["violations"])
                recommendations.extend(quality_validation["recommendations"])
                warnings.extend(quality_validation["warnings"])
                validation_details["quality"] = quality_validation
            
            # 5. Validar rendimiento
            if self.config.validate_performance:
                performance_validation = self._validate_performance_settings(parameters)
                violations.extend(performance_validation["violations"])
                recommendations.extend(performance_validation["recommendations"])
                warnings.extend(performance_validation["warnings"])
                validation_details["performance"] = performance_validation
            
            # Calcular puntuación
            score = self._calculate_validation_score(validation_details)
            
            # Determinar si es válido
            is_valid = len(violations) == 0 and score >= 0.8
            
            processing_time = time.time() - start_time
            
            return AdvancedValidationResult(
                is_valid=is_valid,
                score=score,
                violations=violations,
                recommendations=recommendations,
                warnings=warnings,
                validation_details=validation_details,
                processing_time=processing_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except Exception as e:
            self.logger.error(f"Error validando parámetros avanzados: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "advanced validation", "parameters": parameters})
            
            return AdvancedValidationResult(
                is_valid=False,
                score=0.0,
                violations=[f"Error en validación: {str(e)}"],
                recommendations=["Verificar que los parámetros son válidos"],
                processing_time=time.time() - start_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
    
    def generate_validation_report(self, results: List[AdvancedValidationResult]) -> str:
        """Genera un reporte de validación avanzada"""
        try:
            if not results:
                return "No hay resultados de validación para reportar"
            
            total_validations = len(results)
            valid_validations = sum(1 for r in results if r.is_valid)
            invalid_validations = total_validations - valid_validations
            
            report = f"# Reporte de Validación Avanzada\n\n"
            report += f"**Total de validaciones**: {total_validations}\n"
            report += f"**Validaciones válidas**: {valid_validations}\n"
            report += f"**Validaciones inválidas**: {invalid_validations}\n"
            report += f"**Tasa de éxito**: {(valid_validations/total_validations*100):.1f}%\n\n"
            
            # Estadísticas por categoría
            categories = ["prompts", "parameters", "dimensions", "quality", "performance"]
            for category in categories:
                category_violations = []
                for result in results:
                    if category in result.validation_details:
                        details = result.validation_details[category]
                        category_violations.extend(details.get("violations", []))
                
                if category_violations:
                    report += f"## {category.title()}\n"
                    report += f"**Violaciones**: {len(category_violations)}\n"
                    for violation in set(category_violations):
                        count = category_violations.count(violation)
                        report += f"- {violation} ({count} veces)\n"
                    report += "\n"
            
            # Detalles por validación
            for i, result in enumerate(results, 1):
                report += f"## Validación {i}\n"
                report += f"**Válida**: {'✅ Sí' if result.is_valid else '❌ No'}\n"
                report += f"**Puntuación**: {result.score:.2f}\n"
                report += f"**Tiempo de procesamiento**: {result.processing_time:.3f}s\n"
                
                if result.violations:
                    report += f"**Violaciones**:\n"
                    for violation in result.violations:
                        report += f"- {violation}\n"
                
                if result.recommendations:
                    report += f"**Recomendaciones**:\n"
                    for recommendation in result.recommendations:
                        report += f"- {recommendation}\n"
                
                if result.warnings:
                    report += f"**Advertencias**:\n"
                    for warning in result.warnings:
                        report += f"- {warning}\n"
                
                report += "\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte de validación: {e}")
            return f"Error generando reporte: {str(e)}"
    
    def handle_validation_errors(self, result: AdvancedValidationResult) -> Dict[str, Any]:
        """Maneja errores de validación"""
        try:
            if result.is_valid:
                return {
                    "success": True,
                    "message": "Validación exitosa",
                    "action": "continue"
                }
            
            # Analizar errores críticos
            critical_errors = []
            for violation in result.violations:
                if any(keyword in violation.lower() for keyword in ["crítico", "error", "fallo"]):
                    critical_errors.append(violation)
            
            if critical_errors:
                return {
                    "success": False,
                    "message": "Errores críticos encontrados",
                    "action": "stop",
                    "errors": critical_errors
                }
            
            # Analizar advertencias
            warnings = result.warnings
            if warnings:
                return {
                    "success": True,
                    "message": "Validación con advertencias",
                    "action": "continue_with_warnings",
                    "warnings": warnings
                }
            
            # Errores no críticos
            return {
                "success": False,
                "message": "Errores de validación encontrados",
                "action": "retry",
                "errors": result.violations
            }
            
        except Exception as e:
            self.logger.error(f"Error manejando errores de validación: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "handling validation errors"})
            
            return {
                "success": False,
                "message": f"Error manejando errores: {str(e)}",
                "action": "stop"
            }
    
    def _validate_prompts(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Valida los prompts de generación"""
        try:
            violations = []
            recommendations = []
            warnings = []
            
            # Obtener prompts
            positive_prompt = parameters.get("prompt", "")
            negative_prompt = parameters.get("negative_prompt", "")
            
            # Validar prompt positivo
            if not positive_prompt:
                violations.append("Prompt positivo vacío")
                recommendations.append("Proporcionar un prompt positivo descriptivo")
            elif len(positive_prompt) < self.config.min_prompt_length:
                violations.append(f"Prompt positivo demasiado corto: {len(positive_prompt)} caracteres (mínimo: {self.config.min_prompt_length})")
                recommendations.append("Añadir más detalles al prompt positivo")
            elif len(positive_prompt) > self.config.max_prompt_length:
                violations.append(f"Prompt positivo demasiado largo: {len(positive_prompt)} caracteres (máximo: {self.config.max_prompt_length})")
                recommendations.append("Acortar el prompt positivo")
            
            # Validar prompt negativo
            if negative_prompt and len(negative_prompt) > self.config.max_prompt_length:
                violations.append(f"Prompt negativo demasiado largo: {len(negative_prompt)} caracteres (máximo: {self.config.max_prompt_length})")
                recommendations.append("Acortar el prompt negativo")
            
            # Validar contenido de prompts
            if positive_prompt:
                # Verificar caracteres especiales
                special_chars = re.findall(r'[^\w\s,.-]', positive_prompt)
                if special_chars:
                    warnings.append(f"Caracteres especiales encontrados en prompt positivo: {set(special_chars)}")
                
                # Verificar palabras clave SAIME
                saime_keywords = ["512x768", "pasaporte", "documento", "oficial"]
                if not any(keyword in positive_prompt.lower() for keyword in saime_keywords):
                    warnings.append("Prompt no contiene palabras clave SAIME")
                    recommendations.append("Considerar añadir palabras clave SAIME al prompt")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "warnings": warnings,
                "prompt_length": len(positive_prompt),
                "negative_prompt_length": len(negative_prompt)
            }
            
        except Exception as e:
            self.logger.error(f"Error validando prompts: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando prompts: {str(e)}"],
                "recommendations": ["Verificar que los prompts son válidos"],
                "warnings": [],
                "prompt_length": 0,
                "negative_prompt_length": 0
            }
    
    def _validate_generation_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Valida parámetros de generación"""
        try:
            violations = []
            recommendations = []
            warnings = []
            
            # Validar steps
            steps = parameters.get("steps", 20)
            if steps < self.config.min_steps:
                violations.append(f"Pasos demasiado bajos: {steps} (mínimo: {self.config.min_steps})")
                recommendations.append("Aumentar el número de pasos")
            elif steps > self.config.max_steps:
                violations.append(f"Pasos demasiado altos: {steps} (máximo: {self.config.max_steps})")
                recommendations.append("Reducir el número de pasos para mejor rendimiento")
            
            # Validar CFG Scale
            cfg_scale = parameters.get("cfg_scale", 7.0)
            if cfg_scale < self.config.min_cfg_scale:
                violations.append(f"CFG Scale demasiado bajo: {cfg_scale} (mínimo: {self.config.min_cfg_scale})")
                recommendations.append("Aumentar el CFG Scale")
            elif cfg_scale > self.config.max_cfg_scale:
                violations.append(f"CFG Scale demasiado alto: {cfg_scale} (máximo: {self.config.max_cfg_scale})")
                recommendations.append("Reducir el CFG Scale")
            
            # Validar batch size
            batch_size = parameters.get("batch_size", 1)
            if batch_size < self.config.min_batch_size:
                violations.append(f"Batch size demasiado bajo: {batch_size} (mínimo: {self.config.min_batch_size})")
                recommendations.append("Aumentar el batch size")
            elif batch_size > self.config.max_batch_size:
                violations.append(f"Batch size demasiado alto: {batch_size} (máximo: {self.config.max_batch_size})")
                recommendations.append("Reducir el batch size para mejor rendimiento")
            
            # Advertencias de rendimiento
            if steps > 50 and batch_size > 1:
                warnings.append("Alta carga de procesamiento: muchos pasos y batch size alto")
                recommendations.append("Considerar reducir pasos o batch size para mejor rendimiento")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "warnings": warnings,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "batch_size": batch_size
            }
            
        except Exception as e:
            self.logger.error(f"Error validando parámetros de generación: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando parámetros: {str(e)}"],
                "recommendations": ["Verificar que los parámetros son válidos"],
                "warnings": [],
                "steps": 0,
                "cfg_scale": 0.0,
                "batch_size": 0
            }
    
    def _validate_dimensions(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Valida las dimensiones de la imagen"""
        try:
            violations = []
            recommendations = []
            warnings = []
            
            width = parameters.get("width", 512)
            height = parameters.get("height", 768)
            
            # Validar ancho
            if width < self.config.min_width:
                violations.append(f"Ancho demasiado pequeño: {width}px (mínimo: {self.config.min_width}px)")
                recommendations.append("Aumentar el ancho de la imagen")
            elif width > self.config.max_width:
                violations.append(f"Ancho demasiado grande: {width}px (máximo: {self.config.max_width}px)")
                recommendations.append("Reducir el ancho de la imagen")
            
            # Validar alto
            if height < self.config.min_height:
                violations.append(f"Alto demasiado pequeño: {height}px (mínimo: {self.config.min_height}px)")
                recommendations.append("Aumentar el alto de la imagen")
            elif height > self.config.max_height:
                violations.append(f"Alto demasiado grande: {height}px (máximo: {self.config.max_height}px)")
                recommendations.append("Reducir el alto de la imagen")
            
            # Validar proporción de aspecto
            aspect_ratio = width / height
            if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                warnings.append(f"Proporción de aspecto inusual: {aspect_ratio:.2f}")
                recommendations.append("Considerar una proporción de aspecto más estándar")
            
            # Advertencias de rendimiento
            total_pixels = width * height
            if total_pixels > 1024 * 1024:  # 1MP
                warnings.append("Imagen de alta resolución: puede afectar el rendimiento")
                recommendations.append("Considerar reducir la resolución para mejor rendimiento")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "warnings": warnings,
                "width": width,
                "height": height,
                "aspect_ratio": aspect_ratio,
                "total_pixels": total_pixels
            }
            
        except Exception as e:
            self.logger.error(f"Error validando dimensiones: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando dimensiones: {str(e)}"],
                "recommendations": ["Verificar que las dimensiones son válidas"],
                "warnings": [],
                "width": 0,
                "height": 0,
                "aspect_ratio": 0.0,
                "total_pixels": 0
            }
    
    def _validate_quality_settings(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Valida configuraciones de calidad"""
        try:
            violations = []
            recommendations = []
            warnings = []
            
            # Validar sampler
            sampler = parameters.get("sampler", "DPM++ 2M Karras")
            if not sampler:
                violations.append("Sampler no especificado")
                recommendations.append("Seleccionar un sampler apropiado")
            
            # Validar scheduler
            scheduler = parameters.get("scheduler", "karras")
            if not scheduler:
                violations.append("Scheduler no especificado")
                recommendations.append("Seleccionar un scheduler apropiado")
            
            # Validar seed
            seed = parameters.get("seed", -1)
            if seed == -1:
                warnings.append("Seed aleatorio: resultados no reproducibles")
                recommendations.append("Considerar usar un seed fijo para reproducibilidad")
            
            # Validar restorations
            restore_faces = parameters.get("restore_faces", False)
            if restore_faces:
                warnings.append("Restauración de caras habilitada: puede afectar la calidad")
                recommendations.append("Considerar deshabilitar restauración de caras para pasaportes")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "warnings": warnings,
                "sampler": sampler,
                "scheduler": scheduler,
                "seed": seed,
                "restore_faces": restore_faces
            }
            
        except Exception as e:
            self.logger.error(f"Error validando configuraciones de calidad: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando calidad: {str(e)}"],
                "recommendations": ["Verificar que las configuraciones son válidas"],
                "warnings": [],
                "sampler": "",
                "scheduler": "",
                "seed": -1,
                "restore_faces": False
            }
    
    def _validate_performance_settings(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Valida configuraciones de rendimiento"""
        try:
            violations = []
            recommendations = []
            warnings = []
            
            # Validar batch size vs cantidad
            batch_size = parameters.get("batch_size", 1)
            cantidad = parameters.get("cantidad", 1)
            
            if batch_size > cantidad:
                violations.append(f"Batch size mayor que cantidad: {batch_size} > {cantidad}")
                recommendations.append("Ajustar batch size para que no exceda la cantidad")
            
            # Validar memoria estimada
            width = parameters.get("width", 512)
            height = parameters.get("height", 768)
            steps = parameters.get("steps", 20)
            
            estimated_memory = (width * height * batch_size * steps) / 1000000  # MB aproximado
            if estimated_memory > 8000:  # 8GB
                warnings.append(f"Alto uso de memoria estimado: {estimated_memory:.1f}MB")
                recommendations.append("Considerar reducir batch size, pasos o resolución")
            
            # Validar tiempo estimado
            estimated_time = (steps * batch_size * cantidad) / 10  # segundos aproximados
            if estimated_time > 300:  # 5 minutos
                warnings.append(f"Tiempo estimado alto: {estimated_time:.1f}s")
                recommendations.append("Considerar reducir pasos, batch size o cantidad")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "warnings": warnings,
                "estimated_memory": estimated_memory,
                "estimated_time": estimated_time
            }
            
        except Exception as e:
            self.logger.error(f"Error validando configuraciones de rendimiento: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando rendimiento: {str(e)}"],
                "recommendations": ["Verificar que las configuraciones son válidas"],
                "warnings": [],
                "estimated_memory": 0.0,
                "estimated_time": 0.0
            }
    
    def _calculate_validation_score(self, validation_details: Dict[str, Any]) -> float:
        """Calcula la puntuación de validación"""
        try:
            total_score = 0.0
            total_weight = 0.0
            
            # Pesos para cada categoría
            weights = {
                "prompts": 0.20,
                "parameters": 0.25,
                "dimensions": 0.25,
                "quality": 0.15,
                "performance": 0.15
            }
            
            for category, weight in weights.items():
                if category in validation_details:
                    details = validation_details[category]
                    score = 1.0 if details.get("compliant", False) else 0.0
                    total_score += score * weight
                    total_weight += weight
            
            return total_score / total_weight if total_weight > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculando puntuación de validación: {e}")
            return 0.0

# Instancia global
_advanced_validator_instance: Optional[AdvancedValidator] = None

def get_advanced_validator() -> AdvancedValidator:
    """Obtiene la instancia global de AdvancedValidator"""
    global _advanced_validator_instance
    if _advanced_validator_instance is None:
        _advanced_validator_instance = AdvancedValidator()
    return _advanced_validator_instance
