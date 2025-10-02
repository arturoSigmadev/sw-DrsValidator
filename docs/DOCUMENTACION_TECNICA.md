# 🔧 Documentación Técnica - DRS Validation Framework

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
DRS Validation Framework
├── 🌐 validation_app.py          # API FastAPI (puerto 8080)
├── 🔧 validation/
│   ├── standalone_validator.py   # Lógica de validación TCP
│   └── batch_commands_validator.py # Validación comandos DRS
├── 📋 config/
│   └── validation_scenarios.yaml # Configuración dispositivos
├── 🌐 web/                       # Interfaz web
│   ├── index.html               # UI principal
│   ├── style.css                # Estilos
│   └── app.js                   # JavaScript frontend
└── 🐳 Docker                    # Contenedor con herramientas de red
```

### Flujo de Validación

1. **Usuario** → Web Interface (index.html)
2. **Frontend** → API Call (/api/validation/run)
3. **FastAPI** → Standalone Validator
4. **Validator** → Tests: Ping + TCP + Commands
5. **Resultado** → JSON Response → UI Update

---

## 📄 API Endpoints

### Validación Básica
```http
POST /api/validation/run
Content-Type: application/json

{
  "scenario_id": "dmu_basic_check",
  "ip_address": "192.168.11.22",
  "hostname": "dmu",
  "mode": "live"
}
```

**Respuesta:**
```json
{
  "status": "success",
  "result": {
    "overall_status": "PASS|FAIL",
    "tests": [
      {
        "name": "Ping Test",
        "status": "PASS",
        "message": "Device reachable",
        "duration_ms": 150
      },
      {
        "name": "TCP Connection",
        "status": "PASS",
        "message": "Port 65050 open",
        "duration_ms": 50
      }
    ]
  }
}
```

### Validación Batch Commands
```http
POST /api/validation/batch-commands
Content-Type: application/json

{
  "mode": "live",
  "scenario_id": "drs_master_batch",
  "ip_address": "192.168.11.22",
  "hostname": "test_device"
}
```

---

## 🔧 Lógica de Validación

### Standalone Validator (`standalone_validator.py`)

```python
class TechnicianTCPValidator:
    def validate_device(self, ip, scenario, hostname, live_mode):
        results = []

        # Test 1: Ping
        ping_result = self._ping_test(ip)
        results.append(ping_result)

        # Test 2: TCP Connection (puerto 65050)
        tcp_result = self._tcp_connection_test(ip, ports=[65050])
        results.append(tcp_result)

        # Test 3: Device Commands (si TCP OK)
        if tcp_result['status'] == 'PASS':
            cmd_results = self._validate_device_commands(ip, scenario)
            results.extend(cmd_results)

        return self._format_results(results)
```

### Batch Commands Validator (`batch_commands_validator.py`)

```python
class BatchCommandsValidator:
    DRS_MASTER_COMMANDS = [
        'optical_port_devices_connected_1',
        'optical_port_devices_connected_2',
        'input_and_output_power',
        'channel_switch',
        # ... 22 comandos más
    ]

    def validate_batch(self, ip, command_set, live_mode):
        results = []
        for cmd in self._get_commands_for_set(command_set):
            result = self._send_command_and_validate(ip, cmd, live_mode)
            results.append(result)
        return results
```

---

## 📋 Configuración de Dispositivos

### Archivo: `config/validation_scenarios.yaml`

```yaml
scenarios:
  - id: "dmu_basic_check"
    name: "DMU Basic Communication"
    default_ip: "192.168.11.22"
    default_hostname: "dmu"
    tests:
      - type: "ping"
      - type: "tcp"
        ports: [65050]
      - type: "commands"
        protocol: "santone"

  - id: "dru_remote_check"
    name: "DRU Remote Validation"
    default_ip: "192.168.11.100"
    default_hostname: "dru34132"
    tests:
      - type: "ping"
      - type: "tcp"
        ports: [65050]
      - type: "commands"
        protocol: "santone"
