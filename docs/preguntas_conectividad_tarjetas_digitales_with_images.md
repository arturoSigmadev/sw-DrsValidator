# Preguntas Técnicas: Conectividad Tarjetas Digitales VHF, P25 y LC500

## Contexto del Sistema

### Arquitectura
```mermaid
flowchart TD
    A["Software de Validación<br/>(Nuestro)"] 
    
    subgraph "Sistemas Independientes por Banda"
        B1["Master Digital Board<br/>(VHF)"]
        B2["Master Digital Board<br/>(P25)"]
        B3["Master Digital Board<br/>(LC500)"]
        
        C1["Remoto Digital Board<br/>(VHF)"]
        C2["Remoto Digital Board<br/>(P25)"]
        C3["Remoto Digital Board<br/>(LC500)"]
        
        D1["LNA / PA<br/>(VHF)"]
        D2["LNA / PA<br/>(P25)"]
        D3["LNA / PA<br/>(LC500)"]
    end
    
    A -.->|"TCP/IP Puerto 65050"| B1
    A -.->|"TCP/IP Puerto 65050"| B2
    A -.->|"TCP/IP Puerto 65050"| B3
    
    B1 -.->|"Fibra Óptica"| C1
    B2 -.->|"Fibra Óptica"| C2
    B3 -.->|"Fibra Óptica"| C3
    
    C1 -.->|"DB9↔IDC-10pin JP1"| D1
    C2 -.->|"DB9↔IDC-10pin JP1"| D2
    C3 -.->|"DB9↔IDC-10pin JP1"| D3
    
    style A fill:#e1f5fe,color:#000
    style B1 fill:#e8f5e8,color:#000
    style B2 fill:#e8f5e8,color:#000
    style B3 fill:#ffebee,color:#000
    style C1 fill:#e8f5e8,color:#000
    style C2 fill:#e8f5e8,color:#000
    style C3 fill:#ffebee,color:#000
    style D1 fill:#fff3e0,color:#000
    style D2 fill:#fff3e0,color:#000
    style D3 fill:#ffebee,color:#000
    
    classDef working stroke:#4caf50,stroke-width:2px,color:#000
    classDef problem stroke:#f44336,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    class B1,C1 working
    class B2,C2 working
    class B3,C3,D3 problem
```

**NOTA**: Cada banda (VHF, P25, LC500) tiene su propio Master Digital Board y funciona como sistema independiente

### Versiones de Software
- **VHF**: 231016-BB1-145-15M-16C-OP8 ✅ Compatible TCP
- **P25**: 231115-BB1-806D851M-18M-16C-OP8 ✅ Compatible TCP  
- **LC500**: FPGA:250529-16A, Software:250530-05, Kernel:210909 ❌ No compatible TCP

### Componentes LNA/PA
- **Conexión**: Puerto JP1 pines 5,7 via cable DB9↔IDC-10pin
- **Problema**: Software nativo del remoto NO lee parámetros LNA/PA
- **Objetivo**: Monitoreo integrado via TCP/IP

---

## Preguntas Técnicas

### 1. Monitoreo LNA/PA

**Arquitectura del Problema:**
```mermaid
flowchart TD
    A["Software de Validación<br/>(Nuestro)"] 
    B["Master Digital Board<br/>(VHF/P25)"]
    C["Remoto Digital Board<br/>(VHF/P25)"]
    D["LNA / PA"]
    
    A -.->|"TCP/IP<br/>Puerto 65050"| B
    B -.->|"Fibra Óptica"| C
    C -.->|"Cable DB9↔IDC-10pin<br/>Puerto JP1 (pines 5,7)"| D
    
    style A fill:#e1f5fe,color:#000
    style B fill:#f3e5f5,color:#000
    style C fill:#fff3e0,color:#000
    style D fill:#ffebee,color:#000
    
    classDef problem stroke:#f44336,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    class D problem
```

**PROBLEMA**: Software nativo del remoto NO lee parámetros LNA/PA  
**OBJETIVO**: Monitoreo integrado via TCP/IP

**Preguntas:**
- ¿Existen comandos específicos en "Protocol _TT_2023_8_30.pdf" para LNA y PA?
- ¿Se puede usar puerto 65050 para monitorear LNA/PA?
- ¿Por qué el software nativo del remoto no lee parámetros LNA via DB9-IDC 10pin?
- ¿Es posible transportar comandos LNA/PA a través de: Master → Fibra → Remoto → TCP/IP?
- ¿Se requiere configuración especial en master/remoto para habilitar comunicación LNA/PA?
- ¿Los archivos .rar VHF/P25 incluyen comandos de monitoreo para LNA/PA?

