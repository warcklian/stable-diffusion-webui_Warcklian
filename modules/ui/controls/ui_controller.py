#!/usr/bin/env python3
"""
Controlador de UI Modular
Sistema modular para control de interfaz de usuario
"""

import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

class UIComponentType(Enum):
    """Tipo de componente de UI"""
    INPUT = "input"
    OUTPUT = "output"
    CONTROL = "control"
    DISPLAY = "display"
    INTERACTION = "interaction"
    DROPDOWN = "dropdown"
    SLIDER = "slider"
    CHECKBOX = "checkbox"
    TEXTBOX = "textbox"
    BUTTON = "button"
    MARKDOWN = "markdown"
    JSON = "json"

class UIEventType(Enum):
    """Tipo de evento de UI"""
    CLICK = "click"
    CHANGE = "change"
    SUBMIT = "submit"
    FOCUS = "focus"
    BLUR = "blur"
    HOVER = "hover"

@dataclass
class UIComponent:
    """Componente de UI"""
    id: str
    component_type: UIComponentType
    label: str
    value: Any = None
    visible: bool = True
    enabled: bool = True
    required: bool = False
    validation_rules: List[str] = field(default_factory=list)
    event_handlers: Dict[UIEventType, Callable] = field(default_factory=dict)

@dataclass
class UIEvent:
    """Evento de UI"""
    event_type: UIEventType
    component_id: str
    timestamp: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    user_id: str = ""

@dataclass
class UIState:
    """Estado de UI"""
    components: Dict[str, UIComponent] = field(default_factory=dict)
    current_tab: str = ""
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    session_data: Dict[str, Any] = field(default_factory=dict)
    last_updated: str = ""

