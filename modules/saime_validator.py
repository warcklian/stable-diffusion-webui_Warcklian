#!/usr/bin/env python3
"""
Validador Automático SAIME
Sistema para validar automáticamente el cumplimiento de especificaciones SAIME
"""

import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class SAIMEValidationResult:
    """Resultado de validación SAIME"""
    is_valid: bool
    score: float  # 0.0 a 1.0
    violations: List[str]
    recommendations: List[str]
    dimensions: Dict[str, int]
    compliance_details: Dict[str, Any]

class SAIMEValidator:
    """Validador automático de especificaciones SAIME"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Especificaciones SAIME críticas
        self.saime_specs = {
            "target_width": 512,
            "target_height": 768,
            "aspect_ratio": 512 / 768,  # 0.667
            "tolerance": 0.05,  # 5% de tolerancia
            "min_face_ratio": 0.3,  # 30% del área de la imagen
            "max_face_ratio": 0.7,  # 70% del área de la imagen
            "eye_position_ratio": 0.31,  # 31% desde el borde superior
            "shoulder_position_ratio": 0.78,  # 78% desde el borde superior
            "background_tolerance": 0.95  # 95% de fondo blanco
        }
    
    def validate_image(self, image_path: str) -> SAIMEValidationResult:
        """Valida una imagen contra las especificaciones SAIME"""
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
                    compliance_details={}
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
            
            # Calcular score general
            total_checks = 6
            passed_checks = total_checks - len(violations)
            score = passed_checks / total_checks
            
            is_valid = len(violations) == 0 and score >= 0.8
            
            return SAIMEValidationResult(
                is_valid=is_valid,
                score=score,
                violations=violations,
                recommendations=recommendations,
                dimensions={"width": width, "height": height},
                compliance_details=compliance_details
            )
            
        except Exception as e:
            self.logger.error(f"Error validando imagen {image_path}: {e}")
            return SAIMEValidationResult(
                is_valid=False,
                score=0.0,
                violations=[f"Error de validación: {str(e)}"],
                recommendations=["Verificar integridad de la imagen"],
                dimensions={"width": 0, "height": 0},
                compliance_details={}
            )
    
    def _validate_dimensions(self, width: int, height: int) -> Dict[str, Any]:
        """Valida las dimensiones de la imagen"""
        target_width = self.saime_specs["target_width"]
        target_height = self.saime_specs["target_height"]
        tolerance = self.saime_specs["tolerance"]
        
        width_ok = abs(width - target_width) / target_width <= tolerance
        height_ok = abs(height - target_height) / target_height <= tolerance
        
        violations = []
        recommendations = []
        
        if not width_ok:
            violations.append(f"Ancho incorrecto: {width}px (esperado: {target_width}px)")
            recommendations.append(f"Ajustar ancho a {target_width}px")
        
        if not height_ok:
            violations.append(f"Alto incorrecto: {height}px (esperado: {target_height}px)")
            recommendations.append(f"Ajustar alto a {target_height}px")
        
        return {
            "valid": width_ok and height_ok,
            "violations": violations,
            "recommendations": recommendations,
            "actual": {"width": width, "height": height},
            "expected": {"width": target_width, "height": target_height}
        }
    
    def _validate_aspect_ratio(self, width: int, height: int) -> Dict[str, Any]:
        """Valida la proporción de aspecto"""
        actual_ratio = width / height
        target_ratio = self.saime_specs["aspect_ratio"]
        tolerance = self.saime_specs["tolerance"]
        
        ratio_ok = abs(actual_ratio - target_ratio) <= tolerance
        
        violations = []
        recommendations = []
        
        if not ratio_ok:
            violations.append(f"Proporción incorrecta: {actual_ratio:.3f} (esperada: {target_ratio:.3f})")
            recommendations.append(f"Ajustar proporción a {target_ratio:.3f}")
        
        return {
            "valid": ratio_ok,
            "violations": violations,
            "recommendations": recommendations,
            "actual_ratio": actual_ratio,
            "target_ratio": target_ratio
        }
    
    def _validate_background(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida que el fondo sea blanco"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calcular el porcentaje de píxeles blancos
        white_pixels = np.sum(gray > 240)  # Umbral para blanco
        total_pixels = gray.size
        white_percentage = white_pixels / total_pixels
        
        target_percentage = self.saime_specs["background_tolerance"]
        background_ok = white_percentage >= target_percentage
        
        violations = []
        recommendations = []
        
        if not background_ok:
            violations.append(f"Fondo no es suficientemente blanco: {white_percentage:.1%} (mínimo: {target_percentage:.1%})")
            recommendations.append("Asegurar fondo blanco sólido sin texturas")
        
        return {
            "valid": background_ok,
            "violations": violations,
            "recommendations": recommendations,
            "white_percentage": white_percentage,
            "target_percentage": target_percentage
        }
    
    def _validate_face_detection(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la detección de rostro"""
        # Cargar clasificador de rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        face_detected = len(faces) > 0
        
        violations = []
        recommendations = []
        
        if not face_detected:
            violations.append("No se detectó rostro en la imagen")
            recommendations.append("Asegurar que el rostro sea visible y frontal")
        elif len(faces) > 1:
            violations.append(f"Se detectaron múltiples rostros: {len(faces)}")
            recommendations.append("Asegurar que solo haya un rostro visible")
        
        # Calcular proporción del rostro
        face_ratio = 0.0
        if face_detected and len(faces) == 1:
            x, y, w, h = faces[0]
            face_area = w * h
            image_area = image.shape[0] * image.shape[1]
            face_ratio = face_area / image_area
            
            min_ratio = self.saime_specs["min_face_ratio"]
            max_ratio = self.saime_specs["max_face_ratio"]
            
            if face_ratio < min_ratio:
                violations.append(f"Rostro muy pequeño: {face_ratio:.1%} (mínimo: {min_ratio:.1%})")
                recommendations.append("Acercar la cámara o ajustar el encuadre")
            elif face_ratio > max_ratio:
                violations.append(f"Rostro muy grande: {face_ratio:.1%} (máximo: {max_ratio:.1%})")
                recommendations.append("Alejar la cámara o ajustar el encuadre")
        
        return {
            "valid": face_detected and len(faces) == 1,
            "violations": violations,
            "recommendations": recommendations,
            "faces_detected": len(faces),
            "face_ratio": face_ratio
        }
    
    def _validate_eye_position(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la posición de los ojos"""
        # Cargar clasificador de ojos
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
        
        eyes_detected = len(eyes) >= 2
        
        violations = []
        recommendations = []
        
        if not eyes_detected:
            violations.append("No se detectaron ojos en la imagen")
            recommendations.append("Asegurar que los ojos sean visibles y abiertos")
        else:
            # Calcular posición promedio de los ojos
            eye_centers = []
            for (x, y, w, h) in eyes:
                center_x = x + w // 2
                center_y = y + h // 2
                eye_centers.append((center_x, center_y))
            
            if len(eye_centers) >= 2:
                # Usar los dos ojos más prominentes
                eye_centers = sorted(eye_centers, key=lambda e: e[1])[:2]
                avg_eye_y = sum(eye[1] for eye in eye_centers) / len(eye_centers)
                
                image_height = image.shape[0]
                eye_position_ratio = avg_eye_y / image_height
                target_ratio = self.saime_specs["eye_position_ratio"]
                tolerance = 0.05
                
                if abs(eye_position_ratio - target_ratio) > tolerance:
                    violations.append(f"Posición de ojos incorrecta: {eye_position_ratio:.1%} (esperada: {target_ratio:.1%})")
                    recommendations.append("Ajustar la posición de la cabeza para que los ojos estén al 31% desde arriba")
        
        return {
            "valid": eyes_detected,
            "violations": violations,
            "recommendations": recommendations,
            "eyes_detected": len(eyes),
            "eye_position_ratio": eye_position_ratio if eyes_detected else 0.0
        }
    
    def _validate_shoulder_position(self, image: np.ndarray) -> Dict[str, Any]:
        """Valida la posición de los hombros"""
        # Esta es una validación simplificada
        # En una implementación completa, se usaría detección de pose
        height = image.shape[0]
        target_shoulder_y = int(height * self.saime_specs["shoulder_position_ratio"])
        
        # Validación básica: verificar que hay contenido en la zona de hombros
        shoulder_region = image[target_shoulder_y-20:target_shoulder_y+20, :]
        shoulder_content = np.mean(shoulder_region)
        
        # Si la región de hombros es muy clara (blanca), probablemente no hay hombros
        shoulders_visible = shoulder_content < 200  # Umbral empírico
        
        violations = []
        recommendations = []
        
        if not shoulders_visible:
            violations.append("Hombros no visibles en la posición correcta")
            recommendations.append("Asegurar que los hombros sean visibles al 78% de la altura")
        
        return {
            "valid": shoulders_visible,
            "violations": violations,
            "recommendations": recommendations,
            "shoulder_region_brightness": shoulder_content,
            "target_shoulder_y": target_shoulder_y
        }
    
    def generate_validation_report(self, validation_result: SAIMEValidationResult) -> str:
        """Genera un reporte de validación legible"""
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE VALIDACIÓN SAIME")
        report.append("=" * 60)
        
        # Estado general
        status = "✅ VÁLIDA" if validation_result.is_valid else "❌ INVÁLIDA"
        report.append(f"Estado: {status}")
        report.append(f"Score: {validation_result.score:.1%}")
        report.append(f"Dimensiones: {validation_result.dimensions['width']}x{validation_result.dimensions['height']}")
        report.append("")
        
        # Violaciones
        if validation_result.violations:
            report.append("🚨 VIOLACIONES DETECTADAS:")
            for i, violation in enumerate(validation_result.violations, 1):
                report.append(f"  {i}. {violation}")
            report.append("")
        
        # Recomendaciones
        if validation_result.recommendations:
            report.append("💡 RECOMENDACIONES:")
            for i, recommendation in enumerate(validation_result.recommendations, 1):
                report.append(f"  {i}. {recommendation}")
            report.append("")
        
        # Detalles de cumplimiento
        report.append("📊 DETALLES DE CUMPLIMIENTO:")
        for category, details in validation_result.compliance_details.items():
            status_icon = "✅" if details.get("valid", False) else "❌"
            report.append(f"  {status_icon} {category.upper()}: {details.get('valid', False)}")
        
        report.append("=" * 60)
        
        return "\n".join(report)

# Instancia global del validador
saime_validator = SAIMEValidator()

def validate_saime_compliance(image_path: str) -> SAIMEValidationResult:
    """Valida el cumplimiento SAIME de una imagen"""
    return saime_validator.validate_image(image_path)

def generate_saime_report(image_path: str) -> str:
    """Genera un reporte de validación SAIME"""
    result = validate_saime_compliance(image_path)
    return saime_validator.generate_validation_report(result)
