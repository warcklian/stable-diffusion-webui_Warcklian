#!/usr/bin/env python3
"""
Sistema de Balanceo Inteligente Mejorado
Sistema avanzado para evitar repeticiones excesivas en generación masiva
"""

import random
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging

@dataclass
class BalanceConfig:
    """Configuración de balanceo"""
    max_repetitions: int = 3  # Máximo de repeticiones consecutivas
    diversity_threshold: float = 0.7  # Umbral de diversidad mínimo
    history_size: int = 100  # Tamaño del historial a considerar
    weight_decay: float = 0.9  # Decaimiento de peso para opciones antiguas
    adaptive_balancing: bool = True  # Balanceo adaptativo

@dataclass
class GenerationHistory:
    """Historial de generaciones"""
    timestamp: float
    characteristics: Dict[str, str]
    image_id: str
    weight: float = 1.0

class IntelligentBalancer:
    """Sistema de balanceo inteligente mejorado"""
    
    def __init__(self, config: Optional[BalanceConfig] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or BalanceConfig()
        self.generation_history: List[GenerationHistory] = []
        self.characteristic_weights: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.repetition_tracker: Dict[str, List[str]] = defaultdict(list)
        self.diversity_scores: Dict[str, float] = {}
        
    def add_generation(self, characteristics: Dict[str, str], image_id: str) -> None:
        """Añade una generación al historial"""
        history_entry = GenerationHistory(
            timestamp=time.time(),
            characteristics=characteristics.copy(),
            image_id=image_id
        )
        
        self.generation_history.append(history_entry)
        
        # Actualizar pesos de características
        self._update_characteristic_weights(characteristics)
        
        # Actualizar tracker de repeticiones
        self._update_repetition_tracker(characteristics)
        
        # Limpiar historial antiguo
        self._cleanup_old_history()
    
    def _update_characteristic_weights(self, characteristics: Dict[str, str]) -> None:
        """Actualiza los pesos de las características"""
        current_time = time.time()
        
        for category, value in characteristics.items():
            if value != "aleatorio":
                # Reducir peso de opciones recientes
                self.characteristic_weights[category][value] *= self.config.weight_decay
                
                # Añadir peso basado en antigüedad
                age_factor = 1.0 / (1.0 + (current_time - self.generation_history[-1].timestamp) / 3600)
                self.characteristic_weights[category][value] += age_factor
    
    def _update_repetition_tracker(self, characteristics: Dict[str, str]) -> None:
        """Actualiza el tracker de repeticiones"""
        for category, value in characteristics.items():
            if value != "aleatorio":
                self.repetition_tracker[category].append(value)
                
                # Mantener solo las últimas N repeticiones
                if len(self.repetition_tracker[category]) > self.config.max_repetitions * 2:
                    self.repetition_tracker[category] = self.repetition_tracker[category][-self.config.max_repetitions:]
    
    def _cleanup_old_history(self) -> None:
        """Limpia el historial antiguo"""
        current_time = time.time()
        cutoff_time = current_time - (self.config.history_size * 3600)  # 1 hora por entrada
        
        self.generation_history = [
            entry for entry in self.generation_history 
            if entry.timestamp > cutoff_time
        ]
    
    def get_balanced_characteristics(self, available_options: Dict[str, List[str]], 
                                   nationality: str, gender: str, age: int) -> Dict[str, str]:
        """Genera características balanceadas"""
        balanced_characteristics = {}
        
        for category, options in available_options.items():
            if not options:
                balanced_characteristics[category] = "aleatorio"
                continue
            
            # Filtrar opciones basadas en repeticiones recientes
            filtered_options = self._filter_recent_repetitions(category, options)
            
            # Aplicar balanceo inteligente
            selected_value = self._intelligent_selection(category, filtered_options)
            balanced_characteristics[category] = selected_value
        
        return balanced_characteristics
    
    def _filter_recent_repetitions(self, category: str, options: List[str]) -> List[str]:
        """Filtra opciones que han sido usadas recientemente"""
        if category not in self.repetition_tracker:
            return options
        
        recent_values = self.repetition_tracker[category][-self.config.max_repetitions:]
        recent_counts = Counter(recent_values)
        
        # Filtrar opciones que han alcanzado el máximo de repeticiones
        filtered_options = []
        for option in options:
            if recent_counts[option] < self.config.max_repetitions:
                filtered_options.append(option)
        
        # Si todas las opciones están filtradas, usar todas
        return filtered_options if filtered_options else options
    
    def _intelligent_selection(self, category: str, options: List[str]) -> str:
        """Selección inteligente basada en pesos y diversidad"""
        if not options:
            return "aleatorio"
        
        # Calcular pesos para cada opción
        option_weights = {}
        for option in options:
            if option == "aleatorio":
                option_weights[option] = 1.0
            else:
                # Peso base
                base_weight = 1.0
                
                # Ajustar por frecuencia histórica
                frequency_weight = 1.0 / (1.0 + self.characteristic_weights[category][option])
                
                # Ajustar por diversidad
                diversity_weight = self._calculate_diversity_weight(category, option)
                
                option_weights[option] = base_weight * frequency_weight * diversity_weight
        
        # Selección ponderada
        return self._weighted_selection(option_weights)
    
    def _calculate_diversity_weight(self, category: str, option: str) -> float:
        """Calcula el peso de diversidad para una opción"""
        if not self.generation_history:
            return 1.0
        
        # Calcular diversidad basada en combinaciones recientes
        recent_combinations = self._get_recent_combinations(category, option)
        diversity_score = self._calculate_combination_diversity(recent_combinations)
        
        # Convertir diversidad a peso (mayor diversidad = mayor peso)
        return 1.0 + diversity_score
    
    def _get_recent_combinations(self, category: str, option: str) -> List[Dict[str, str]]:
        """Obtiene combinaciones recientes que incluyen esta opción"""
        recent_history = self.generation_history[-10:]  # Últimas 10 generaciones
        
        combinations = []
        for entry in recent_history:
            if entry.characteristics.get(category) == option:
                combinations.append(entry.characteristics)
        
        return combinations
    
    def _calculate_combination_diversity(self, combinations: List[Dict[str, str]]) -> float:
        """Calcula la diversidad de combinaciones"""
        if len(combinations) < 2:
            return 1.0
        
        # Calcular similitud promedio entre combinaciones
        similarities = []
        for i in range(len(combinations)):
            for j in range(i + 1, len(combinations)):
                similarity = self._calculate_similarity(combinations[i], combinations[j])
                similarities.append(similarity)
        
        if not similarities:
            return 1.0
        
        avg_similarity = sum(similarities) / len(similarities)
        diversity = 1.0 - avg_similarity  # Mayor diversidad = menor similitud
        
        return max(0.0, min(1.0, diversity))
    
    def _calculate_similarity(self, combo1: Dict[str, str], combo2: Dict[str, str]) -> float:
        """Calcula la similitud entre dos combinaciones"""
        if not combo1 or not combo2:
            return 0.0
        
        common_keys = set(combo1.keys()) & set(combo2.keys())
        if not common_keys:
            return 0.0
        
        matches = sum(1 for key in common_keys if combo1[key] == combo2[key])
        similarity = matches / len(common_keys)
        
        return similarity
    
    def _weighted_selection(self, weights: Dict[str, float]) -> str:
        """Selección ponderada basada en pesos"""
        if not weights:
            return "aleatorio"
        
        # Normalizar pesos
        total_weight = sum(weights.values())
        if total_weight == 0:
            return random.choice(list(weights.keys()))
        
        normalized_weights = {k: v / total_weight for k, v in weights.items()}
        
        # Selección aleatoria ponderada
        rand = random.random()
        cumulative = 0.0
        
        for option, weight in normalized_weights.items():
            cumulative += weight
            if rand <= cumulative:
                return option
        
        # Fallback
        return max(normalized_weights, key=normalized_weights.get)
    
    def get_balancing_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del balanceo"""
        stats = {
            "total_generations": len(self.generation_history),
            "characteristic_distribution": {},
            "repetition_violations": {},
            "diversity_scores": {},
            "recommendations": []
        }
        
        # Distribución de características
        for category in self.characteristic_weights:
            total_weight = sum(self.characteristic_weights[category].values())
            if total_weight > 0:
                stats["characteristic_distribution"][category] = {
                    option: weight / total_weight 
                    for option, weight in self.characteristic_weights[category].items()
                }
        
        # Violaciones de repetición
        for category, recent_values in self.repetition_tracker.items():
            if len(recent_values) >= self.config.max_repetitions:
                recent_counts = Counter(recent_values[-self.config.max_repetitions:])
                violations = {option: count for option, count in recent_counts.items() 
                           if count >= self.config.max_repetitions}
                if violations:
                    stats["repetition_violations"][category] = violations
        
        # Recomendaciones
        if stats["repetition_violations"]:
            stats["recommendations"].append("Considerar aumentar la diversidad en las opciones disponibles")
        
        if len(self.generation_history) > self.config.history_size:
            stats["recommendations"].append("El historial está lleno, considerando limpiar entradas antiguas")
        
        return stats
    
    def reset_balancing(self) -> None:
        """Resetea el sistema de balanceo"""
        self.generation_history.clear()
        self.characteristic_weights.clear()
        self.repetition_tracker.clear()
        self.diversity_scores.clear()
        self.logger.info("Sistema de balanceo reseteado")

# Instancia global del balanceador
intelligent_balancer = IntelligentBalancer()

def get_intelligent_balancer() -> IntelligentBalancer:
    """Obtiene la instancia global del balanceador inteligente"""
    return intelligent_balancer

def add_generation_to_balance(characteristics: Dict[str, str], image_id: str) -> None:
    """Añade una generación al sistema de balanceo"""
    intelligent_balancer.add_generation(characteristics, image_id)

def get_balanced_characteristics(available_options: Dict[str, List[str]], 
                               nationality: str, gender: str, age: int) -> Dict[str, str]:
    """Obtiene características balanceadas"""
    return intelligent_balancer.get_balanced_characteristics(
        available_options, nationality, gender, age
    )

def get_balancing_stats() -> Dict[str, Any]:
    """Obtiene estadísticas del balanceo"""
    return intelligent_balancer.get_balancing_statistics()
