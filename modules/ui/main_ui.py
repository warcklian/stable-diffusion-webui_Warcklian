"""
Interfaz Principal Modular
Interfaz principal simplificada que integra todos los módulos
"""

import gradio as gr
import time
from typing import Optional, Any, Dict, List, Callable
from pathlib import Path
from dataclasses import dataclass, field
import logging

# Imports de módulos de optimización
try:
    from modules.ui.generation import GeneticGenerator, PassportGenerator, BatchProcessor, get_batch_processor
    from modules.ui.controls import get_genetic_controls, get_passport_controls, get_template_controls
    from modules.ui.validation import get_parameter_validator
    from modules.ui.utils import get_progress_manager, get_file_manager, get_error_handler
    from modules.ui.config import get_ui_config, get_generation_config
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False

@dataclass
class MainUIConfig:
    """Configuración de la interfaz principal"""
    title: str = "🧬 Sistema UI Modular"
    description: str = "Sistema modular para generación de imágenes genéticas y de pasaporte"
    theme: str = "default"
    analytics_enabled: bool = False
    show_progress: bool = True
    enable_batch_processing: bool = True
    enable_genetic_controls: bool = True
    enable_passport_controls: bool = True
    enable_template_controls: bool = True

@dataclass
class UIState:
    """Estado de la interfaz principal"""
    current_tab: str = "genetic"
    is_processing: bool = False
    batch_processing: bool = False
    last_update: str = ""
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    session_data: Dict[str, Any] = field(default_factory=dict)

