# DRS Validation Framework - Development Guide

## 🚀 Quick Start

### Development Mode (with Hot Reload)
```bash
# From project root
./dev.sh
```

This will:
- Start the application with hot reload enabled
- Watch for file changes and restart automatically
- Serve on http://localhost:8080

### Manual Start
```bash
cd validation-framework
source venv/bin/activate
export PYTHONPATH="$(pwd)/src"
python -m uvicorn validation_app:app --host 0.0.0.0 --port 8080 --reload --log-level info
```

## 🌐 Access Points

- **Web Interface**: http://localhost:8080
- **Health Check**: http://localhost:8080/health
- **API Documentation**: http://localhost:8080/docs
- **API Endpoints**:
  - `POST /api/validation/run` - Run validation
  - `POST /api/validation/ping/{ip}` - Test connectivity
  - `POST /api/validation/batch-commands` - Run batch commands

## 🛠️ Development Workflow

1. **Make changes** to Python files in `src/` or JavaScript in `src/web/static/`
2. **Save the file** - hot reload will automatically restart the server
3. **Test in browser** - refresh to see changes
4. **Check logs** in terminal for any errors

## 🐳 Production Deployment

For production deployment on remote servers:

```bash
# Deploy via Ansible
cd validation-framework
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/site.yml
```

## 📁 Project Structure

```
validation-framework/
├── src/
│   ├── validation_app.py      # FastAPI application
│   ├── web/
│   │   ├── static/
│   │   │   ├── app.js         # Frontend JavaScript
│   │   │   └── style.css      # Styles
│   │   └── templates/
│   │       └── index.html     # Main template
│   └── config/                # Configuration files
├── results/                   # Validation results (created automatically)
├── logs/                      # Application logs (created automatically)
├── temp/                      # Temporary files (created automatically)
└── ansible/                   # Deployment automation
```

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure `PYTHONPATH` is set: `export PYTHONPATH="$(pwd)/src"`

**"Permission denied" on directories:**
- Check that `results/`, `logs/`, `temp/` directories exist and are writable

**Hot reload not working:**
- Make sure you're running with `--reload` flag
- Check that files are saved in the watched directories

**API 404 errors:**
- Verify endpoints match: `/api/validation/run`, not `/api/run-validation`
- Check browser console for JavaScript errors