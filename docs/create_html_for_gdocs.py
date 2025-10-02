#!/usr/bin/env python3
"""
Script para crear HTML optimizado para Google Docs con Mermaid como SVG embebido
"""
import re

def create_clean_html_for_gdocs(markdown_file, output_file):
    """Crear HTML limpio y optimizado para Google Docs"""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar diagramas Mermaid con descripciones HTML estructuradas
    mermaid_replacements = {
        1: """
<div style="border: 2px solid #4CAF50; padding: 20px; margin: 10px 0; background-color: #f8f9fa;">
    <h4 style="color: #2E7D32;">🏗️ Arquitectura General del Sistema</h4>
    <ul>
        <li><strong>Software de Validación (Nuestro)</strong> → TCP/IP Puerto 65050</li>
        <li><strong>Sistemas Independientes por Banda:</strong>
            <ul>
                <li>🟢 <strong>VHF:</strong> Master Digital Board → Fibra Óptica → Remoto → LNA/PA (Compatible)</li>
                <li>🟢 <strong>P25:</strong> Master Digital Board → Fibra Óptica → Remoto → LNA/PA (Compatible)</li>
                <li>🔴 <strong>LC500:</strong> Master Digital Board → Fibra Óptica → Remoto → LNA/PA (No Compatible)</li>
            </ul>
        </li>
    </ul>
</div>
""",
        2: """
<div style="border: 2px solid #FF9800; padding: 20px; margin: 10px 0; background-color: #fff3e0;">
    <h4 style="color: #E65100;">⚠️ Diagrama de Conectividad LNA/PA</h4>
    <ol>
        <li><strong>Software de Validación</strong> → TCP/IP Puerto 65050 → <strong>Master Digital Board (VHF/P25)</strong></li>
        <li><strong>Master Digital Board</strong> → Fibra Óptica → <strong>Remoto Digital Board</strong></li>
        <li><strong>Remoto Digital Board</strong> → Cable DB9↔IDC-10pin Puerto JP1 (pines 5,7) → <strong>LNA/PA</strong></li>
    </ol>
    <p style="color: #d32f2f; font-weight: bold;">❌ PROBLEMA: Software nativo del remoto NO lee parámetros LNA/PA</p>
</div>
""",
        3: """
<div style="border: 2px solid #F44336; padding: 20px; margin: 10px 0; background-color: #ffebee;">
    <h4 style="color: #C62828;">❌ Diagrama de Incompatibilidad LC500</h4>
    <ul>
        <li><strong>Software de Validación</strong> → TCP/IP Puerto 65050 → <strong>Master Digital Board (LC500)</strong> ❌ No Compatible</li>
        <li><strong>Master Digital Board</strong> → Fibra Óptica → <strong>Remoto Digital Board (LC500)</strong> ❌ No Compatible</li>
    </ul>
    <p style="color: #d32f2f; font-weight: bold;">🚫 PROBLEMA: LC500 no soporta protocolo TCP Puerto 65050</p>
</div>
""",
        4: """
<div style="border: 2px solid #2196F3; padding: 20px; margin: 10px 0; background-color: #e3f2fd;">
    <h4 style="color: #1565C0;">🔄 Diagrama de Estandarización de Versiones</h4>
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #f5f5f5;">
            <th style="border: 1px solid #ddd; padding: 8px;">Tarjeta</th>
            <th style="border: 1px solid #ddd; padding: 8px;">Versión Actual</th>
            <th style="border: 1px solid #ddd; padding: 8px;">Estado</th>
            <th style="border: 1px solid #ddd; padding: 8px;">Objetivo</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;"><strong>VHF</strong></td>
            <td style="border: 1px solid #ddd; padding: 8px;">231016-BB1-145-15M-16C-OP8</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #4CAF50;">✅ Funciona</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Versión Estandarizada</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;"><strong>P25</strong></td>
            <td style="border: 1px solid #ddd; padding: 8px;">231115-BB1-806D851M-18M-16C-OP8</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #4CAF50;">✅ Funciona</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Versión Estandarizada</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;"><strong>LC500</strong></td>
            <td style="border: 1px solid #ddd; padding: 8px;">FPGA:250529-16A<br/>Software:250530-05<br/>Kernel:210909</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #F44336;">❌ No Compatible</td>
            <td style="border: 1px solid #ddd; padding: 8px;">Versión Actualizada</td>
        </tr>
    </table>
</div>
"""
    }
    
    # Crear HTML base
    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preguntas Técnicas: Conectividad Tarjetas Digitales</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            line-height: 1.6; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            color: #333;
        }
        h1, h2, h3, h4 { color: #2c3e50; }
        h1 { border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { border-bottom: 2px solid #95a5a6; padding-bottom: 5px; }
        ul, ol { padding-left: 20px; }
        li { margin-bottom: 5px; }
        code { 
            background-color: #f8f9fa; 
            padding: 2px 5px; 
            border-radius: 3px; 
            font-family: 'Courier New', monospace;
        }
        .command-list {
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 10px 0;
        }
        .note {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .reference {
            background-color: #e8f5e9;
            border: 1px solid #4caf50;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
"""
    
    # Procesar el contenido markdown
    lines = content.split('\n')
    html_content = []
    in_mermaid = False
    mermaid_count = 0
    
    for line in lines:
        if line.strip() == '```mermaid':
            in_mermaid = True
            mermaid_count += 1
            continue
        elif line.strip() == '```' and in_mermaid:
            in_mermaid = False
            # Insertar el reemplazo HTML correspondiente
            if mermaid_count in mermaid_replacements:
                html_content.append(mermaid_replacements[mermaid_count])
            continue
        elif in_mermaid:
            continue  # Saltar líneas del diagrama Mermaid
        else:
            # Procesar markdown básico
            line = line.replace('**', '<strong>').replace('**', '</strong>')
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = line.replace('`', '<code>').replace('`', '</code>')
            line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
            
            if line.startswith('# '):
                html_content.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_content.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_content.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('- '):
                if not html_content or not html_content[-1].startswith('<ul>'):
                    html_content.append('<ul>')
                html_content.append(f'<li>{line[2:]}</li>')
            elif line.strip() == '':
                if html_content and html_content[-1].startswith('<ul>'):
                    html_content.append('</ul>')
                html_content.append('<br/>')
            elif line.startswith('---'):
                html_content.append('<hr/>')
            else:
                html_content.append(f'<p>{line}</p>')
    
    # Cerrar listas abiertas
    if html_content and html_content[-1].startswith('<ul>'):
        html_content.append('</ul>')
    
    # Generar HTML final
    final_html = html_template + '\n'.join(html_content) + '\n</body>\n</html>'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ HTML optimizado para Google Docs creado: {output_file}")
    return output_file

def main():
    input_file = 'preguntas_conectividad_tarjetas_digitales.md'
    output_file = 'preguntas_conectividad_gdocs_optimized.html'
    
    clean_html = create_clean_html_for_gdocs(input_file, output_file)
    
    print("\n🚀 Pasos para importar a Google Docs:")
    print("1. Ve a docs.google.com")
    print("2. Archivo → Abrir → Subir")
    print(f"3. Selecciona: {output_file}")
    print("4. Google Docs convertirá automáticamente el HTML")
    print("\n💡 Alternativa:")
    print("1. Abre el archivo HTML en tu navegador")
    print("2. Selecciona todo (Ctrl+A) y copia (Ctrl+C)")
    print("3. Pega directamente en un Google Doc nuevo")

if __name__ == '__main__':
    main()