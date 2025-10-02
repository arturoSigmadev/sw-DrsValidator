# 🚀 DRS Validation Framework

## 🎯 ¿Qué es esto?

Una herramienta web simple que permite a técnicos validar dispositivos de red DRS (DMU/DRU) con solo unos clics, sin necesidad de comandos complicados.

### ✨ Lo que hace:
- ✅ **Prueba conexión** a dispositivos DMU/DRU
- ✅ **Valida comandos DRS** usando protocolo Santone
- ✅ **Muestra resultados claros** (PASS/FAIL)
- ✅ **Funciona en mock/live** (pruebas o producción)

---

## 🚀 Inicio Rápido (3 pasos)

### 1. Instalar
```bash
# Con Ansible (recomendado)
sudo apt install ansible
cd validation-framework
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml

# O con Docker
docker-compose up -d
```

### 2. Acceder
- **Web**: http://192.168.60.140:8080 (producción) o http://localhost:8080 (desarrollo)
- **API**: http://192.168.60.140:8080/docs

### 3. Usar
1. Abrir la web
2. Seleccionar tipo de dispositivo (DMU/DRU)
3. Poner IP del dispositivo
4. Hacer clic "Run Validation"
5. Ver resultados ✅

---

## 📋 Dispositivos Soportados

| Dispositivo | IP por defecto | Puerto | Descripción |
|-------------|----------------|--------|-------------|
| **DMU** | 192.168.11.22 | 65050 | Data Management Unit |
| **DRU** | 192.168.11.100 | 65050 | Data Remote Unit |

---

## 🧪 Modos de Validación

### **Mock Mode** (Pruebas)
- Simula respuestas sin dispositivo real
- Ideal para aprender y testing
- Siempre funciona ✅

### **Live Mode** (Producción)
- Conecta con dispositivo real
- Validación completa
- Resultados reales

---

## 🔧 Comandos de Gestión

```bash
# Ver estado del sistema
ssh pi@192.168.60.140 "drs status"

# Ver logs
ssh pi@192.168.60.140 "drs logs"

# Reiniciar servicios
ssh pi@192.168.60.140 "drs restart"

# Backup manual
ssh pi@192.168.60.140 "drs backup"
```

---

## 📊 Resultados de Validación

### Ejemplo de resultado exitoso:
```
✅ OVERALL: PASS

🔍 Tests realizados:
✅ Ping: 192.168.11.22 reachable
✅ TCP Connection: Port 65050 open
✅ Device Commands: 26/26 commands working
✅ Temperature: 45°C (within range)
✅ Signal: -20dBm (good level)
```

### Ejemplo de resultado con problemas:
```
❌ OVERALL: FAIL

🔍 Tests realizados:
✅ Ping: 192.168.11.22 reachable
❌ TCP Connection: Port 65050 closed
❌ Device Commands: 0/26 commands responding
```

---

## 🆘 Solución de Problemas

### **No puedo acceder a la web**
```bash
# Verificar que el servicio está corriendo
ssh pi@192.168.60.140 "sudo systemctl status drs-validation"

# Reiniciar si es necesario
ssh pi@192.168.60.140 "drs restart"
```

### **Validación falla**
- Verificar IP del dispositivo
- Confirmar que el dispositivo está encendido
- Revisar conexión de red
- Usar "mock mode" para probar la interfaz

### **Ansible falla**
- Verificar SSH key authentication
- Confirmar que Ansible está instalado
- Revisar conectividad a 192.168.60.140

---

## 📞 Soporte

**Para técnicos de campo:**
- Usar la interfaz web para validaciones
- Reportar dispositivos que fallen consistentemente

**Para administradores:**
- Ver [GUÍA_DEPLOYMENT.md](GUIA_DEPLOYMENT.md) para instalación avanzada
- Ver [DOCUMENTACIÓN_TÉCNICA.md](DOCUMENTACION_TECNICA.md) para desarrollo

---

## 🎯 Estado del Proyecto

- ✅ **Implementación**: 100% completa
- ✅ **Deployment**: Automatizado con Ansible
- ✅ **Testing**: Mock y live modes funcionando
- ✅ **Documentación**: Simplificada y organizada
- ✅ **Producción**: Listo para uso en campo

---

*Framework creado para simplificar la validación de dispositivos DRS* 🚀</content>
<parameter name="filePath">/home/arturo/sw-drsmonitoring/validation-framework/README_SIMPLIFICADO.md