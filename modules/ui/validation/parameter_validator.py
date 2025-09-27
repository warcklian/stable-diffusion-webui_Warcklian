#!/usr/bin/env python3
"""
Validador de Parámetros Modular
Sistema modular para validación de parámetros de generación
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import logging

@dataclass
class ValidationResult:
    """Resultado de validación de parámetros"""
    valid: bool
    error_message: str = ""
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

@dataclass
class GenerationValidationParams:
    """Parámetros para validación de generación"""
    # Parámetros básicos
    cantidad: int
    edad_min: int
    edad_max: int
    width: int
    height: int
    
    # Parámetros opcionales
    nacionalidad: str = ""
    genero: str = ""
    region: str = ""
    cfg_scale: float = 12.0
    steps: int = 35
    batch_size: int = 1
    
    # Parámetros SAIME
    is_saime: bool = False
    saime_width: int = 512
    saime_height: int = 768

class ParameterValidator:
    """Validador de parámetros de generación"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Límites de validación
        self.limits = {
            "cantidad_min": 1,
            "cantidad_max": 1000,
            "edad_min": 1,
            "edad_max": 120,
            "width_min": 64,
            "width_max": 2048,
            "height_min": 64,
            "height_max": 2048,
            "cfg_scale_min": 1.0,
            "cfg_scale_max": 30.0,
            "steps_min": 1,
            "steps_max": 150,
            "batch_size_min": 1,
            "batch_size_max": 32
        }
        
        # Especificaciones SAIME
        self.saime_specs = {
            "width": 512,
            "height": 768,
            "aspect_ratio": 512 / 768,
            "min_width": 512,
            "max_width": 512,
            "min_height": 768,
            "max_height": 768
        }
    
    def validate_generation_params(self, params: GenerationValidationParams) -> ValidationResult:
        """
        Valida parámetros de generación generales
        
        Args:
            params: Parámetros a validar
            
        Returns:
            ValidationResult: Resultado de la validación
        """
        try:
            warnings = []
            
            # Validar cantidad
            quantity_result = self.validate_quantity(params.cantidad)
            if not quantity_result.valid:
                return ValidationResult(valid=False, error_message=quantity_result.error_message)
            warnings.extend(quantity_result.warnings)
            
            # Validar rango de edad
            age_result = self.validate_age_range(params.edad_min, params.edad_max)
            if not age_result.valid:
                return ValidationResult(valid=False, error_message=age_result.error_message)
            warnings.extend(age_result.warnings)
            
            # Validar dimensiones
            dimensions_result = self.validate_dimensions(params.width, params.height, params.is_saime)
            if not dimensions_result.valid:
                return ValidationResult(valid=False, error_message=dimensions_result.error_message)
            warnings.extend(dimensions_result.warnings)
            
            # Validar parámetros opcionales
            optional_result = self._validate_optional_params(params)
            if not optional_result.valid:
                return ValidationResult(valid=False, error_message=optional_result.error_message)
            warnings.extend(optional_result.warnings)
            
            return ValidationResult(valid=True, warnings=warnings)
            
        except Exception as e:
            self.logger.error(f"Error en validación de parámetros: {e}")
            return ValidationResult(valid=False, error_message=f"Error de validación: {str(e)}")
    
    def validate_quantity(self, cantidad: int) -> ValidationResult:
        """
        Valida la cantidad de imágenes a generar
        
        Args:
            cantidad: Cantidad a validar
            
        Returns:
            ValidationResult: Resultado de la validación
        """
        try:
            cantidad_int = int(cantidad)
            warnings = []
            
            # Validar rango
            if cantidad_int < self.limits["cantidad_min"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La cantidad debe ser mayor o igual a {self.limits['cantidad_min']}"
                )
            
            if cantidad_int > self.limits["cantidad_max"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La cantidad no puede ser mayor a {self.limits['cantidad_max']}"
                )
            
            # Advertencias
            if cantidad_int > 100:
                warnings.append(f"⚠️ Generar {cantidad_int} imágenes puede tomar mucho tiempo")
            
            if cantidad_int > 500:
                warnings.append(f"⚠️ Se recomienda usar batch_size más pequeño para {cantidad_int} imágenes")
            
            return ValidationResult(valid=True, warnings=warnings)
            
        except (ValueError, TypeError) as e:
            return ValidationResult(
                valid=False,
                error_message=f"❌ Error: La cantidad debe ser un número entero válido"
            )
    
    def validate_age_range(self, edad_min: int, edad_max: int) -> ValidationResult:
        """
        Valida el rango de edad
        
        Args:
            edad_min: Edad mínima
            edad_max: Edad máxima
            
        Returns:
            ValidationResult: Resultado de la validación
        """
        try:
            edad_min_int = int(edad_min)
            edad_max_int = int(edad_max)
            warnings = []
            
            # Validar rango de edad mínima
            if edad_min_int < self.limits["edad_min"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La edad mínima debe ser mayor o igual a {self.limits['edad_min']}"
                )
            
            if edad_min_int > self.limits["edad_max"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La edad mínima no puede ser mayor a {self.limits['edad_max']}"
                )
            
            # Validar rango de edad máxima
            if edad_max_int < self.limits["edad_min"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La edad máxima debe ser mayor o igual a {self.limits['edad_min']}"
                )
            
            if edad_max_int > self.limits["edad_max"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La edad máxima no puede ser mayor a {self.limits['edad_max']}"
                )
            
            # Validar que edad_min < edad_max
            if edad_min_int >= edad_max_int:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La edad mínima ({edad_min_int}) debe ser menor que la máxima ({edad_max_int})"
                )
            
            # Advertencias
            age_range = edad_max_int - edad_min_int
            if age_range < 5:
                warnings.append(f"⚠️ Rango de edad muy pequeño ({age_range} años) puede limitar la diversidad")
            
            if age_range > 50:
                warnings.append(f"⚠️ Rango de edad muy amplio ({age_range} años) puede generar inconsistencias")
            
            return ValidationResult(valid=True, warnings=warnings)
            
        except (ValueError, TypeError) as e:
            return ValidationResult(
                valid=False,
                error_message=f"❌ Error: Las edades deben ser números enteros válidos"
            )
    
    def validate_dimensions(self, width: int, height: int, is_saime: bool = False) -> ValidationResult:
        """
        Valida las dimensiones de la imagen
        
        Args:
            width: Ancho de la imagen
            height: Alto de la imagen
            is_saime: Si es para especificaciones SAIME
            
        Returns:
            ValidationResult: Resultado de la validación
        """
        try:
            width_int = int(width)
            height_int = int(height)
            warnings = []
            
            # Validación SAIME
            if is_saime:
                saime_result = self.validate_saime_params(width_int, height_int)
                if not saime_result.valid:
                    return saime_result
                warnings.extend(saime_result.warnings)
                return ValidationResult(valid=True, warnings=warnings)
            
            # Validación general
            if width_int < self.limits["width_min"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: El ancho debe ser mayor o igual a {self.limits['width_min']} píxeles"
                )
            
            if width_int > self.limits["width_max"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: El ancho no puede ser mayor a {self.limits['width_max']} píxeles"
                )
            
            if height_int < self.limits["height_min"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La altura debe ser mayor o igual a {self.limits['height_min']} píxeles"
                )
            
            if height_int > self.limits["height_max"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La altura no puede ser mayor a {self.limits['height_max']} píxeles"
                )
            
            # Advertencias
            aspect_ratio = width_int / height_int
            if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                warnings.append(f"⚠️ Relación de aspecto inusual ({aspect_ratio:.2f}) puede afectar la calidad")
            
            if width_int * height_int > 1024 * 1024:
                warnings.append(f"⚠️ Resolución muy alta ({width_int}x{height_int}) puede requerir mucha memoria")
            
            return ValidationResult(valid=True, warnings=warnings)
            
        except (ValueError, TypeError) as e:
            return ValidationResult(
                valid=False,
                error_message=f"❌ Error: Las dimensiones deben ser números enteros válidos"
            )
    
    def validate_saime_params(self, width: int, height: int) -> ValidationResult:
        """
        Valida parámetros específicos para SAIME
        
        Args:
            width: Ancho de la imagen
            height: Alto de la imagen
            
        Returns:
            ValidationResult: Resultado de la validación
        """
        try:
            warnings = []
            
            # Validar dimensiones exactas SAIME
            if width != self.saime_specs["width"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: Para SAIME el ancho debe ser exactamente {self.saime_specs['width']} píxeles, no {width}"
                )
            
            if height != self.saime_specs["height"]:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: Para SAIME la altura debe ser exactamente {self.saime_specs['height']} píxeles, no {height}"
                )
            
            # Validar relación de aspecto
            aspect_ratio = width / height
            if abs(aspect_ratio - self.saime_specs["aspect_ratio"]) > 0.01:
                return ValidationResult(
                    valid=False,
                    error_message=f"❌ Error: La relación de aspecto debe ser {self.saime_specs['aspect_ratio']:.3f} para SAIME"
                )
            
            # Advertencias SAIME
            warnings.append("✅ Dimensiones SAIME correctas (512x768)")
            warnings.append("✅ Cumple especificaciones para pasaportes venezolanos")
            
            return ValidationResult(valid=True, warnings=warnings)
            
        except (ValueError, TypeError) as e:
            return ValidationResult(
                valid=False,
                error_message=f"❌ Error: Las dimensiones SAIME deben ser números enteros válidos"
            )
    
    def _validate_optional_params(self, params: GenerationValidationParams) -> ValidationResult:
        """Valida parámetros opcionales"""
        try:
            warnings = []
            
            # Validar cfg_scale
            if hasattr(params, 'cfg_scale'):
                if params.cfg_scale < self.limits["cfg_scale_min"]:
                    return ValidationResult(
                        valid=False,
                        error_message=f"❌ Error: CFG Scale debe ser mayor o igual a {self.limits['cfg_scale_min']}"
                    )
                if params.cfg_scale > self.limits["cfg_scale_max"]:
                    return ValidationResult(
                        valid=False,
                        error_message=f"❌ Error: CFG Scale no puede ser mayor a {self.limits['cfg_scale_max']}"
                    )
            
            # Validar steps
            if hasattr(params, 'steps'):
                if params.steps < self.limits["steps_min"]:
                    return ValidationResult(
                        valid=False,
                        error_message=f"❌ Error: Steps debe ser mayor o igual a {self.limits['steps_min']}"
                    )
                if params.steps > self.limits["steps_max"]:
                    return ValidationResult(
                        valid=False,
                        error_message=f"❌ Error: Steps no puede ser mayor a {self.limits['steps_max']}"
                    )
            
            # Validar batch_size
            if hasattr(params, 'batch_size'):
                if params.batch_size < self.limits["batch_size_min"]:
                    return ValidationResult(
                        valid=False,
                        error_message=f"❌ Error: Batch size debe ser mayor o igual a {self.limits['batch_size_min']}"
                    )
                if params.batch_size > self.limits["batch_size_max"]:
                    return ValidationResult(
                        valid=False,
                        error_message=f"❌ Error: Batch size no puede ser mayor a {self.limits['batch_size_max']}"
                    )
            
            return ValidationResult(valid=True, warnings=warnings)
            
        except Exception as e:
            return ValidationResult(
                valid=False,
                error_message=f"❌ Error validando parámetros opcionales: {str(e)}"
            )
    
    def get_validation_limits(self) -> Dict[str, Any]:
        """Obtiene los límites de validación"""
        return self.limits.copy()
    
    def get_saime_specs(self) -> Dict[str, Any]:
        """Obtiene las especificaciones SAIME"""
        return self.saime_specs.copy()

# Instancia global del validador
parameter_validator = ParameterValidator()

def get_parameter_validator() -> ParameterValidator:
    """Obtiene la instancia global del validador de parámetros"""
    return parameter_validator
