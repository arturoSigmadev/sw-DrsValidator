#!/usr/bin/env python3
"""
Script simplificado para crear versión compatible con Google Docs
"""
import re

def remove_mermaid_blocks(markdown_file, output_file):
    """Reemplaza bloques Mermaid con texto descriptivo"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Diccionario de reemplazos para cada diagrama
    replacements = {
        1: """
**Arquitectura General del Sistema:**
- Software de Validación (Nuestro) conecta via TCP/IP Puerto 65050
- Sistemas Independientes por Banda:
  - VHF: Master → Fibra Óptica → Remoto → LNA/PA (✅ Compatible)
  - P25: Master → Fibra Óptica → Remoto → LNA/PA (✅ Compatible) 
  - LC500: Master → Fibra Óptica → Remoto → LNA/PA (❌ No Compatible)
""",
        2: """
**Diagrama de Conectividad LNA/PA:**
- Software de Validación → TCP/IP Puerto 65050 → Master Digital Board (VHF/P25)
- Master Digital Board → Fibra Óptica → Remoto Digital Board
- Remoto Digital Board → Cable DB9↔IDC-10pin Puerto JP1 (pines 5,7) → LNA/PA
- PROBLEMA: Software nativo del remoto NO lee parámetros LNA/PA
""",
        3: """
**Diagrama de Incompatibilidad LC500:**
- Software de Validación → TCP/IP Puerto 65050 → Master Digital Board (LC500) ❌ No Compatible
- Master Digital Board → Fibra Óptica → Remoto Digital Board (LC500) ❌ No Compatible
- PROBLEMA: LC500 no soporta protocolo TCP Puerto 65050
""",
        4: """
**Diagrama de Estandarización de Versiones:**
- Estado Actual:
  - VHF: 231016-BB1-145-15M-16C-OP8 ✅ Funciona
  - P25: 231115-BB1-806D851M-18M-16C-OP8 ✅ Funciona
  - LC500: FPGA:250529-16A, Software:250530-05, Kernel:210909 ❌ No Compatible
- Objetivo: Versiones Unificadas para todas las tarjetas
"""
    }
    
    # Reemplazar cada bloque Mermaid
    pattern = r'```mermaid\n(.*?)\n```'
    replacement_count = 0
    
    def replacer(match):
        nonlocal replacement_count
        replacement_count += 1
        return replacements.get(replacement_count, "\n**[Diagrama no disponible]**\n")
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Archivo sin Mermaid creado: {output_file}")
    return output_file

def main():
    input_file = 'preguntas_conectividad_tarjetas_digitales.md'
    output_file = 'preguntas_conectividad_gdocs_compatible.md'
    
    # Crear versión sin Mermaid
    clean_file = remove_mermaid_blocks(input_file, output_file)
    
    # Convertir a DOCX
    import subprocess
    subprocess.run(['pandoc', clean_file, '-o', 
                   'preguntas_conectividad_gdocs_compatible.docx'],
                  check=True)
    
    print("✅ Archivo DOCX compatible con Google Docs creado!")
    print("📁 Archivo: preguntas_conectividad_gdocs_compatible.docx")
    print("\n🚀 Pasos siguientes:")
    print("1. Ve a drive.google.com")
    print("2. Arrastra el archivo .docx")
    print("3. Google Docs lo convertirá automáticamente")

if __name__ == '__main__':
    main()