class UIController:
    """Controlador de interfaz de usuario"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.state = UIState()
        self.event_queue: List[UIEvent] = []
        self.component_registry: Dict[str, UIComponent] = {}
        self.event_handlers: Dict[str, Callable] = {}
        
    def create_ui_components(self, component_configs: List[Dict[str, Any]]) -> Dict[str, UIComponent]:
        """
        Crea componentes de UI basados en configuraciones
        
        Args:
            component_configs: Lista de configuraciones de componentes
            
        Returns:
            Dict[str, UIComponent]: Componentes creados
        """
        try:
            created_components = {}
            
            for config in component_configs:
                component_id = config.get("id")
                if not component_id:
                    self.logger.warning("Componente sin ID, saltando...")
                    continue
                
                # Crear componente
                component = UIComponent(
                    id=component_id,
                    component_type=UIComponentType(config.get("type", "input")),
                    label=config.get("label", ""),
                    value=config.get("value"),
                    visible=config.get("visible", True),
                    enabled=config.get("enabled", True),
                    required=config.get("required", False),
                    validation_rules=config.get("validation_rules", []),
                    event_handlers=config.get("event_handlers", {})
                )
                
                # Registrar componente
                self.component_registry[component_id] = component
                self.state.components[component_id] = component
                created_components[component_id] = component
                
                self.logger.info(f"Componente creado: {component_id}")
            
            self.state.last_updated = datetime.now().isoformat()
            return created_components
            
        except Exception as e:
            self.logger.error(f"Error creando componentes de UI: {e}")
            return {}
    
    def handle_event(self, event: UIEvent) -> Dict[str, Any]:
        """Procesa un evento de UI, invocando a los manejadores registrados."""
        try:
            self.logger.info(f"Evento recibido: {event.event_type.value} para {event.component_id} con valor {event.new_value}")
            
            # Obtener componente
            component = self.component_registry.get(event.component_id)
            if not component:
                return {"success": False, "error": f"Componente no encontrado: {event.component_id}"}
            
            # Obtener manejador de evento
            event_handler = component.event_handlers.get(event.event_type)
            if not event_handler:
                return {"success": False, "error": f"No hay manejador para evento {event.event_type.value}"}
            
            # Ejecutar manejador
            result = event_handler(event)
            return {"success": True, "result": result}
            
        except Exception as e:
            self.logger.error(f"Error manejando evento: {e}")
            return {"success": False, "error": str(e)}
    
    def handle_ui_events(self, event: UIEvent) -> Dict[str, Any]:
        """
        Maneja eventos de UI
        
        Args:
            event: Evento de UI a manejar
            
        Returns:
            Dict[str, Any]: Resultado del manejo del evento
        """
        try:
            # Agregar timestamp si no existe
            if not event.timestamp:
                event.timestamp = datetime.now().isoformat()
            
            # Agregar a cola de eventos
            self.event_queue.append(event)
            
            # Obtener componente
            component = self.component_registry.get(event.component_id)
            if not component:
                return {"success": False, "error": f"Componente no encontrado: {event.component_id}"}
            
            # Obtener manejador de evento
            event_handler = component.event_handlers.get(event.event_type)
            if not event_handler:
                return {"success": False, "error": f"No hay manejador para evento {event.event_type.value}"}
            
            # Ejecutar manejador
            result = event_handler(event.data)
            
            # Actualizar estado
            self._update_component_state(event.component_id, event.data)
            
            self.logger.info(f"Evento manejado: {event.event_type.value} en {event.component_id}")
            return {"success": True, "result": result}
            
        except Exception as e:
            self.logger.error(f"Error manejando evento de UI: {e}")
            return {"success": False, "error": str(e)}
    
    def update_ui_state(self, component_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualiza el estado de un componente de UI
        
        Args:
            component_id: ID del componente
            updates: Actualizaciones a aplicar
            
        Returns:
            bool: True si la actualización fue exitosa
        """
        try:
            component = self.component_registry.get(component_id)
            if not component:
                self.logger.warning(f"Componente no encontrado: {component_id}")
                return False
            
            # Aplicar actualizaciones
            for key, value in updates.items():
                if hasattr(component, key):
                    setattr(component, key, value)
                else:
                    self.logger.warning(f"Atributo no válido: {key}")
            
            # Actualizar timestamp
            self.state.last_updated = datetime.now().isoformat()
            
            self.logger.info(f"Estado actualizado para componente: {component_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error actualizando estado de UI: {e}")
            return False
    
    def validate_ui_inputs(self, component_ids: List[str] = None) -> Dict[str, Any]:
        """
        Valida entradas de UI
        
        Args:
            component_ids: Lista de IDs de componentes a validar (None = todos)
            
        Returns:
            Dict[str, Any]: Resultado de la validación
        """
        try:
            validation_results = {}
            all_valid = True
            
            # Determinar componentes a validar
            if component_ids:
                components_to_validate = [self.component_registry.get(cid) for cid in component_ids if self.component_registry.get(cid)]
            else:
                components_to_validate = list(self.component_registry.values())
            
            for component in components_to_validate:
                if not component:
                    continue
                
                component_result = self._validate_component(component)
                validation_results[component.id] = component_result
                
                if not component_result["valid"]:
                    all_valid = False
            
            return {
                "valid": all_valid,
                "results": validation_results,
                "total_components": len(components_to_validate),
                "valid_components": len([r for r in validation_results.values() if r["valid"]]),
                "invalid_components": len([r for r in validation_results.values() if not r["valid"]])
            }
            
        except Exception as e:
            self.logger.error(f"Error validando entradas de UI: {e}")
            return {"valid": False, "error": str(e)}
    
    def get_ui_state(self) -> UIState:
        """Obtiene el estado actual de la UI"""
        return self.state
    
    def get_component(self, component_id: str) -> Optional[UIComponent]:
        """Obtiene un componente por ID"""
        return self.component_registry.get(component_id)
    
    def get_components_by_type(self, component_type: UIComponentType) -> List[UIComponent]:
        """Obtiene componentes por tipo"""
        return [comp for comp in self.component_registry.values() if comp.component_type == component_type]
    
    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """Registra un manejador de evento global"""
        self.event_handlers[event_type] = handler
        self.logger.info(f"Manejador de evento registrado: {event_type}")
    
    def unregister_event_handler(self, event_type: str) -> None:
        """Desregistra un manejador de evento global"""
        if event_type in self.event_handlers:
            del self.event_handlers[event_type]
            self.logger.info(f"Manejador de evento desregistrado: {event_type}")
    
    def clear_event_queue(self) -> None:
        """Limpia la cola de eventos"""
        self.event_queue.clear()
        self.logger.info("Cola de eventos limpiada")
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de eventos"""
        try:
            if not self.event_queue:
                return {"total_events": 0, "message": "No hay eventos registrados"}
            
            # Contar por tipo
            event_types = {}
            for event in self.event_queue:
                event_type = event.event_type.value
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Eventos recientes (últimas 24 horas)
            recent_events = [
                event for event in self.event_queue
                if (datetime.now() - datetime.fromisoformat(event.timestamp)).total_seconds() < 86400
            ]
            
            return {
                "total_events": len(self.event_queue),
                "recent_events": len(recent_events),
                "event_types": event_types,
                "components_with_events": len(set(event.component_id for event in self.event_queue))
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas de eventos: {e}")
            return {"error": str(e)}
    
    def reset_ui_state(self) -> None:
        """Resetea el estado de la UI"""
        self.state = UIState()
        self.component_registry.clear()
        self.event_queue.clear()
        self.event_handlers.clear()
        self.logger.info("Estado de UI reseteado")
    
    def _validate_component(self, component: UIComponent) -> Dict[str, Any]:
        """Valida un componente individual"""
        try:
            validation_errors = []
            
            # Validar valor requerido
            if component.required and (component.value is None or component.value == ""):
                validation_errors.append("Campo requerido")
            
            # Aplicar reglas de validación personalizadas
            for rule in component.validation_rules:
                if not self._apply_validation_rule(component, rule):
                    validation_errors.append(f"Regla de validación falló: {rule}")
            
            return {
                "valid": len(validation_errors) == 0,
                "errors": validation_errors,
                "component_id": component.id,
                "component_type": component.component_type.value
            }
            
        except Exception as e:
            self.logger.error(f"Error validando componente {component.id}: {e}")
            return {
                "valid": False,
                "errors": [f"Error de validación: {str(e)}"],
                "component_id": component.id,
                "component_type": component.component_type.value
            }
    
    def _apply_validation_rule(self, component: UIComponent, rule: str) -> bool:
        """Aplica una regla de validación específica"""
        try:
            if rule == "not_empty":
                return component.value is not None and str(component.value).strip() != ""
            elif rule == "numeric":
                return str(component.value).replace(".", "").replace("-", "").isdigit()
            elif rule == "positive":
                return float(component.value) > 0
            elif rule == "email":
                return "@" in str(component.value) and "." in str(component.value)
            elif rule.startswith("min_length:"):
                min_length = int(rule.split(":")[1])
                return len(str(component.value)) >= min_length
            elif rule.startswith("max_length:"):
                max_length = int(rule.split(":")[1])
                return len(str(component.value)) <= max_length
            else:
                self.logger.warning(f"Regla de validación no reconocida: {rule}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error aplicando regla de validación {rule}: {e}")
            return False
    
    def _update_component_state(self, component_id: str, data: Dict[str, Any]) -> None:
        """Actualiza el estado de un componente basado en datos de evento"""
        try:
            component = self.component_registry.get(component_id)
            if not component:
                return
            
            # Actualizar valor si está en los datos
            if "value" in data:
                component.value = data["value"]
            
            # Actualizar visibilidad si está en los datos
            if "visible" in data:
                component.visible = data["visible"]
            
            # Actualizar habilitación si está en los datos
            if "enabled" in data:
                component.enabled = data["enabled"]
            
            # Actualizar timestamp
            self.state.last_updated = datetime.now().isoformat()
            
        except Exception as e:
            self.logger.error(f"Error actualizando estado del componente {component_id}: {e}")

# Instancia global del controlador de UI
ui_controller = UIController()

def get_ui_controller() -> UIController:
    """Obtiene la instancia global del controlador de UI"""
    return ui_controller

def create_ui_event(event_type: UIEventType, component_id: str, data: Dict[str, Any] = None) -> UIEvent:
    """Función de conveniencia para crear eventos de UI"""
    return UIEvent(
        event_type=event_type,
        component_id=component_id,
        timestamp=datetime.now().isoformat(),
        data=data or {},
        user_id="default"
    )
