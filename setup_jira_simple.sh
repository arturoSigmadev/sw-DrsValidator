#!/bin/bash
# Script simplificado de configuración Jira para sw-DrsValidator
# Fecha: 2 de Octubre, 2025

set -e

echo "🎯 Configuración simplificada de Jira para sw-DrsValidator"
echo "========================================================="

# Cargar variables de entorno de manera segura
export JIRA_URL="${JIRA_URL:-https://uqomm-teams.atlassian.net}"
export JIRA_USERNAME="${JIRA_USERNAME:-arturo@uqomm.com}"
export JIRA_API_TOKEN="${JIRA_API_TOKEN:-YOUR_API_TOKEN_HERE}"
export JIRA_PROJECT_KEY="${JIRA_PROJECT_KEY:-SW}"

# Función para crear issue simple
create_simple_issue() {
    local summary="$1"
    local description="$2"
    local issue_type="$3"

    echo "📝 Creando: $summary"

    # JSON simplificado y escapado correctamente
    local json_data="{
        \"fields\": {
            \"project\": {
                \"key\": \"$JIRA_PROJECT_KEY\"
            },
            \"summary\": \"$summary\",
            \"description\": \"$description\",
            \"issuetype\": {
                \"name\": \"$issue_type\"
            },
            \"assignee\": {
                \"name\": \"$JIRA_USERNAME\"
            },
            \"labels\": [\"sw-drs-validator\", \"migration\"]
        }
    }"

    # Debug: mostrar JSON
    echo "JSON: $json_data"

    local response=$(curl -s -u "$JIRA_USERNAME:$JIRA_API_TOKEN" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$json_data" \
        "$JIRA_URL/rest/api/2/issue")

    echo "Response: $response"

    local issue_key=$(echo "$response" | grep -o '"key":"[^"]*' | cut -d'"' -f4)

    if [ -n "$issue_key" ]; then
        echo "✅ Creado: $JIRA_URL/browse/$issue_key"
        echo "$issue_key" >> jira_issues_created.txt
    else
        echo "❌ Error creando issue"
    fi
}

# Verificar conexión
echo "🔗 Verificando conexión..."
if curl -s -u "$JIRA_USERNAME:$JIRA_API_TOKEN" "$JIRA_URL/rest/api/2/project/$JIRA_PROJECT_KEY" > /dev/null; then
    echo "✅ Conexión OK"
else
    echo "❌ Error de conexión"
    exit 1
fi

# Crear archivo de tracking
> jira_issues_created.txt

echo ""
echo "🚀 Creando issues básicos..."

# Issue 1: Épica de migración
create_simple_issue \
    "EPIC-001: Migración Validation Framework" \
    "Migración completa del validation-framework al repositorio independiente sw-DrsValidator" \
    "Epic"

# Issue 2: Setup CI/CD (usando "Tarea")
create_simple_issue \
    "SW-001: Configurar GitHub Actions CI/CD" \
    "Implementar pipeline básico de CI/CD con tests automáticos" \
    "Tarea"

# Issue 3: Verificar funcionalidad (usando "Tarea")
create_simple_issue \
    "SW-002: Verificar funcionalidad post-migración" \
    "Ejecutar tests completos y verificar que todo funciona después de la migración" \
    "Tarea"

echo ""
echo "✅ Proceso completado!"
echo "Issues creados: $(wc -l < jira_issues_created.txt)"
echo "Ver archivo: jira_issues_created.txt"