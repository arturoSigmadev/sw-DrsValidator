# Guía de Uso - Batch Commands Validator API

## Descripción General

El **Batch Commands Validator** proporciona una API REST completa para validar múltiples comandos DRS usando el protocolo Santone. Soporta tanto modo mock (para testing) como modo live (dispositivos reales).

## Características Principales

- ✅ **Validación masiva**: 28+ comandos DRS (15 Master + 13 Remote)
- ✅ **Integración SantoneDecoder**: Decodificación profesional de respuestas
- ✅ **Modo Mock/Live**: Testing sin dispositivo + validación real
- ✅ **API REST**: Endpoints FastAPI con documentación automática
- ✅ **Timeouts configurables**: Control de tiempos por comando
- ✅ **Estadísticas detalladas**: Success rate, duraciones, errores

## Endpoints API

### 1. Ejecutar Batch de Comandos

```http
POST /api/validation/batch-commands
Content-Type: application/json

{
  "ip_address": "192.168.1.100",
  "command_type": "master",
  "mode": "mock",
  "selected_commands": ["device_id", "temperature", "optical_port_devices_connected_1"],
  "timeout_seconds": 3
}
```

**Respuesta:**
```json
{
  "overall_status": "PASS",
  "command_type": "master",
  "mode": "mock", 
  "ip_address": "192.168.1.100",
  "total_commands": 3,
  "commands_tested": 3,
  "statistics": {
    "total_commands": 3,
    "passed": 3,
    "failed": 0,
    "timeouts": 0,
    "errors": 0,
    "success_rate": 100.0,
    "average_duration_ms": 125.3
  },
  "results": [
    {
      "command": "device_id",
      "command_type": "master",
      "status": "PASS",
      "message": "✅ Mock validation successful for device_id",
      "decoded_values": {
        "device_id": 3594,
        "status": "mock_enhanced",
        "decoder_mapping": true
      },
      "duration_ms": 153
    }
  ],
  "duration_ms": 376,
  "timestamp": "2025-09-26 13:15:08"
}
```

### 2. Obtener Comandos Soportados

```http
GET /api/validation/supported-commands
```

**Respuesta:**
```json
{
  "master_commands": [
    "optical_port_devices_connected_1",
    "optical_port_devices_connected_2", 
    "device_id",
    "temperature",
    "input_and_output_power"
  ],
  "remote_commands": [
    "temperature",
    "device_id", 
    "input_and_output_power"
  ],
  "total_commands": 28,
  "decoder_mappings": {
    "device_id": true,
    "temperature": true,
    "optical_port_devices_connected_1": true
  }
}
```

### 3. Estado del Sistema

```http
GET /api/validation/batch-commands/status
```

## Modo de Uso

### Modo Mock (Recomendado para Testing)

El modo mock es ideal para:
- ✅ Desarrollo y testing de aplicaciones
- ✅ Validación de lógica sin hardware
- ✅ Demos y presentaciones
- ✅ CI/CD pipeline testing

```bash
curl -X POST "http://localhost:8000/api/validation/batch-commands" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.1.100",
    "command_type": "master",
    "mode": "mock",
    "selected_commands": ["device_id", "temperature"]
  }'
```

### Modo Live (Dispositivos Reales)

El modo live requiere:
- 🔌 Dispositivo DRS en red (puerto 65050)
- 🌐 Conectividad TCP al dispositivo
- ⏱️ Timeouts configurables (default: 3s)

```bash
curl -X POST "http://localhost:8000/api/validation/batch-commands" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.1.50",
    "command_type": "master", 
    "mode": "live",
    "timeout_seconds": 5
  }'
```

## Comandos Disponibles

### Master Commands (15 comandos)
- `optical_port_devices_connected_1/2/3/4` - Dispositivos conectados por puerto
- `input_and_output_power` - Potencias de entrada y salida
- `channel_switch` - Estado switching de canales
- `channel_frequency_configuration` - Configuración frecuencias
- `central_frequency_point` - Punto central de frecuencia
- `broadband_switching` - Switching banda ancha
- `optical_port_switch` - Estado puerto óptico
- `optical_port_status` - Estado puerto óptico
- `subband_bandwidth` - Ancho banda subcanal
- `temperature` - Temperatura dispositivo
- `device_id` - ID único del dispositivo
- `datt` - Comando DATT

### Remote Commands (13 comandos)
- `temperature` - Temperatura dispositivo remoto
- `input_and_output_power` - Potencias dispositivo remoto
- `device_id` - ID dispositivo remoto
- `channel_switch` - Switching canales remoto
- `optical_port_devices_connected_1/2` - Dispositivos conectados
- Y más...

## Decodificación de Respuestas

