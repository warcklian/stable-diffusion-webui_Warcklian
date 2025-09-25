#!/bin/bash

echo "🔧 RESTAURANDO PROYECTO COMPLETO DE STABLE-DIFFUSION-WEBUI"
echo "=========================================================="

# Crear respaldo del estado actual
echo "📦 Creando respaldo del estado actual..."
cp -r /media/warcklian/DATA_500GB/CODE/stable-diffusion-webui /media/warcklian/DATA_500GB/CODE/stable-diffusion-webui_incompleto_$(date +%Y%m%d_%H%M%S)

# Crear directorio temporal para descargar el proyecto completo
echo "📥 Descargando proyecto completo..."
cd /media/warcklian/DATA_500GB/CODE/
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git stable-diffusion-webui-completo

# Copiar archivos de configuración existentes
echo "📋 Preservando archivos de configuración existentes..."
if [ -f "stable-diffusion-webui/Consulta/ultra_diversity_engine.py" ]; then
    cp -r stable-diffusion-webui/Consulta stable-diffusion-webui-completo/
    echo "✅ Consulta/ preservado"
fi

if [ -f "stable-diffusion-webui/modules/ui.py" ]; then
    cp stable-diffusion-webui/modules/ui.py stable-diffusion-webui-completo/modules/ui.py
    echo "✅ modules/ui.py preservado"
fi

if [ -f "stable-diffusion-webui/plan_integracion_saime_avanzado.md" ]; then
    cp stable-diffusion-webui/plan_integracion_saime_avanzado.md stable-diffusion-webui-completo/
    echo "✅ plan_integracion_saime_avanzado.md preservado"
fi

if [ -f "stable-diffusion-webui/resumen_integracion_completada.md" ]; then
    cp stable-diffusion-webui/resumen_integracion_completada.md stable-diffusion-webui-completo/
    echo "✅ resumen_integracion_completada.md preservado"
fi

# Reemplazar el directorio incompleto con el completo
echo "🔄 Reemplazando directorio incompleto con el completo..."
rm -rf stable-diffusion-webui
mv stable-diffusion-webui-completo stable-diffusion-webui

echo "✅ Proyecto completo restaurado"
echo "📁 Archivos preservados:"
echo "   - Consulta/ (motor de diversidad)"
echo "   - modules/ui.py (controles mejorados)"
echo "   - Documentación de integración"

echo ""
echo "🚀 Ahora puedes ejecutar:"
echo "   cd /media/warcklian/DATA_500GB/CODE/stable-diffusion-webui"
echo "   ./webui.sh"
