# SW-DRS Validator

Sistema de validación completo para tarjetas digitales VHF, P25 y LC500 del proyecto DRS Monitoring.

## 📋 Descripción

Este proyecto contiene el framework de validación para el sistema de monitoreo DRS (Digital Radio System), diseñado para validar la conectividad y funcionalidad de tarjetas digitales VHF, P25 y LC500.

## 🚀 Características

- ✅ Validación TCP/IP puerto 65050
- ✅ Soporte para protocolos VHF, P25 y LC500
- ✅ Monitoreo de LNA/PA
- ✅ Reportes automatizados
- ✅ Interfaz web de monitoreo
- ✅ Tests automatizados
- ✅ API REST completa con documentación automática
- ✅ Despliegue automatizado con Ansible
- ✅ Contenedorización con Docker

## 🏗️ Arquitectura

```
sw-DrsValidator/
├── src/                    # Código fuente principal
│   ├── validation_app.py   # FastAPI application
│   ├── web/                # Interfaz web
│   │   ├── static/         # JavaScript & CSS
│   │   └── templates/      # HTML templates
│   └── config/             # Configuraciones
├── tests/                  # Suite de tests
├── docs/                   # Documentación técnica
├── scripts/                # Scripts de automatización
├── ansible/                # Configuración de despliegue
├── planning/               # Archivos de planificación y Jira
├── docker-compose.yml      # Orquestación de contenedores
└── requirements.txt        # Dependencias Python
```

## 🛠️ Instalación y Desarrollo

### Prerrequisitos
- Python 3.8+
- Docker & Docker Compose
- Git
- Ansible (para despliegue)

### 🚀 Desarrollo Rápido (Hot Reload)

```bash
# Clonar repositorio
git clone https://github.com/arturoSigmadev/sw-DrsValidator.git
cd sw-DrsValidator

# Modo desarrollo con hot reload
./dev.sh
```

### 🐳 Instalación con Docker

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con Docker
docker-compose up -d
```

### 🔧 Instalación Manual

```bash
cd validation-framework
source venv/bin/activate
export PYTHONPATH="$(pwd)/src"
python -m uvicorn validation_app:app --host 0.0.0.0 --port 8080 --reload --log-level info
```

## 🌐 Puntos de Acceso

### Desarrollo
- **Interfaz Web**: http://localhost:8080
- **Health Check**: http://localhost:8080/health
- **Documentación API**: http://localhost:8080/docs

### Producción (MiniPC)
- **Interfaz Web**: http://192.168.60.140:8080
- **API Endpoints**:
  - `POST /api/validation/run` - Ejecutar validación
  - `POST /api/validation/ping/{ip}` - Test de conectividad
  - `POST /api/validation/batch-commands` - Ejecutar comandos batch
  - `GET /api/validation/supported-commands` - Lista de comandos disponibles
  - `GET /api/validation/batch-commands/status` - Estado del sistema

## 🚀 Despliegue en Producción

### Con Ansible (Recomendado)

```bash
# Configurar SSH keys
ssh-copy-id root@192.168.60.140

# Desplegar en MiniPC
cd ansible/
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --limit minipc
```

### Targets Soportados
- **MiniPC (Producción)**: `192.168.60.140` - Para técnicos de campo
- **Development (Local)**: `localhost` - Para desarrollo

## 🧪 Testing y Validación

```bash
# Ejecutar tests completos
python -m pytest tests/

# Ejecutar validación específica
python src/main.py --validate-all

# Scripts de testing de API (en planning/)
./planning/test_api.ps1
./planning/test_ping.ps1
```

## 🔄 Flujo de Desarrollo

1. **Hacer cambios** a archivos Python en `src/` o JavaScript en `src/web/static/`
2. **Guardar el archivo** - hot reload reiniciará automáticamente el servidor
3. **Probar en navegador** - refrescar para ver cambios
4. **Revisar logs** en terminal para errores

## 📚 Documentación

- [Documentación Técnica](./docs/DOCUMENTACION_TECNICA.md)
- [Guía de Despliegue](./docs/GUIA_DEPLOYMENT.md)
- [Plan de Mejoras](./planning/PLAN_MEJORA_VALIDATOR_FRAMEWORK.md)
- [Guía de API](./planning/BATCH_COMMANDS_API_GUIDE.md)

## 🔄 CI/CD

Este proyecto utiliza GitHub Actions para:
- ✅ Tests automatizados
- ✅ Validación de código
- ✅ Build de contenedores
- ✅ Despliegue automático

## 📊 Estado del Proyecto

### Releases
- **v1.0.0** - Foundation ✅
- **v1.1.0** - Improvements ✅
- **v1.2.0** - Analytics 🚧
- **v2.0.0** - Production Ready 📋

### Compatibilidad de Tarjetas
- **VHF**: ✅ Compatible (versión 231016-BB1-145-15M-16C-OP8)
- **P25**: ✅ Compatible (versión 231115-BB1-806D851M-18M-16C-OP8)
- **LC500**: ❌ No compatible (FPGA:250529-16A, Software:250530-05)

### API Status
- ✅ `POST /api/validation/batch-commands` - Ejecutar batch de comandos DRS
- ✅ `GET /api/validation/supported-commands` - 28 comandos disponibles 
- ✅ `GET /api/validation/batch-commands/status` - Capacidades del sistema
- ✅ Documentación automática con FastAPI

## 🔧 Resolución de Problemas

### Errores Comunes

**"Module not found":**
```bash
export PYTHONPATH="$(pwd)/src"
```

**"Permission denied" en directorios:**
- Verificar que `results/`, `logs/`, `temp/` existen y son escribibles

**Hot reload no funciona:**
- Asegurar que se ejecuta con `--reload`
- Verificar que los archivos se guardan en directorios observados

**Errores API 404:**
- Verificar endpoints: `/api/validation/run`, no `/api/run-validation`
- Revisar consola del navegador para errores JavaScript

## 📁 Organización de Archivos

### planning/
Contiene archivos de planificación, Jira y APIs:
- `setup_jira_simple.sh` - Script de configuración Jira
- `jira_issues_created.txt` - Lista de issues creados
- `REFACTOR_PLAN*.md` - Planes de refactorización
- `test_api.ps1` - Scripts de prueba de API

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

**Proyecto:** SW (DRS Monitoring)  
**Jira:** [https://uqomm-teams.atlassian.net/jira/core/projects/SW/summary](https://uqomm-teams.atlassian.net/jira/core/projects/SW/summary)  
**Responsable:** Arturo Armando Veras Olivos  
**Email:** arturo@uqomm.com

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

*Última actualización: Octubre 2025*