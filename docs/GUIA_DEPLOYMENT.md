# 🚀 Guía de Deployment - DRS Validation Framework

## 🎯 Opciones de Deployment

### Opción 1: Ansible (Recomendado - Automatizado)

#### Requisitos Previos
- **Máquina de control**: Linux, macOS o WSL2 (NO Windows nativo)
- **Python 3.8+** con pip
- **Cliente SSH** configurado
- **Acceso de red** al MiniPC en 192.168.60.140

#### Configuración del MiniPC
- **IP**: 192.168.60.140 (estática)
- **Usuario**: pi
- **Autenticación**: SSH basado en clave (sin contraseña)
- **Privilegios**: acceso sudo para usuario pi
- **OS**: Raspberry Pi OS o Linux basado en Debian

#### Pasos de Deployment

1. **Instalar Ansible**
```bash
# Actualizar sistema
sudo apt update

# Instalar Ansible
sudo apt install ansible

# Verificar instalación
ansible --version
```

2. **Configurar acceso SSH**
```bash
# Generar clave SSH si no existe
ssh-keygen -t rsa -b 4096 -C "ansible@drs-deployment"

# Copiar clave pública al MiniPC
ssh-copy-id pi@192.168.60.140

# Probar acceso sin contraseña
ssh pi@192.168.60.140 "whoami && sudo whoami"
```

3. **Clonar repositorio**
```bash
# Clonar desde tu repositorio Git
git clone <tu-repo-url>
cd validation-framework
```

4. **Ejecutar deployment**
```bash
# Deployment completo
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml

# Con output detallado
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml -v
```

5. **Verificar deployment**
```bash
# Verificar estado del servicio
ansible minipc -m shell -a "sudo systemctl status drs-validation" -i ansible/inventory/hosts.yml

# Probar interfaz web
curl -f http://192.168.60.140:8080/health

# Verificar contenedores Docker
ansible minipc -m shell -a "docker ps" -i ansible/inventory/hosts.yml
```

### Opción 2: Docker Manual (Desarrollo/Local)

#### Requisitos
- Docker & Docker Compose
- Puerto 8080 disponible

#### Deployment
```bash
# Clonar repositorio
git clone <tu-repo-url>
cd validation-framework

# Construir y ejecutar
docker-compose up -d

# Verificar
curl http://localhost:8080/health
```

---

## 🎮 Acceso al Sistema

### Producción (MiniPC)
- **Interfaz Web**: http://192.168.60.140:8080
- **Documentación API**: http://192.168.60.140:8080/docs
- **Health Check**: http://192.168.60.140:8080/health

### Desarrollo (Local)
- **Interfaz Web**: http://localhost:8080
- **Documentación API**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

---

## 🔧 Comandos de Gestión (Producción)

### Acceso SSH
```bash
ssh pi@192.168.60.140
```

### Comandos de Gestión
```bash
# Ver estado del sistema
drs status

# Ver logs de aplicación
drs logs

# Reiniciar servicios
drs restart

# Backup manual
drs backup

# Verificar servicios del sistema
sudo systemctl status drs-validation

# Ver contenedores Docker
docker ps

# Ver logs de Docker
docker-compose -f /opt/drs-validation/docker-compose.yml logs -f
```

---

## 🛠️ Troubleshooting

### Problemas Comunes

#### SSH Connection Fails
```bash
# Probar SSH manualmente
ssh -vvv pi@192.168.60.140

# Verificar configuración SSH
cat ~/.ssh/config
```

#### Ansible Inventory Issues
```bash
# Depurar inventario
ansible-inventory -i ansible/inventory/hosts.yml --list --yaml

# Probar con usuario diferente
ansible minipc -m ping -i ansible/inventory/hosts.yml -u pi
```

#### Permission Errors
```bash
# Verificar acceso sudo
ssh pi@192.168.60.140 "sudo -l"

# Verificar grupos de usuario
ssh pi@192.168.60.140 "groups"
```

#### Service Deployment Issues
```bash
# Ver logs del servicio
ssh pi@192.168.60.140 "sudo journalctl -u drs-validation -n 50"

# Verificar instalación de Docker
ssh pi@192.168.60.140 "docker --version && docker-compose --version"
```

### Debug Commands
```bash
# Ver estado completo del sistema
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml --check

# Ejecutar solo tareas específicas
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml --tags="docker"

# Debug detallado
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml -vvv
```

---

## 📊 Verificación Post-Deployment

### Health Checks
```bash
# API health
curl http://192.168.60.140:8080/health

# Documentación API
curl http://192.168.60.140:8080/docs

# Estado del servicio
ssh pi@192.168.60.140 "drs status"
```

### Functional Tests
```bash
# Test básico (mock mode)
curl -X POST "http://192.168.60.140:8080/api/validation/run" \
     -H "Content-Type: application/json" \
     -d '{
       "scenario_id": "dmu_basic_check",
       "ip_address": "192.168.11.22",
       "hostname": "dmu",
       "mode": "mock"
     }'
```

---

## 🔄 Maintenance y Updates

### Actualizaciones
```bash
# Actualizar código
git pull origin main

# Redeploy (idempotente)
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml

# Deploy solo componentes específicos
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml --tags="docker,app"
```

### Backup y Recovery
```bash
# Backup manual
ssh pi@192.168.60.140 "drs backup"

# Listar backups
ssh pi@192.168.60.140 "ls -la /opt/drs-validation/backups/"

# Restore si es necesario
ssh pi@192.168.60.140 "drs restore <archivo-backup>"
```

---

## 📋 Checklist de Deployment

### Pre-Deployment
- [ ] Ansible instalado en máquina de control
- [ ] Acceso SSH configurado al MiniPC
- [ ] Repositorio clonado y actualizado
- [ ] Inventario verificado (hosts.yml)
- [ ] Conectividad de red confirmada

### Deployment
- [ ] Comando de deployment ejecutado exitosamente
- [ ] Sintaxis verificada sin errores
- [ ] Servicios iniciados correctamente
- [ ] Contenedores Docker corriendo

### Post-Deployment
- [ ] Interfaz web accesible (puerto 8080)
- [ ] API respondiendo correctamente
- [ ] Health checks pasando
- [ ] Validación mock funcionando
- [ ] Gestión de comandos operativa

---

## 🎯 Criterios de Éxito

✅ **Deployment Exitoso Cuando:**
- Servicio DRS corriendo y accesible
- Interfaz web respondiendo en puerto 8080
- Todos los contenedores Docker saludables
- Comandos de gestión funcionando
- Health checks automatizados activos

---

## 📞 Soporte

Para problemas de deployment:
1. Revisar esta guía de troubleshooting
2. Verificar logs con flags `-v` de Ansible
3. Revisar logs del sistema MiniPC
4. Confirmar conectividad de red
5. Validar configuración SSH

---

*Guía simplificada para deployment del DRS Validation Framework* 🚀</content>
<parameter name="filePath">/home/arturo/sw-drsmonitoring/validation-framework/GUIA_DEPLOYMENT.md