### 2. Compatibilidad LC500

**Arquitectura del Problema:**
```mermaid
flowchart TD
    A["Software de Validación<br/>(Nuestro)"] 
    B["Master Digital Board<br/>(LC500)"]
    C["Remoto Digital Board<br/>(LC500)"]
    
    A -.->|"TCP/IP Puerto 65050<br/>❌ No Compatible"| B
    B -.->|"Fibra Óptica"| C
    
    style A fill:#e1f5fe,color:#000
    style B fill:#ffebee,color:#000
    style C fill:#ffebee,color:#000
    
    classDef incompatible stroke:#f44336,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    class B,C incompatible
```

**PROBLEMA**: LC500 no soporta protocolo TCP Puerto 65050  
**OBJETIVO**: Hacer LC500 compatible con sistema de monitoreo

**Preguntas:**
- ¿LC500 soporta los mismos comandos TCP que VHF/P25 via fibra óptica?
- ¿Es compatible con puerto 65050 en master digital board?
- ¿Qué modificaciones requiere LC500 para compatibilidad TCP?
- ¿Hay que actualizar LC500 a versiones compatibles con VHF/P25?

### 3. Estandarización

**Arquitectura de Versiones:**
```mermaid
flowchart TD
    A["Software de Validación<br/>(Sistema Unificado)"]
    
    subgraph "Versiones Actuales"
        V1["VHF<br/>231016-BB1-145-15M-16C-OP8<br/>✅ Funciona"]
        V2["P25<br/>231115-BB1-806D851M-18M-16C-OP8<br/>✅ Funciona"]
        V3["LC500<br/>FPGA: 250529-16A<br/>Software: 250530-05<br/>Kernel: 210909<br/>❌ No Compatible"]
    end
    
    subgraph "Objetivo: Versiones Unificadas"
        U1["VHF Estandarizado<br/>Versión Compatible"]
        U2["P25 Estandarizado<br/>Versión Compatible"]
        U3["LC500 Actualizado<br/>Versión Compatible"]
    end
    
    A -.-> V1
    A -.-> V2
    A -.-> V3
    
    V1 --> U1
    V2 --> U2
    V3 --> U3
    
    style A fill:#e1f5fe,color:#000
    style V1 fill:#e8f5e8,color:#000
    style V2 fill:#e8f5e8,color:#000
    style V3 fill:#ffebee,color:#000
    style U1 fill:#f0f4c3,color:#000
    style U2 fill:#f0f4c3,color:#000
    style U3 fill:#f0f4c3,color:#000
    
    classDef working stroke:#4caf50,stroke-width:2px,color:#000
    classDef broken stroke:#f44336,stroke-width:2px,color:#000
    classDef target stroke:#ff9800,stroke-width:2px,stroke-dasharray: 3 3,color:#000
    class V1,V2 working
    class V3 broken
    class U1,U2,U3 target
```

**PROBLEMA**: Diferentes versiones complican mantenimiento y compatibilidad  
**OBJETIVO**: Estandarizar versiones para monitoreo unificado

**Preguntas:**
- ¿Es posible usar las mismas versiones VHF/P25 en todas las tarjetas?
- ¿Mejoraría esto la compatibilidad del monitoreo TCP?
- ¿Hay implicaciones técnicas en estandarizar versiones?

## Comandos de Monitoreo Requeridos (13 comandos TCP)
- `temperature` (0x02), `device_id` (0x97), `datt` (0x09)
- `input_and_output_power` (0xF3), `channel_switch` (0x42)
- `channel_frequency_configuration` (0x36), `central_frequency_point` (0xEB)
- `subband_bandwidth` (0xED), `broadband_switching` (0x81)
- `optical_port_switch` (0x91), `optical_port_status` (0x9A)
- `optical_port_devices_connected_1` (0xF8), `optical_port_devices_connected_2` (0xF9)

## Archivos de Referencia
- `Protocol _TT_2023_8_30.pdf` ✅ Protocolo principal (funciona)
- `Santone module monitor protocol_2023_8_15.pdf` ❌ No funciona
- `VHF - 231016-BB1-145-15M-16C-OP8.rar`, `P25 - 231115-BB1-806D851M-18M-16C-OP8.rar`
- `LNA_VHF_Technical Specification (1).pdf`

---
*Versión: 2.2 - Diagramas Mermaid por pregunta*</content>
<parameter name="filePath">/home/arturo/sw-drsmonitoring/validation-framework/docs/preguntas_conectividad_tarjetas_digitales.md