```

---

## 🔌 Protocolo DRS (Santone)

### Puerto TCP: 65050

### Comandos Soportados

#### DRS Master Commands (13)
- `optical_port_devices_connected_1/2/3/4`
- `input_and_output_power`
- `channel_switch`, `channel_frequency_configuration`
- `central_frequency_point`, `broadband_switching`
- `optical_port_switch`, `optical_port_status`
- `subband_bandwidth`, `temperature`, `device_id`, `datt`

#### DRS Remote Commands (13)
- `temperature`, `input_and_output_power`
- `channel_switch`, `channel_frequency_configuration`
- `central_frequency_point`, `broadband_switching`
- `optical_port_switch`, `optical_port_status`
- `subband_bandwidth`, `optical_port_devices_connected_1/2`
- `device_id`, `datt`

### Formato de Trama
```python
# Ejemplo trama hexadecimal
hex_frame = "010300000001840A"  # Comando device_id
```

---

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Instalar herramientas de red
RUN apt-get update && apt-get install -y \
    iputils-ping \
    telnet \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
CMD ["uvicorn", "validation_app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  drs-validation:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

---

## 🧪 Modos de Operación

### Mock Mode
- **Propósito**: Desarrollo, testing, demostraciones
- **Comportamiento**: Simula respuestas sin conexiones reales
- **Ventajas**: Rápido, predecible, no requiere hardware

### Live Mode
- **Propósito**: Validación real en producción
- **Comportamiento**: Conecta con dispositivos físicos
- **Consideraciones**: Manejo de timeouts, errores de red

---

## 📊 Manejo de Resultados

### Estructura de Resultados
```python
{
    "overall_status": "PASS|FAIL",
    "tests": [
        {
            "name": str,
            "status": "PASS|FAIL",
            "message": str,
            "details": str,  # opcional
            "duration_ms": int
        }
    ],
    "duration_ms": int,
    "timestamp": str,
    "scenario_id": str,
    "mode": "mock|live"
}
```

### Lógica de Estado General
```python
def calculate_overall_status(test_results):
    # FAIL si cualquier test crítico falla
    critical_tests = ['ping', 'tcp_connection']
    for test in test_results:
        if test['name'] in critical_tests and test['status'] == 'FAIL':
            return 'FAIL'

    # FAIL si menos del 80% de comandos pasan
    command_tests = [t for t in test_results if 'command' in t['name']]
    if command_tests:
        pass_rate = sum(1 for t in command_tests if t['status'] == 'PASS') / len(command_tests)
        if pass_rate < 0.8:
            return 'FAIL'

    return 'PASS'
```

---

## 🔍 Debugging y Troubleshooting

### Logs del Sistema
```bash
# Ver logs del contenedor
docker-compose logs -f drs-validation

# Ver logs específicos
docker-compose logs drs-validation | grep ERROR

# Logs de aplicación
tail -f logs/validation_app.log
```

### Tests de Conectividad
```bash
# Ping manual
ping 192.168.11.22

# Telnet al puerto DRS
telnet 192.168.11.22 65050

# Netcat test
nc -zv 192.168.11.22 65050
```

### Debug API
```bash
# Health check
curl http://localhost:8080/health

# Test API
curl -X POST http://localhost:8080/api/validation/run \
  -H "Content-Type: application/json" \
  -d '{"scenario_id":"dmu_basic_check","ip_address":"192.168.11.22","hostname":"dmu","mode":"mock"}'
```

---

## 🔄 Desarrollo y Extensión

### Agregar Nuevo Dispositivo
1. **Configurar** en `validation_scenarios.yaml`
2. **Implementar** lógica específica en validator
3. **Actualizar** interfaz web si necesario
4. **Probar** en mock y live modes

### Agregar Nuevo Comando DRS
1. **Definir** trama hexadecimal en `hex_frames.py`
2. **Agregar** a lista de comandos en `batch_commands_validator.py`
3. **Implementar** validación de respuesta
4. **Actualizar** documentación

### Extender API
1. **Crear** nuevo endpoint en `validation_app.py`
2. **Implementar** lógica en validator correspondiente
3. **Actualizar** documentación de API
4. **Probar** integración

---

## 📋 Dependencias

### Python Packages (`requirements.txt`)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
jinja2==3.1.2
python-multipart==0.0.6
```

### System Dependencies (Docker)
- `iputils-ping`: Para tests de conectividad
- `telnet`: Para debugging de conexiones
- `netcat-traditional`: Para tests de puertos
- `curl`: Para health checks

---

## 🎯 Métricas de Rendimiento

### Tiempos Esperados
- **Ping Test**: 100-200ms
- **TCP Connection**: 50-100ms
- **Single Command**: 200-500ms
- **Batch Commands (26)**: 5-10 segundos
- **Validación Completa**: 6-12 segundos

### Límites de Recursos
- **CPU**: < 5% en idle, < 20% durante validación
- **Memoria**: ~100MB base, ~150MB durante validación
- **Red**: ~50KB por validación completa

---

*Documentación técnica para desarrolladores y administradores del sistema* 🔧</content>
<parameter name="filePath">/home/arturo/sw-drsmonitoring/validation-framework/DOCUMENTACION_TECNICA.md