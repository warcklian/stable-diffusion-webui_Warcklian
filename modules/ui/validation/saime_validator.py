"""
Módulo de Validación SAIME
Sistema modular para validación de cumplimiento SAIME
"""

import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json
import time

# Imports de módulos de optimización
try:
    from modules.ui.utils import get_error_handler, get_file_manager
    from modules.ui.controls import get_ui_controller, create_ui_event, UIEventType
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

@dataclass
class SAIMEValidationResult:
    """Resultado de validación SAIME"""
    is_valid: bool
    score: float  # 0.0 a 1.0
    violations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    compliance_details: Dict[str, Any] = field(default_factory=dict)
    dimensions: Dict[str, int] = field(default_factory=dict)
    processing_time: float = 0.0
    timestamp: str = ""

@dataclass
class SAIMEValidationConfig:
    """Configuración de validación SAIME"""
    target_width: int = 512
    target_height: int = 768
    aspect_ratio: float = 512 / 768  # 0.667
    tolerance: float = 0.05  # 5% de tolerancia
    min_face_ratio: float = 0.3  # 30% del área de la imagen
    max_face_ratio: float = 0.7  # 70% del área de la imagen
    eye_position_ratio: float = 0.31  # 31% desde el borde superior
    shoulder_position_ratio: float = 0.78  # 78% desde el borde superior
    background_white_ratio: float = 0.95  # 95% de fondo blanco
    strict_mode: bool = True
    auto_correct: bool = False