class MainUI:
    """Interfaz principal modular"""
    
    def __init__(self, config: Optional[MainUIConfig] = None):
        self.config = config if config else MainUIConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ui_state = UIState()
        self.generators = {}
        self.controls = {}
        self.batch_processor = None
        self.progress_manager = None
        self.file_manager = None
        self.error_handler = None
        
        if OPTIMIZATION_MODULES_AVAILABLE:
            self._initialize_modules()
    
    def _initialize_modules(self):
        """Inicializa los módulos disponibles"""
        try:
            # Inicializar generadores
            self.generators = {
                "genetic": GeneticGenerator(),
                "passport": PassportGenerator()
            }
            
            # Inicializar controles
            self.controls = {
                "genetic": get_genetic_controls(),
                "passport": get_passport_controls(),
                "template": get_template_controls()
            }
            
            # Inicializar procesador de lotes
            self.batch_processor = get_batch_processor()
            
            # Inicializar utilidades
            self.progress_manager = get_progress_manager()
            self.file_manager = get_file_manager()
            self.error_handler = get_error_handler()
            
            self.logger.info("Módulos inicializados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error inicializando módulos: {e}")
    
    def create_main_ui(self) -> gr.Blocks:
        """Crea la interfaz principal modular"""
        try:
            with gr.Blocks(
                analytics_enabled=self.config.analytics_enabled,
                title=self.config.title,
                css=self._get_custom_css()
            ) as interface:
                
                # Crear interfaz principal
                self._create_header(interface)
                self._create_main_tabs(interface)
                self._create_footer(interface)
                
                # Configurar eventos
                self._setup_ui_events(interface)
                
            return interface
            
        except Exception as e:
            self.logger.error(f"Error creando interfaz principal: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "creating main UI"})
            raise
    
    def handle_ui_events(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja eventos de la interfaz principal"""
        try:
            if event_type == "tab_change":
                return self._handle_tab_change(data)
            elif event_type == "start_generation":
                return self._handle_start_generation(data)
            elif event_type == "cancel_generation":
                return self._handle_cancel_generation(data)
            elif event_type == "start_batch":
                return self._handle_start_batch(data)
            elif event_type == "get_ui_state":
                return self._handle_get_ui_state(data)
            else:
                return {"success": False, "error": f"Evento desconocido: {event_type}"}
                
        except Exception as e:
            self.logger.error(f"Error manejando evento de UI: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "handling UI event", "event_type": event_type})
            return {"success": False, "error": str(e)}
    
    def update_ui_state(self, updates: Dict[str, Any]) -> bool:
        """Actualiza el estado de la interfaz principal"""
        try:
            for key, value in updates.items():
                if hasattr(self.ui_state, key):
                    setattr(self.ui_state, key, value)
            
            self.ui_state.last_update = time.strftime("%Y-%m-%d %H:%M:%S")
            return True
            
        except Exception as e:
            self.logger.error(f"Error actualizando estado de UI: {e}")
            if self.error_handler:
                self.error_handler.log_error(e, {"context": "updating UI state"})
            return False
    
    def _create_header(self, interface: gr.Blocks):
        """Crea el encabezado de la interfaz"""
        with gr.Row():
            gr.Markdown(f"# {self.config.title}")
            gr.Markdown(f"## {self.config.description}")
    
    def _create_main_tabs(self, interface: gr.Blocks):
        """Crea las pestañas principales"""
        with gr.Tabs(elem_id="main_tabs") as tabs:
            
            # Pestaña de generación genética
            if self.config.enable_genetic_controls:
                with gr.TabItem("🧬 Generación Genética", id="genetic_tab"):
                    self._create_genetic_tab()
            
            # Pestaña de generación de pasaportes
            if self.config.enable_passport_controls:
                with gr.TabItem("🛂 Generación de Pasaportes", id="passport_tab"):
                    self._create_passport_tab()
            
            # Pestaña de procesamiento de lotes
            if self.config.enable_batch_processing:
                with gr.TabItem("📦 Procesamiento de Lotes", id="batch_tab"):
                    self._create_batch_tab()
            
            # Pestaña de plantillas
            if self.config.enable_template_controls:
                with gr.TabItem("📋 Plantillas", id="template_tab"):
                    self._create_template_tab()
    
    def _create_genetic_tab(self):
        """Crea la pestaña de generación genética"""
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🧬 Controles Genéticos")
                
                # Controles básicos
                with gr.Group():
                    gr.Markdown("#### Configuración Básica")
                    cantidad_genetic = gr.Slider(1, 100, value=10, label="Cantidad", info="Número de imágenes a generar")
                    edad_min_genetic = gr.Slider(18, 65, value=18, label="Edad Mínima")
                    edad_max_genetic = gr.Slider(18, 65, value=65, label="Edad Máxima")
                
                # Controles avanzados
                with gr.Group():
                    gr.Markdown("#### Configuración Avanzada")
                    nacionalidad_genetic = gr.Dropdown(
                        choices=["venezolana", "colombiana", "peruana", "ecuatoriana", "boliviana", "chilena", "argentina", "brasileña", "mexicana", "española", "italiana", "francesa", "alemana", "inglesa", "estadounidense", "canadiense", "australiana", "japonesa", "china", "coreana", "india", "árabe", "africana", "mixta"],
                        value="venezolana",
                        label="Nacionalidad"
                    )
                    genero_genetic = gr.Dropdown(
                        choices=["aleatorio", "masculino", "femenino"],
                        value="aleatorio",
                        label="Género"
                    )
                
                # Botones de control
                with gr.Row():
                    generar_genetic_btn = gr.Button("🧬 Generar Imágenes Genéticas", variant="primary")
                    cancelar_genetic_btn = gr.Button("❌ Cancelar", variant="stop")
            
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Progreso y Resultados")
                
                # Progreso
                progress_genetic = gr.Progress()
                status_genetic = gr.Textbox(label="Estado", interactive=False)
                
                # Resultados
                gallery_genetic = gr.Gallery(label="Imágenes Generadas", show_label=True, elem_id="gallery_genetic")
                
                # Información
                info_genetic = gr.Markdown("💡 **Generación Genética**: Crea imágenes con características genéticas diversas y realistas.")
    
    def _create_passport_tab(self):
        """Crea la pestaña de generación de pasaportes"""
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🛂 Controles de Pasaporte")
                
                # Controles básicos
                with gr.Group():
                    gr.Markdown("#### Configuración Básica")
                    cantidad_passport = gr.Slider(1, 100, value=10, label="Cantidad", info="Número de imágenes a generar")
                    nacionalidad_passport = gr.Dropdown(
                        choices=["venezolana", "colombiana", "peruana", "ecuatoriana", "boliviana", "chilena", "argentina", "brasileña", "mexicana", "española", "italiana", "francesa", "alemana", "inglesa", "estadounidense", "canadiense", "australiana", "japonesa", "china", "coreana", "india", "árabe", "africana", "mixta"],
                        value="venezolana",
                        label="Nacionalidad"
                    )
                    genero_passport = gr.Dropdown(
                        choices=["aleatorio", "masculino", "femenino"],
                        value="aleatorio",
                        label="Género"
                    )
                
                # Controles SAIME
                with gr.Group():
                    gr.Markdown("#### Configuración SAIME")
                    width_passport = gr.Slider(512, 512, value=512, label="Ancho (SAIME)", interactive=False)
                    height_passport = gr.Slider(768, 768, value=768, label="Alto (SAIME)", interactive=False)
                    cfg_scale_passport = gr.Slider(1.0, 20.0, value=7.0, label="CFG Scale")
                    steps_passport = gr.Slider(1, 150, value=20, label="Pasos")
                
                # Botones de control
                with gr.Row():
                    generar_passport_btn = gr.Button("🛂 Generar Pasaportes", variant="primary")
                    cancelar_passport_btn = gr.Button("❌ Cancelar", variant="stop")
            
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Progreso y Resultados")
                
                # Progreso
                progress_passport = gr.Progress()
                status_passport = gr.Textbox(label="Estado", interactive=False)
                
                # Resultados
                gallery_passport = gr.Gallery(label="Pasaportes Generados", show_label=True, elem_id="gallery_passport")
                
                # Información
                info_passport = gr.Markdown("💡 **Generación de Pasaportes**: Crea imágenes que cumplen estándares SAIME para documentos oficiales.")
    
    def _create_batch_tab(self):
        """Crea la pestaña de procesamiento de lotes"""
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📦 Procesamiento de Lotes")
                
                # Configuración de lote
                with gr.Group():
                    gr.Markdown("#### Configuración de Lote")
                    batch_size = gr.Slider(1, 10, value=1, label="Tamaño de Lote")
                    max_concurrent = gr.Slider(1, 5, value=1, label="Máximo Concurrente")
                    memory_optimization = gr.Checkbox(value=True, label="Optimización de Memoria")
                
                # Botones de control
                with gr.Row():
                    procesar_lote_btn = gr.Button("📦 Procesar Lote", variant="primary")
                    cancelar_lote_btn = gr.Button("❌ Cancelar", variant="stop")
            
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Progreso y Resultados")
                
                # Progreso
                progress_batch = gr.Progress()
                status_batch = gr.Textbox(label="Estado", interactive=False)
                
                # Resultados
                gallery_batch = gr.Gallery(label="Imágenes del Lote", show_label=True, elem_id="gallery_batch")
                
                # Información
                info_batch = gr.Markdown("💡 **Procesamiento de Lotes**: Procesa múltiples imágenes de forma eficiente y optimizada.")
    
    def _create_template_tab(self):
        """Crea la pestaña de plantillas"""
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📋 Gestión de Plantillas")
                
                # Selector de plantillas
                with gr.Group():
                    gr.Markdown("#### Plantillas Disponibles")
                    template_selector = gr.Dropdown(
                        choices=["Nueva Plantilla"],
                        value="Nueva Plantilla",
                        label="Seleccionar Plantilla"
                    )
                    
                    with gr.Row():
                        cargar_plantilla_btn = gr.Button("📂 Cargar", variant="secondary")
                        guardar_plantilla_btn = gr.Button("💾 Guardar", variant="primary")
                        eliminar_plantilla_btn = gr.Button("🗑️ Eliminar", variant="stop")
                
                # Editor de plantillas
                with gr.Group():
                    gr.Markdown("#### Editor de Plantillas")
                    template_name = gr.Textbox(label="Nombre de Plantilla", value="Nueva Plantilla")
                    template_description = gr.Textbox(label="Descripción", value="")
                    template_parameters = gr.Textbox(label="Parámetros (JSON)", value="{}", lines=10)
            
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Información de Plantillas")
                
                # Información
                info_template = gr.Markdown("💡 **Sistema de Plantillas**: Guarda y carga configuraciones personalizadas para diferentes tipos de generación.")
                
                # Estadísticas
                stats_template = gr.Markdown("📊 **Estadísticas**: No hay plantillas guardadas aún.")
    
    def _create_footer(self, interface: gr.Blocks):
        """Crea el pie de página de la interfaz"""
        with gr.Row():
            gr.Markdown("---")
            gr.Markdown("### 🔧 Sistema UI Modular - Versión 1.0")
            gr.Markdown("**Desarrollado con**: Python, Gradio, Stable Diffusion")
    
    def _get_custom_css(self) -> str:
        """Obtiene CSS personalizado para la interfaz"""
        return """
        /* Estilos personalizados para la interfaz modular */
        .genetic-tab {
            background-color: rgba(138, 43, 226, 0.1) !important;
        }
        
        .passport-tab {
            background-color: rgba(34, 139, 34, 0.1) !important;
        }
        
        .batch-tab {
            background-color: rgba(255, 165, 0, 0.1) !important;
        }
        
        .template-tab {
            background-color: rgba(70, 130, 180, 0.1) !important;
        }
        
        .gallery-container {
            border: 2px solid #ddd !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }
        """
    
    def _setup_ui_events(self, interface: gr.Blocks):
        """Configura los eventos de la interfaz"""
        # TODO: Implementar eventos de la interfaz
        pass
    
    def _handle_tab_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el cambio de pestaña"""
        try:
            new_tab = data.get("tab", "genetic")
            self.ui_state.current_tab = new_tab
            
            return {"success": True, "message": f"Pestaña cambiada a {new_tab}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_start_generation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el inicio de generación"""
        try:
            generation_type = data.get("type", "genetic")
            parameters = data.get("parameters", {})
            
            if generation_type not in self.generators:
                return {"success": False, "error": f"Tipo de generación no soportado: {generation_type}"}
            
            # Iniciar generación
            self.ui_state.is_processing = True
            
            return {"success": True, "message": f"Generación {generation_type} iniciada"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_cancel_generation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la cancelación de generación"""
        try:
            self.ui_state.is_processing = False
            
            return {"success": True, "message": "Generación cancelada"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_start_batch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el inicio de procesamiento de lote"""
        try:
            if not self.batch_processor:
                return {"success": False, "error": "Procesador de lotes no disponible"}
            
            items = data.get("items", [])
            if not items:
                return {"success": False, "error": "No hay elementos para procesar"}
            
            # Iniciar procesamiento de lote
            self.ui_state.batch_processing = True
            
            return {"success": True, "message": f"Procesamiento de lote iniciado con {len(items)} elementos"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _handle_get_ui_state(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la obtención del estado de la UI"""
        try:
            return {
                "success": True,
                "state": {
                    "current_tab": self.ui_state.current_tab,
                    "is_processing": self.ui_state.is_processing,
                    "batch_processing": self.ui_state.batch_processing,
                    "last_update": self.ui_state.last_update
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

def create_ui() -> gr.Blocks:
    """
    Crea la interfaz principal modular
    
    Returns:
        gr.Blocks: Interfaz principal de Gradio
    """
    try:
        # Importar la función create_ui original del sistema
        import sys
        import os
        
        # Agregar el directorio modules al path si no está
        modules_dir = os.path.join(os.path.dirname(__file__), '..')
        if modules_dir not in sys.path:
            sys.path.insert(0, modules_dir)
        
        # Importar la función create_ui original
        from modules.ui import create_ui as original_create_ui
        return original_create_ui()
        
    except Exception as e:
        # Fallback a interfaz básica en caso de error
        with gr.Blocks(analytics_enabled=False) as interface:
            gr.Markdown("# 🧬 Sistema UI Modular - Error")
            gr.Markdown(f"## Error creando interfaz: {str(e)}")
            gr.Markdown("### Interfaz básica de respaldo activada")
        
        return interface

def get_ui_info() -> Dict[str, Any]:
    """
    Obtiene información sobre la interfaz principal
    
    Returns:
        Dict[str, Any]: Información de la interfaz
    """
    return {
        "title": "Sistema UI Modular",
        "version": "1.0",
        "description": "Interfaz principal modular para generación de imágenes",
        "modules_available": OPTIMIZATION_MODULES_AVAILABLE,
        "features": [
            "Generación genética",
            "Generación de pasaportes",
            "Procesamiento de lotes",
            "Gestión de plantillas"
        ]
    }
