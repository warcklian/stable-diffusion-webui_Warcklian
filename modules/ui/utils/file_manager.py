#!/usr/bin/env python3
"""
Gestor de Archivos Modular
Sistema modular para gestión de archivos y directorios
"""

import os
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import logging

@dataclass
class FileOperationResult:
    """Resultado de operación de archivo"""
    success: bool
    file_path: str = ""
    error_message: str = ""
    file_size: int = 0
    operation_time: float = 0.0

@dataclass
class DirectoryConfig:
    """Configuración de directorios"""
    base_output_dir: str = "outputs"
    temp_dir: str = "temp"
    backup_dir: str = "backups"
    templates_dir: str = "outputs/templates"
    metadata_dir: str = "outputs/metadata"
    create_subdirs: bool = True
    use_timestamps: bool = True

class FileManager:
    """Gestor de archivos para generación de imágenes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = DirectoryConfig()
        self.created_directories = set()
        
    def create_output_directories(self, model_name: str = "unknown_model", generation_type: str = "generation") -> Path:
        """
        Crea directorios de salida para la generación
        
        Args:
            model_name: Nombre del modelo
            generation_type: Tipo de generación (genetic, passport, etc.)
            
        Returns:
            Path: Directorio de salida creado
        """
        try:
            # Limpiar nombre del modelo
            model_name_clean = self._clean_filename(model_name)
            
            # Crear directorio base
            base_dir = Path(self.config.base_output_dir)
            base_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear subdirectorio del modelo
            model_dir = base_dir / model_name_clean
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear subdirectorio del tipo de generación
            if self.config.use_timestamps:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                generation_dir = model_dir / f"{generation_type}_{timestamp}"
            else:
                generation_dir = model_dir / generation_type
            
            generation_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear subdirectorios adicionales si está configurado
            if self.config.create_subdirs:
                subdirs = ["images", "metadata", "logs", "temp"]
                for subdir in subdirs:
                    (generation_dir / subdir).mkdir(exist_ok=True)
            
            # Registrar directorio creado
            self.created_directories.add(str(generation_dir))
            
            self.logger.info(f"Directorio de salida creado: {generation_dir}")
            return generation_dir
            
        except Exception as e:
            self.logger.error(f"Error creando directorios de salida: {e}")
            # Fallback a directorio por defecto
            fallback_dir = Path("outputs/generation")
            fallback_dir.mkdir(parents=True, exist_ok=True)
            return fallback_dir
    
    def save_image(self, image_data: Any, output_path: Path, filename: str, metadata: Dict[str, Any] = None) -> FileOperationResult:
        """
        Guarda una imagen en el directorio de salida
        
        Args:
            image_data: Datos de la imagen
            output_path: Directorio de salida
            filename: Nombre del archivo
            metadata: Metadatos adicionales
            
        Returns:
            FileOperationResult: Resultado de la operación
        """
        start_time = time.time()
        
        try:
            # Crear directorio de imágenes si no existe
            images_dir = output_path / "images"
            images_dir.mkdir(exist_ok=True)
            
            # Limpiar nombre del archivo
            clean_filename = self._clean_filename(filename)
            if not clean_filename.endswith(('.png', '.jpg', '.jpeg')):
                clean_filename += '.png'
            
            # Crear ruta completa del archivo
            file_path = images_dir / clean_filename
            
            # TODO: Implementar guardado real de imagen
            # Por ahora, crear archivo dummy para testing
            with open(file_path, 'w') as f:
                f.write(f"# Imagen generada: {clean_filename}\n")
                f.write(f"# Metadatos: {metadata or {}}\n")
                f.write(f"# Timestamp: {datetime.now().isoformat()}\n")
            
            # Guardar metadatos si se proporcionan
            if metadata:
                self.save_json_metadata(output_path, f"{clean_filename}_metadata", metadata)
            
            operation_time = time.time() - start_time
            file_size = file_path.stat().st_size if file_path.exists() else 0
            
            return FileOperationResult(
                success=True,
                file_path=str(file_path),
                file_size=file_size,
                operation_time=operation_time
            )
            
        except Exception as e:
            self.logger.error(f"Error guardando imagen: {e}")
            return FileOperationResult(
                success=False,
                error_message=f"Error guardando imagen: {str(e)}"
            )
    
    def save_json_metadata(self, output_path: Path, filename: str, metadata: Dict[str, Any]) -> FileOperationResult:
        """
        Guarda metadatos en formato JSON
        
        Args:
            output_path: Directorio de salida
            filename: Nombre del archivo
            metadata: Metadatos a guardar
            
        Returns:
            FileOperationResult: Resultado de la operación
        """
        start_time = time.time()
        
        try:
            # Crear directorio de metadatos si no existe
            metadata_dir = output_path / "metadata"
            metadata_dir.mkdir(exist_ok=True)
            
            # Limpiar nombre del archivo
            clean_filename = self._clean_filename(filename)
            if not clean_filename.endswith('.json'):
                clean_filename += '.json'
            
            # Crear ruta completa del archivo
            file_path = metadata_dir / clean_filename
            
            # Añadir metadatos de sistema
            metadata_with_system = {
                **metadata,
                "saved_at": datetime.now().isoformat(),
                "file_manager_version": "1.0.0",
                "system_info": {
                    "timestamp": time.time(),
                    "created_by": "FileManager"
                }
            }
            
            # Guardar JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_with_system, f, indent=2, ensure_ascii=False)
            
            operation_time = time.time() - start_time
            file_size = file_path.stat().st_size
            
            return FileOperationResult(
                success=True,
                file_path=str(file_path),
                file_size=file_size,
                operation_time=operation_time
            )
            
        except Exception as e:
            self.logger.error(f"Error guardando metadatos JSON: {e}")
            return FileOperationResult(
                success=False,
                error_message=f"Error guardando metadatos: {str(e)}"
            )
    
    def cleanup_temp_files(self, output_path: Path = None, max_age_hours: int = 24) -> FileOperationResult:
        """
        Limpia archivos temporales
        
        Args:
            output_path: Directorio específico a limpiar (None = todos)
            max_age_hours: Edad máxima en horas para archivos temporales
            
        Returns:
            FileOperationResult: Resultado de la operación
        """
        start_time = time.time()
        cleaned_files = 0
        total_size = 0
        
        try:
            if output_path:
                # Limpiar directorio específico
                directories_to_clean = [output_path]
            else:
                # Limpiar todos los directorios creados
                directories_to_clean = [Path(d) for d in self.created_directories]
            
            for directory in directories_to_clean:
                if not directory.exists():
                    continue
                
                # Limpiar archivos temporales
                temp_dir = directory / "temp"
                if temp_dir.exists():
                    for file_path in temp_dir.iterdir():
                        if file_path.is_file():
                            file_age = time.time() - file_path.stat().st_mtime
                            if file_age > (max_age_hours * 3600):
                                file_size = file_path.stat().st_size
                                file_path.unlink()
                                cleaned_files += 1
                                total_size += file_size
                                self.logger.info(f"Archivo temporal eliminado: {file_path}")
                
                # Limpiar archivos .tmp
                for file_path in directory.rglob("*.tmp"):
                    if file_path.is_file():
                        file_age = time.time() - file_path.stat().st_mtime
                        if file_age > (max_age_hours * 3600):
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            cleaned_files += 1
                            total_size += file_size
                            self.logger.info(f"Archivo temporal eliminado: {file_path}")
            
            operation_time = time.time() - start_time
            
            return FileOperationResult(
                success=True,
                file_path=f"cleaned_{cleaned_files}_files",
                file_size=total_size,
                operation_time=operation_time
            )
            
        except Exception as e:
            self.logger.error(f"Error limpiando archivos temporales: {e}")
            return FileOperationResult(
                success=False,
                error_message=f"Error limpiando archivos: {str(e)}"
            )
    
    def create_backup(self, source_path: Path, backup_name: str = None) -> FileOperationResult:
        """
        Crea una copia de seguridad de un directorio
        
        Args:
            source_path: Ruta del directorio a respaldar
            backup_name: Nombre del respaldo (opcional)
            
        Returns:
            FileOperationResult: Resultado de la operación
        """
        start_time = time.time()
        
        try:
            if not source_path.exists():
                return FileOperationResult(
                    success=False,
                    error_message=f"Directorio no existe: {source_path}"
                )
            
            # Crear directorio de respaldos
            backup_dir = Path(self.config.backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Generar nombre de respaldo
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}"
            
            backup_path = backup_dir / backup_name
            
            # Crear respaldo
            shutil.copytree(source_path, backup_path)
            
            operation_time = time.time() - start_time
            backup_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
            
            return FileOperationResult(
                success=True,
                file_path=str(backup_path),
                file_size=backup_size,
                operation_time=operation_time
            )
            
        except Exception as e:
            self.logger.error(f"Error creando respaldo: {e}")
            return FileOperationResult(
                success=False,
                error_message=f"Error creando respaldo: {str(e)}"
            )
    
    def get_directory_info(self, directory_path: Path) -> Dict[str, Any]:
        """
        Obtiene información de un directorio
        
        Args:
            directory_path: Ruta del directorio
            
        Returns:
            Dict[str, Any]: Información del directorio
        """
        try:
            if not directory_path.exists():
                return {"error": "Directorio no existe"}
            
            files = list(directory_path.rglob('*'))
            total_files = len([f for f in files if f.is_file()])
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            
            return {
                "path": str(directory_path),
                "total_files": total_files,
                "total_size": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "created_at": datetime.fromtimestamp(directory_path.stat().st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(directory_path.stat().st_mtime).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo información del directorio: {e}")
            return {"error": str(e)}
    
    def _clean_filename(self, filename: str) -> str:
        """Limpia un nombre de archivo para que sea seguro"""
        # Remover caracteres no seguros
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
        cleaned = "".join(c for c in filename if c in safe_chars)
        
        # Limitar longitud
        if len(cleaned) > 100:
            cleaned = cleaned[:100]
        
        # Asegurar que no esté vacío
        if not cleaned:
            cleaned = f"file_{int(time.time())}"
        
        return cleaned
    
    def configure(self, **kwargs) -> None:
        """Configura el gestor de archivos"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                
        self.logger.info(f"Configuración actualizada: {kwargs}")
    
    def get_config(self) -> DirectoryConfig:
        """Obtiene la configuración actual"""
        return self.config
    
    def reset(self) -> None:
        """Resetea el gestor de archivos"""
        self.created_directories.clear()
        self.config = DirectoryConfig()
        self.logger.info("Gestor de archivos reseteado")

# Instancia global del gestor de archivos
file_manager = FileManager()

def get_file_manager() -> FileManager:
    """Obtiene la instancia global del gestor de archivos"""
    return file_manager