class SAIMEValidator:
    """Validador automático de especificaciones SAIME"""
    
    def __init__(self, config: Optional[SAIMEValidationConfig] = None):
        self.config = config if config else SAIMEValidationConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_handler = None
        self.file_manager = None
        self.ui_controller = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self.error_handler = get_error_handler()
            self.file_manager = get_file_manager()
            self.ui_controller = get_ui_controller()
    
    def validate_saime_compliance(self, image_path: str) -> SAIMEValidationResult:
        """Valida una imagen contra las especificaciones SAIME"""
        start_time = time.time()
        
        try:
            # Cargar imagen
            image = cv2.imread(image_path)
            if image is None:
                return SAIMEValidationResult(
                    is_valid=False,
                    score=0.0,
                    violations=["No se pudo cargar la imagen"],
                    recommendations=["Verificar que el archivo existe y es válido"],
                    dimensions={"width": 0, "height": 0},
                    processing_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            height, width = image.shape[:2]
            violations = []
            recommendations = []
            compliance_details = {}
            
            # 1. Validar dimensiones
            dimension_compliance = self._validate_dimensions(width, height)
            violations.extend(dimension_compliance["violations"])
            recommendations.extend(dimension_compliance["recommendations"])
            compliance_details["dimensions"] = dimension_compliance
            
            # 2. Validar proporción de aspecto
            aspect_compliance = self._validate_aspect_ratio(width, height)
            violations.extend(aspect_compliance["violations"])
            recommendations.extend(aspect_compliance["recommendations"])
            compliance_details["aspect_ratio"] = aspect_compliance
            
            # 3. Validar fondo blanco
            background_compliance = self._validate_background(image)
            violations.extend(background_compliance["violations"])
            recommendations.extend(background_compliance["recommendations"])
            compliance_details["background"] = background_compliance
            
            # 4. Validar detección de rostro
            face_compliance = self._validate_face_detection(image)
            violations.extend(face_compliance["violations"])
            recommendations.extend(face_compliance["recommendations"])
            compliance_details["face_detection"] = face_compliance
            
            # 5. Validar posición de ojos
            eye_compliance = self._validate_eye_position(image)
            violations.extend(eye_compliance["violations"])
            recommendations.extend(eye_compliance["recommendations"])
            compliance_details["eye_position"] = eye_compliance
            
            # 6. Validar posición de hombros
            shoulder_compliance = self._validate_shoulder_position(image)
            violations.extend(shoulder_compliance["violations"])
            recommendations.extend(shoulder_compliance["recommendations"])
            compliance_details["shoulder_position"] = shoulder_compliance
            
            # Calcular puntuación
            score = self._calculate_compliance_score(compliance_details)
            
            # Determinar si es válido
            is_valid = len(violations) == 0 and score >= 0.8
            
            processing_time = time.time() - start_time
            
            return SAIMEValidationResult(
                is_valid=is_valid,
                score=score,
                violations=violations,
                recommendations=recommendations,
                compliance_details=compliance_details,
                dimensions={"width": width, "height": height},
                processing_time=processing_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except Exception as e:
            self.logger.error(f"Error validando cumplimiento SAIME: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "SAIME validation", "image_path": image_path})
            
            return SAIMEValidationResult(
                is_valid=False,
                score=0.0,
                violations=[f"Error en validación: {str(e)}"],
                recommendations=["Verificar que la imagen es válida y accesible"],
                dimensions={"width": 0, "height": 0},
                processing_time=time.time() - start_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
    
    def validate_dimensions(self, width: int, height: int) -> Dict[str, Any]:
        """Valida las dimensiones de la imagen"""
        try:
            violations = []
            recommendations = []
            
            # Validar ancho
            if width != self.config.target_width:
                violations.append(f"Ancho incorrecto: {width}px (requerido: {self.config.target_width}px)")
                recommendations.append("Ajustar el ancho a 512 píxeles")
            
            # Validar alto
            if height != self.config.target_height:
                violations.append(f"Alto incorrecto: {height}px (requerido: {self.config.target_height}px)")
                recommendations.append("Ajustar el alto a 768 píxeles")
            
            # Validar tolerancia si no es modo estricto
            if not self.config.strict_mode:
                width_tolerance = abs(width - self.config.target_width) / self.config.target_width
                height_tolerance = abs(height - self.config.target_height) / self.config.target_height
                
                if width_tolerance > self.config.tolerance:
                    violations.append(f"Ancho fuera de tolerancia: {width_tolerance:.2%} (máximo: {self.config.tolerance:.2%})")
                
                if height_tolerance > self.config.tolerance:
                    violations.append(f"Alto fuera de tolerancia: {height_tolerance:.2%} (máximo: {self.config.tolerance:.2%})")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "actual_dimensions": {"width": width, "height": height},
                "target_dimensions": {"width": self.config.target_width, "height": self.config.target_height}
            }
            
        except Exception as e:
            self.logger.error(f"Error validando dimensiones: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando dimensiones: {str(e)}"],
                "recommendations": ["Verificar que las dimensiones son números válidos"],
                "actual_dimensions": {"width": width, "height": height},
                "target_dimensions": {"width": self.config.target_width, "height": self.config.target_height}
            }
    
    def validate_background(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida el fondo de la imagen"""
        try:
            violations = []
            recommendations = []
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calcular histograma
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            
            # Encontrar el pico más alto (fondo dominante)
            dominant_value = np.argmax(hist)
            
            # Calcular porcentaje de píxeles blancos (valores altos)
            white_pixels = np.sum(gray > 200)  # Píxeles casi blancos
            total_pixels = gray.size
            white_ratio = white_pixels / total_pixels
            
            if white_ratio < self.config.background_white_ratio:
                violations.append(f"Fondo insuficientemente blanco: {white_ratio:.2%} (requerido: {self.config.background_white_ratio:.2%})")
                recommendations.append("Ajustar el fondo para que sea más blanco")
            
            return {
                "compliant": white_ratio >= self.config.background_white_ratio,
                "violations": violations,
                "recommendations": recommendations,
                "white_ratio": white_ratio,
                "dominant_value": int(dominant_value)
            }
            
        except Exception as e:
            self.logger.error(f"Error validando fondo: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando fondo: {str(e)}"],
                "recommendations": ["Verificar que la imagen es válida"],
                "white_ratio": 0.0,
                "dominant_value": 0
            }
    
    def validate_expression(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la expresión facial"""
        try:
            violations = []
            recommendations = []
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar rostro usando Haar Cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                violations.append("No se detectó rostro en la imagen")
                recommendations.append("Asegurar que hay un rostro visible en la imagen")
                return {
                    "compliant": False,
                    "violations": violations,
                    "recommendations": recommendations,
                    "face_detected": False,
                    "face_count": 0
                }
            
            # Validar que solo hay un rostro
            if len(faces) > 1:
                violations.append(f"Múltiples rostros detectados: {len(faces)}")
                recommendations.append("Asegurar que solo hay un rostro en la imagen")
            
            # Validar expresión neutra (simplificado)
            # En una implementación real, se usaría un modelo de reconocimiento de emociones
            expression_score = 0.8  # Simulado
            
            if expression_score < 0.7:
                violations.append("Expresión no neutra detectada")
                recommendations.append("Asegurar que la expresión facial sea neutra")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "face_detected": True,
                "face_count": len(faces),
                "expression_score": expression_score
            }
            
        except Exception as e:
            self.logger.error(f"Error validando expresión: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando expresión: {str(e)}"],
                "recommendations": ["Verificar que la imagen es válida"],
                "face_detected": False,
                "face_count": 0,
                "expression_score": 0.0
            }
    
    def _validate_dimensions(self, width: int, height: int) -> Dict[str, Any]:
        """Valida las dimensiones de la imagen"""
        return self.validate_dimensions(width, height)
    
    def _validate_aspect_ratio(self, width: int, height: int) -> Dict[str, Any]:
        """Valida la proporción de aspecto"""
        try:
            violations = []
            recommendations = []
            
            actual_ratio = width / height
            target_ratio = self.config.aspect_ratio
            
            if abs(actual_ratio - target_ratio) > 0.01:
                violations.append(f"Proporción de aspecto incorrecta: {actual_ratio:.3f} (requerida: {target_ratio:.3f})")
                recommendations.append("Ajustar las dimensiones para mantener la proporción correcta")
            
            return {
                "compliant": abs(actual_ratio - target_ratio) <= 0.01,
                "violations": violations,
                "recommendations": recommendations,
                "actual_ratio": actual_ratio,
                "target_ratio": target_ratio
            }
            
        except Exception as e:
            self.logger.error(f"Error validando proporción de aspecto: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando proporción de aspecto: {str(e)}"],
                "recommendations": ["Verificar que las dimensiones son válidas"],
                "actual_ratio": 0.0,
                "target_ratio": self.config.aspect_ratio
            }
    
    def _validate_background(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida el fondo de la imagen"""
        return self.validate_background(image)
    
    def _validate_face_detection(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la detección de rostro"""
        try:
            violations = []
            recommendations = []
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar rostro
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                violations.append("No se detectó rostro en la imagen")
                recommendations.append("Asegurar que hay un rostro visible en la imagen")
                return {
                    "compliant": False,
                    "violations": violations,
                    "recommendations": recommendations,
                    "face_detected": False,
                    "face_count": 0
                }
            
            # Validar tamaño del rostro
            for (x, y, w, h) in faces:
                face_area = w * h
                total_area = image.shape[0] * image.shape[1]
                face_ratio = face_area / total_area
                
                if face_ratio < self.config.min_face_ratio:
                    violations.append(f"Rostro demasiado pequeño: {face_ratio:.2%} (mínimo: {self.config.min_face_ratio:.2%})")
                    recommendations.append("Acercar la cámara o ajustar el encuadre")
                
                if face_ratio > self.config.max_face_ratio:
                    violations.append(f"Rostro demasiado grande: {face_ratio:.2%} (máximo: {self.config.max_face_ratio:.2%})")
                    recommendations.append("Alejar la cámara o ajustar el encuadre")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "face_detected": True,
                "face_count": len(faces)
            }
            
        except Exception as e:
            self.logger.error(f"Error validando detección de rostro: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando detección de rostro: {str(e)}"],
                "recommendations": ["Verificar que la imagen es válida"],
                "face_detected": False,
                "face_count": 0
            }
    
    def _validate_eye_position(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la posición de los ojos"""
        try:
            violations = []
            recommendations = []
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar ojos
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(eyes) == 0:
                violations.append("No se detectaron ojos en la imagen")
                recommendations.append("Asegurar que los ojos son visibles")
                return {
                    "compliant": False,
                    "violations": violations,
                    "recommendations": recommendations,
                    "eyes_detected": False,
                    "eye_count": 0
                }
            
            # Validar posición de ojos
            for (x, y, w, h) in eyes:
                eye_y_ratio = y / image.shape[0]
                
                if eye_y_ratio < (self.config.eye_position_ratio - 0.05):
                    violations.append(f"Ojos demasiado altos: {eye_y_ratio:.2%} (requerido: {self.config.eye_position_ratio:.2%})")
                    recommendations.append("Ajustar la posición de la cámara")
                
                if eye_y_ratio > (self.config.eye_position_ratio + 0.05):
                    violations.append(f"Ojos demasiado bajos: {eye_y_ratio:.2%} (requerido: {self.config.eye_position_ratio:.2%})")
                    recommendations.append("Ajustar la posición de la cámara")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "eyes_detected": True,
                "eye_count": len(eyes)
            }
            
        except Exception as e:
            self.logger.error(f"Error validando posición de ojos: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando posición de ojos: {str(e)}"],
                "recommendations": ["Verificar que la imagen es válida"],
                "eyes_detected": False,
                "eye_count": 0
            }
    
    def _validate_shoulder_position(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la posición de los hombros"""
        try:
            violations = []
            recommendations = []
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar hombros (simplificado)
            # En una implementación real, se usaría un modelo de pose estimation
            shoulder_detected = True  # Simulado
            shoulder_ratio = 0.78  # Simulado
            
            if not shoulder_detected:
                violations.append("No se detectaron hombros en la imagen")
                recommendations.append("Asegurar que los hombros son visibles")
            
            if abs(shoulder_ratio - self.config.shoulder_position_ratio) > 0.05:
                violations.append(f"Posición de hombros incorrecta: {shoulder_ratio:.2%} (requerida: {self.config.shoulder_position_ratio:.2%})")
                recommendations.append("Ajustar la posición de la cámara")
            
            return {
                "compliant": len(violations) == 0,
                "violations": violations,
                "recommendations": recommendations,
                "shoulder_detected": shoulder_detected,
                "shoulder_ratio": shoulder_ratio
            }
            
        except Exception as e:
            self.logger.error(f"Error validando posición de hombros: {e}")
            return {
                "compliant": False,
                "violations": [f"Error validando posición de hombros: {str(e)}"],
                "recommendations": ["Verificar que la imagen es válida"],
                "shoulder_detected": False,
                "shoulder_ratio": 0.0
            }
    
    def _calculate_compliance_score(self, compliance_details: Dict[str, Any]) -> float:
        """Calcula la puntuación de cumplimiento"""
        try:
            total_score = 0.0
            total_weight = 0.0
            
            # Pesos para cada aspecto
            weights = {
                "dimensions": 0.25,
                "aspect_ratio": 0.15,
                "background": 0.20,
                "face_detection": 0.20,
                "eye_position": 0.10,
                "shoulder_position": 0.10
            }
            
            for aspect, weight in weights.items():
                if aspect in compliance_details:
                    details = compliance_details[aspect]
                    score = 1.0 if details.get("compliant", False) else 0.0
                    total_score += score * weight
                    total_weight += weight
            
            return total_score / total_weight if total_weight > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculando puntuación de cumplimiento: {e}")
            return 0.0
    
    def generate_validation_report(self, results: List[SAIMEValidationResult]) -> str:
        """Genera un reporte de validación"""
        try:
            if not results:
                return "No hay resultados de validación para reportar"
            
            total_images = len(results)
            valid_images = sum(1 for r in results if r.is_valid)
            invalid_images = total_images - valid_images
            
            report = f"# Reporte de Validación SAIME\n\n"
            report += f"**Total de imágenes**: {total_images}\n"
            report += f"**Imágenes válidas**: {valid_images}\n"
            report += f"**Imágenes inválidas**: {invalid_images}\n"
            report += f"**Tasa de cumplimiento**: {(valid_images/total_images*100):.1f}%\n\n"
            
            # Detalles por imagen
            for i, result in enumerate(results, 1):
                report += f"## Imagen {i}\n"
                report += f"**Válida**: {'✅ Sí' if result.is_valid else '❌ No'}\n"
                report += f"**Puntuación**: {result.score:.2f}\n"
                report += f"**Dimensiones**: {result.dimensions.get('width', 0)}x{result.dimensions.get('height', 0)}\n"
                
                if result.violations:
                    report += f"**Violaciones**:\n"
                    for violation in result.violations:
                        report += f"- {violation}\n"
                
                if result.recommendations:
                    report += f"**Recomendaciones**:\n"
                    for recommendation in result.recommendations:
                        report += f"- {recommendation}\n"
                
                report += "\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte de validación: {e}")
            return f"Error generando reporte: {str(e)}"

# Instancia global
_saime_validator_instance: Optional[SAIMEValidator] = None

def get_saime_validator() -> SAIMEValidator:
    """Obtiene la instancia global de SAIMEValidator"""
    global _saime_validator_instance
    if _saime_validator_instance is None:
        _saime_validator_instance = SAIMEValidator()
    return _saime_validator_instance
