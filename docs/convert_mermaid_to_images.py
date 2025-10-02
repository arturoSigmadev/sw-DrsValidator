#!/usr/bin/env python3
"""
Script para extraer diagramas Mermaid del markdown y convertirlos a imágenes
"""
import re
import os
import subprocess
import tempfile

def extract_mermaid_diagrams(markdown_file):
    """Extrae todos los diagramas Mermaid del archivo markdown"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para encontrar bloques de código Mermaid
    pattern = r'```mermaid\n(.*?)\n```'
    diagrams = re.findall(pattern, content, re.DOTALL)
    
    return diagrams, content

def convert_mermaid_to_image(mermaid_code, output_path):
    """Convierte código Mermaid a imagen usando mermaid-cli"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(mermaid_code)
        temp_file = f.name
    
    try:
        # Usar mmdc para convertir a PNG
        subprocess.run(['mmdc', '-i', temp_file, '-o', output_path], 
                      check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting diagram: {e}")
        return False
    finally:
        os.unlink(temp_file)

def replace_mermaid_with_images(content, image_paths):
    """Reemplaza bloques Mermaid con referencias a imágenes"""
    pattern = r'```mermaid\n(.*?)\n```'
    
    def replacer(match):
        if image_paths:
            img_path = image_paths.pop(0)
            return f'![Diagrama]({img_path})'
        return match.group(0)
    
    return re.sub(pattern, replacer, content, flags=re.DOTALL)

def main():
    markdown_file = 'preguntas_conectividad_tarjetas_digitales.md'
    output_dir = 'mermaid_images'
    
    # Crear directorio para imágenes
    os.makedirs(output_dir, exist_ok=True)
    
    # Extraer diagramas
    diagrams, content = extract_mermaid_diagrams(markdown_file)
    print(f"Encontrados {len(diagrams)} diagramas Mermaid")
    
    # Convertir cada diagrama a imagen
    image_paths = []
    for i, diagram in enumerate(diagrams):
        output_path = f'{output_dir}/diagram_{i+1}.png'
        if convert_mermaid_to_image(diagram, output_path):
            image_paths.append(output_path)
            print(f"Diagrama {i+1} convertido: {output_path}")
        else:
            print(f"Error convirtiendo diagrama {i+1}")
    
    # Crear nuevo markdown con imágenes
    new_content = replace_mermaid_with_images(content, image_paths.copy())
    
    # Guardar markdown modificado
    output_file = 'preguntas_conectividad_tarjetas_digitales_with_images.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Archivo modificado guardado: {output_file}")
    
    # Ahora convertir a DOCX
    subprocess.run(['pandoc', output_file, '-o', 
                   'preguntas_conectividad_tarjetas_digitales_final.docx'],
                  check=True)
    
    print("Conversión a DOCX completada: preguntas_conectividad_tarjetas_digitales_final.docx")

if __name__ == '__main__':
    main()