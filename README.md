# SW-DRS Validator

Sistema de validación para tarjetas digitales VHF, P25 y LC500 del proyecto DRS Monitoring.

## 📋 Descripción

Este proyecto contiene el framework de validación para el sistema de monitoreo DRS (Digital Radio System), diseñado para validar la conectividad y funcionalidad de tarjetas digitales VHF, P25 y LC500.

## 🚀 Características

- ✅ Validación TCP/IP puerto 65050
- ✅ Soporte para protocolos VHF, P25 y LC500
- ✅ Monitoreo de LNA/PA
- ✅ Reportes automatizados
- ✅ Interfaz web de monitoreo
- ✅ Tests automatizados

## 🏗️ Arquitectura

```
sw-DrsValidator/
├── src/                    # Código fuente principal
├── tests/                  # Suite de tests
├── docs/                   # Documentación técnica
├── scripts/                # Scripts de automatización
├── ansible/                # Configuración de despliegue
├── docker-compose.yml      # Orquestación de contenedores
└── requirements.txt        # Dependencias Python
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- Docker & Docker Compose
- Git

### Instalación rápida
```bash
# Clonar repositorio
git clone https://github.com/arturoSigmadev/sw-DrsValidator.git
cd sw-DrsValidator

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con Docker
docker-compose up -d
```

## 🧪 Testing

```bash
# Ejecutar tests completos
python -m pytest tests/

# Ejecutar validación específica
python src/main.py --validate-all
```

## 📚 Documentación

- [Documentación Técnica](./docs/)
- [Guía de Despliegue](./docs/GUIA_DEPLOYMENT.md)
- [API Reference](./docs/API_REFERENCE.md)

## 🔄 CI/CD

Este proyecto utiliza GitHub Actions para:
- ✅ Tests automatizados
- ✅ Validación de código
- ✅ Build de contenedores
- ✅ Despliegue automático

## 📊 Estado del Proyecto

### Releases
- **v1.0.0** - Foundation ✅
- **v1.1.0** - Improvements 🚧
- **v1.2.0** - Analytics 📋
- **v2.0.0** - Production Ready 📋

### Compatibilidad
- **VHF**: ✅ Compatible (versión 231016-BB1-145-15M-16C-OP8)
- **P25**: ✅ Compatible (versión 231115-BB1-806D851M-18M-16C-OP8)
- **LC500**: ❌ No compatible (FPGA:250529-16A, Software:250530-05)

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