Todos los comandos usan **SantoneDecoder** para parsing profesional:

```json
{
  "device_id": 3594,                    // ID extraído (16-bit)
  "temperature": 45.5,                  // °C (signed 16-bit * 0.1)
  "central_frequency_point": "12.3456", // MHz (32-bit / 10000)
  "optical_port_devices_connected_1": 3, // Count de dispositivos
  "_decoder_info": {
    "method": "_decode_device_id",
    "integration_phase": "enhanced_mock"
  }
}
```

## Interpretación de Resultados

### Status por Comando
- **PASS**: Comando ejecutado y decodificado correctamente
- **FAIL**: Comando falló (dispositivo reportó error)
- **TIMEOUT**: Timeout TCP (dispositivo no responde)
- **ERROR**: Error de ejecución (trama inválida, etc.)

### Overall Status
- **PASS**: ≥80% comandos exitosos
- **FAIL**: <80% comandos exitosos
- **ERROR**: Error crítico del sistema

### Estadísticas
```json
{
  "total_commands": 5,
  "passed": 4,
  "failed": 0,
  "timeouts": 1,
  "errors": 0,
  "success_rate": 80.0,        // 4/5 comandos exitosos
  "average_duration_ms": 145.2 // Tiempo promedio por comando
}
```

## Ejemplos de Uso

### 1. Test Completo Master Commands

```python
import requests

response = requests.post('http://localhost:8000/api/validation/batch-commands', json={
    "ip_address": "192.168.1.100",
    "command_type": "master",
    "mode": "mock"
    # Sin selected_commands = ejecuta TODOS los comandos master
})

print(f"Success Rate: {response.json()['statistics']['success_rate']}%")
```

### 2. Test Específico de Dispositivos Conectados

```python
response = requests.post('http://localhost:8000/api/validation/batch-commands', json={
    "ip_address": "192.168.1.50",
    "command_type": "master",
    "mode": "live",
    "selected_commands": [
        "optical_port_devices_connected_1",
        "optical_port_devices_connected_2",
        "optical_port_devices_connected_3", 
        "optical_port_devices_connected_4"
    ]
})

# Extraer cantidad de dispositivos por puerto
for result in response.json()['results']:
    cmd = result['command']
    if 'optical_port_devices_connected' in cmd:
        port = cmd.split('_')[-1]
        devices = result['decoded_values'].get(cmd, 0)
        print(f"Puerto {port}: {devices} dispositivos")
```

### 3. Verificar Comandos Soportados

```python
response = requests.get('http://localhost:8000/api/validation/supported-commands')
data = response.json()

print(f"Total comandos: {data['total_commands']}")
print(f"Master: {len(data['master_commands'])}")
print(f"Remote: {len(data['remote_commands'])}")

# Comandos con decodificadores específicos
mapped_commands = [cmd for cmd, mapped in data['decoder_mappings'].items() if mapped]
print(f"Con decodificadores: {len(mapped_commands)}")
```

## Troubleshooting

### Error 503 - Service Unavailable
```json
{"detail": "Batch commands validator not available"}
```
**Solución**: Verificar que el módulo `batch_commands_validator.py` esté disponible.

### Error 400 - Bad Request  
```json
{"detail": "command_type must be 'master' or 'remote'"}
```
**Solución**: Usar `command_type: "master"` o `command_type: "remote"`.

### Timeouts en Modo Live
- Verificar conectividad: `ping <ip_address>`
- Verificar puerto 65050: `telnet <ip_address> 65050` 
- Aumentar `timeout_seconds` para redes lentas

### Comandos No Reconocidos
- Consultar `/api/validation/supported-commands`
- Verificar spelling exacto de comandos
- Usar nombres de `hex_frames.py`

## Documentación Automática

La API incluye documentación interactiva:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Permite probar endpoints directamente desde el navegador.

---

## Integración con Aplicaciones

### JavaScript/Frontend
```javascript
async function runBatchTest(deviceIP, commands) {
  const response = await fetch('/api/validation/batch-commands', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ip_address: deviceIP,
      command_type: 'master',
      mode: 'mock',
      selected_commands: commands
    })
  });
  
  const result = await response.json();
  console.log(`Success Rate: ${result.statistics.success_rate}%`);
  return result;
}
```

### Python Script
```python
from validation.batch_commands_validator import BatchCommandsValidator, CommandType

validator = BatchCommandsValidator()
result = validator.validate_batch_commands(
    ip_address="192.168.1.100",
    command_type=CommandType.MASTER,
    mode="mock"
)
```

## Próximos Pasos

- [ ] Integración con sistema de reportes
- [ ] Almacenamiento de histórico de tests
- [ ] Alertas automáticas por errores
- [ ] Dashboard web para visualización