# Project Refactoring Plan

This document outlines the steps to reorganize the project structure to align with standard Python best practices.

## 1. Create New Directories

- [x] Create a `src` directory for all core application source code.
- [x] Create a `tests` directory for all test files.
- [x] Create a `reports` directory for generated test reports.

## 2. Move Files and Directories

- [x] Move `validation_app.py` into `src/`.
- [x] Move the `validation/` package into `src/`.
- [x] Move the `web/` directory into `src/`.
- [x] Move the `config/` directory into `src/`.
- [x] Move `test_api_integration.py` and `test_comprehensive.py` into `tests/`.
- [x] Move all `batch_commands_test_report_*.html` and `*.json` files into `reports/`.
- [x] Move the following markdown files into `docs/`:
    - `CHANGELOG.md`
    - `DEPLOYMENT_ANALYSIS_AND_CORRECTIONS.md`
    - `DOCUMENTACION_TECNICA.md`
    - `GUIA_DEPLOYMENT.md`
    - `README_SIMPLIFICADO.md`

## 3. Analyze and Update References

- [x] **Python Imports:** Scan all `.py` files in `src/` and `tests/` and update import statements to reflect the new structure.
- [x] **File Paths in Code:** Search for and correct any hardcoded file paths in the Python code to be location-independent.
- [x] **Configuration Files:** Inspect and update paths in `Dockerfile`, `docker-compose.yml`, and Ansible files (`ansible/**/*.yml`).
- [x] **Scripts:** Check and update relative paths in the `scripts/` directory.

## 4. Update `.gitignore`

- [x] Add the `reports/` directory to the `.gitignore` file.

## 5. Final Instructions

- [x] Provide updated commands for running the application and tests after the refactoring is complete.
