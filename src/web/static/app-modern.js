/* Modern JavaScript for DRS Validator UI */
/* Bootstrap 5 Integration + Enhanced User Experience */
/* Version: 2.0 - October 2025 */

class DRSValidatorUI {
    constructor() {
        this.currentTab = 'validation';
        this.validationInProgress = false;
        this.sidebarOpen = window.innerWidth >= 768;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSidebar();
        this.setupFormValidation();
        this.setupToastNotifications();
        this.loadPreviousResults();
        
        console.log('DRS Validator UI v2.0 initialized');
    }

    /* ========================================
       EVENT LISTENERS
    ======================================== */
    setupEventListeners() {
        // Sidebar toggle
        const sidebarToggle = document.getElementById('sidebarToggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        }

        // Navigation tabs
        document.querySelectorAll('.sidebar-nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const tabId = item.getAttribute('data-tab');
                this.switchTab(tabId);
            });
        });

        // Form submission
        const validationForm = document.getElementById('validationForm');
        if (validationForm) {
            validationForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.startValidation();
            });
        }

        // Pre-validation button
        const preValidateBtn = document.getElementById('preValidateBtn');
        if (preValidateBtn) {
            preValidateBtn.addEventListener('click', () => this.preValidateConnection());
        }

        // Clear output button
        const clearOutputBtn = document.getElementById('clearOutputBtn');
        if (clearOutputBtn) {
            clearOutputBtn.addEventListener('click', () => this.clearOutput());
        }

        // Export results button
        const exportResultsBtn = document.getElementById('exportResultsBtn');
        if (exportResultsBtn) {
            exportResultsBtn.addEventListener('click', () => this.exportResults());
        }

        // Batch upload button
        const uploadBatchBtn = document.getElementById('uploadBatchBtn');
        if (uploadBatchBtn) {
            uploadBatchBtn.addEventListener('click', () => this.uploadBatchFile());
        }

        // Window resize handler
        window.addEventListener('resize', () => this.handleResize());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }

    /* ========================================
       SIDEBAR MANAGEMENT
    ======================================== */
    setupSidebar() {
        this.updateSidebarState();
    }

    toggleSidebar() {
        this.sidebarOpen = !this.sidebarOpen;
        this.updateSidebarState();
    }

    updateSidebarState() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('mainContent');
        
        if (this.sidebarOpen) {
            sidebar.classList.add('active');
            mainContent.classList.add('sidebar-open');
        } else {
            sidebar.classList.remove('active');
            mainContent.classList.remove('sidebar-open');
        }
    }

    handleResize() {
        if (window.innerWidth >= 768) {
            this.sidebarOpen = true;
        } else {
            this.sidebarOpen = false;
        }
        this.updateSidebarState();
    }

    /* ========================================
       TAB NAVIGATION
    ======================================== */
    switchTab(tabId) {
        // Update active nav item
        document.querySelectorAll('.sidebar-nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });
        document.getElementById(tabId).style.display = 'block';

        // Update breadcrumb
        const currentPage = document.getElementById('currentPage');
        if (currentPage) {
            const tabNames = {
                'validation': 'Validación',
                'results': 'Resultados',
                'batch': 'Comandos Batch',
                'monitoring': 'Monitoreo',
                'help': 'Ayuda'
            };
            currentPage.textContent = tabNames[tabId] || 'DRS Validator';
        }

        this.currentTab = tabId;
        
        // Close sidebar on mobile after navigation
        if (window.innerWidth < 768) {
            this.sidebarOpen = false;
            this.updateSidebarState();
        }
    }

    /* ========================================
       FORM VALIDATION & SUBMISSION
    ======================================== */
    setupFormValidation() {
        const form = document.getElementById('validationForm');
        if (!form) return;

        // Real-time IP validation
        const deviceIp = document.getElementById('deviceIp');
        if (deviceIp) {
            deviceIp.addEventListener('input', (e) => {
                this.validateIPAddress(e.target);
            });
        }

        // Port validation
        const devicePort = document.getElementById('devicePort');
        if (devicePort) {
            devicePort.addEventListener('input', (e) => {
                this.validatePort(e.target);
            });
        }
    }

    validateIPAddress(input) {
        const ipPattern = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
        const isValid = ipPattern.test(input.value);
        
        if (input.value && !isValid) {
            input.classList.add('is-invalid');
            this.showFieldError(input, 'Formato de IP inválido');
        } else {
            input.classList.remove('is-invalid');
            this.hideFieldError(input);
        }
        
        return isValid;
    }

    validatePort(input) {
        const port = parseInt(input.value);
        const isValid = port >= 1 && port <= 65535;
        
        if (input.value && !isValid) {
            input.classList.add('is-invalid');
            this.showFieldError(input, 'Puerto debe estar entre 1 y 65535');
        } else {
            input.classList.remove('is-invalid');
            this.hideFieldError(input);
        }
        
        return isValid;
    }

    showFieldError(input, message) {
        let errorDiv = input.nextElementSibling;
        if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            input.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    hideFieldError(input) {
        const errorDiv = input.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
            errorDiv.remove();
        }
    }

    /* ========================================
       VALIDATION PROCESS
    ======================================== */
    async preValidateConnection() {
        const deviceIp = document.getElementById('deviceIp').value;
        const devicePort = document.getElementById('devicePort').value;
        
        if (!deviceIp || !devicePort) {
            this.showToast('error', 'Por favor complete IP y puerto antes de pre-validar');
            return;
        }

        const btn = document.getElementById('preValidateBtn');
        this.setButtonLoading(btn, true);
        
        try {
            const response = await fetch('/api/prevalidate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    ip_address: deviceIp, 
                    port: parseInt(devicePort) 
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showToast('success', 'Conexión exitosa al dispositivo');
            } else {
                this.showToast('error', `Error de conexión: ${result.error}`);
            }
        } catch (error) {
            this.showToast('error', 'Error al validar conexión');
            console.error('Pre-validation error:', error);
        } finally {
            this.setButtonLoading(btn, false);
        }
    }

    async startValidation() {
        if (this.validationInProgress) {
            this.showToast('warning', 'Validación ya en progreso');
            return;
        }

        const formData = new FormData(document.getElementById('validationForm'));
        const validationData = Object.fromEntries(formData);

        // Validate required fields
        if (!this.validateForm(validationData)) {
            return;
        }

        this.validationInProgress = true;
        this.showValidationProgress();
        this.clearOutput();
        
        const startBtn = document.getElementById('startValidationBtn');
        this.setButtonLoading(startBtn, true);

        try {
            await this.executeValidation(validationData);
        } catch (error) {
            this.showToast('error', 'Error durante la validación');
            console.error('Validation error:', error);
        } finally {
            this.validationInProgress = false;
            this.setButtonLoading(startBtn, false);
        }
    }

    validateForm(data) {
        const requiredFields = ['scenario_id', 'ip_address', 'port', 'timeout'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            this.showToast('error', 'Por favor complete todos los campos requeridos');
            return false;
        }

        // Validate IP format
        const ipInput = document.getElementById('deviceIp');
        if (!this.validateIPAddress(ipInput)) {
            this.showToast('error', 'Formato de IP inválido');
            return false;
        }

        // Validate port range
        const portInput = document.getElementById('devicePort');
        if (!this.validatePort(portInput)) {
            this.showToast('error', 'Puerto inválido');
            return false;
        }

        return true;
    }

    async executeValidation(validationData) {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(validationData)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        // Handle streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            this.processValidationChunk(chunk);
        }
        
        this.completeValidation();
    }

    processValidationChunk(chunk) {
        // Parse streaming data and update UI
        const lines = chunk.split('\n').filter(line => line.trim());
        
        lines.forEach(line => {
            try {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.substring(6));
                    this.updateValidationProgress(data);
                }
            } catch (error) {
                // Handle raw text output
                this.appendToOutput(line);
            }
        });
    }

    updateValidationProgress(data) {
        if (data.progress !== undefined) {
            this.setProgress(data.progress);
        }
        
        if (data.message) {
            this.updateProgressText(data.message);
            this.appendToOutput(data.message);
        }
        
        if (data.output) {
            this.appendToOutput(data.output);
        }
    }

    completeValidation() {
        this.setProgress(100);
        this.updateProgressText('Validación completada');
        this.showToast('success', 'Validación completada exitosamente');
        
        // Auto-switch to results tab after completion
        setTimeout(() => {
            this.switchTab('results');
            this.loadPreviousResults();
        }, 2000);
    }

    /* ========================================
       UI UPDATES
    ======================================== */
    showValidationProgress() {
        const progressSection = document.getElementById('validationProgress');
        const outputSection = document.getElementById('liveOutputSection');
        
        progressSection.style.display = 'block';
        outputSection.style.display = 'block';
        
        this.setProgress(0);
        this.updateProgressText('Iniciando validación...');
    }

    setProgress(percentage) {
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');
        
        if (progressBar) progressBar.style.width = `${percentage}%`;
        if (progressPercent) progressPercent.textContent = `${percentage}%`;
    }

    updateProgressText(text) {
        const progressText = document.getElementById('progressText');
        if (progressText) progressText.textContent = text;
    }

    appendToOutput(text) {
        const output = document.getElementById('liveOutput');
        if (!output) return;
        
        const line = document.createElement('div');
        line.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
        
        // Color coding based on content
        if (text.includes('ERROR') || text.includes('FAILED')) {
            line.className = 'text-danger';
        } else if (text.includes('SUCCESS') || text.includes('OK')) {
            line.className = 'text-success';
        } else if (text.includes('WARNING')) {
            line.className = 'text-warning';
        } else {
            line.className = 'text-info';
        }
        
        output.appendChild(line);
        output.scrollTop = output.scrollHeight;
    }

    clearOutput() {
        const output = document.getElementById('liveOutput');
        if (output) {
            output.innerHTML = `
                <div class="text-success">DRS Validator v2.0 - Ready</div>
                <div class="text-muted">Esperando comandos...</div>
            `;
        }
    }

    setButtonLoading(button, loading) {
        if (!button) return;
        
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
        }
    }

    /* ========================================
       TOAST NOTIFICATIONS
    ======================================== */
    setupToastNotifications() {
        // Create toast container if it doesn't exist
        if (!document.getElementById('toastContainer')) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
    }

    showToast(type, message, duration = 5000) {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = 'toast-modern';
        
        const icons = {
            success: 'bi-check-circle-fill text-success',
            error: 'bi-x-circle-fill text-danger',
            warning: 'bi-exclamation-triangle-fill text-warning',
            info: 'bi-info-circle-fill text-info'
        };

        toast.innerHTML = `
            <i class="bi ${icons[type] || icons.info}"></i>
            <div class="flex-grow-1">
                <div class="font-medium">${this.capitalizeFirst(type)}</div>
                <div class="text-sm text-muted">${message}</div>
            </div>
            <button type="button" class="btn-close btn-sm" aria-label="Close"></button>
        `;

        container.appendChild(toast);

        // Add close functionality
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            this.removeToast(toast);
        });

        // Auto-remove after duration
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);
    }

    removeToast(toast) {
        toast.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    /* ========================================
       RESULTS MANAGEMENT
    ======================================== */
    async loadPreviousResults() {
        try {
            const response = await fetch('/api/results');
            const results = await response.json();
            
            this.updateResultsTable(results);
        } catch (error) {
            console.error('Error loading results:', error);
        }
    }

    updateResultsTable(results) {
        const tbody = document.getElementById('resultsTableBody');
        if (!tbody) return;

        if (!results || results.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted py-4">
                        <i class="bi bi-inbox display-6 d-block mb-2"></i>
                        No hay validaciones disponibles
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = results.map(result => `
            <tr>
                <td>${new Date(result.timestamp).toLocaleString()}</td>
                <td>${result.device_ip}:${result.port}</td>
                <td>${result.scenario}</td>
                <td>
                    <span class="status-indicator status-${result.status === 'success' ? 'success' : 'error'}">
                        <i class="bi bi-circle-fill"></i>
                        ${result.status === 'success' ? 'Exitoso' : 'Falló'}
                    </span>
                </td>
                <td>${result.duration || 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="drsUI.viewResult('${result.id}')">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="drsUI.downloadResult('${result.id}')">
                        <i class="bi bi-download"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    async viewResult(resultId) {
        try {
            const response = await fetch(`/api/results/${resultId}`);
            const result = await response.json();
            
            // Show result in modal or new tab
            this.showResultModal(result);
        } catch (error) {
            this.showToast('error', 'Error al cargar el resultado');
        }
    }

    async downloadResult(resultId) {
        try {
            const response = await fetch(`/api/results/${resultId}/download`);
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `validation_${resultId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            this.showToast('error', 'Error al descargar el resultado');
        }
    }

    async exportResults() {
        try {
            const response = await fetch('/api/results/export');
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `drs_validation_results_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.showToast('success', 'Resultados exportados exitosamente');
        } catch (error) {
            this.showToast('error', 'Error al exportar resultados');
        }
    }

    /* ========================================
       BATCH OPERATIONS
    ======================================== */
    async uploadBatchFile() {
        const fileInput = document.getElementById('batchFile');
        if (!fileInput.files[0]) {
            this.showToast('warning', 'Por favor seleccione un archivo');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const btn = document.getElementById('uploadBatchBtn');
        this.setButtonLoading(btn, true);

        try {
            const response = await fetch('/api/batch/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.showToast('success', 'Archivo batch cargado y ejecutado');
                this.switchTab('validation');
            } else {
                this.showToast('error', `Error: ${result.error}`);
            }
        } catch (error) {
            this.showToast('error', 'Error al cargar archivo batch');
        } finally {
            this.setButtonLoading(btn, false);
        }
    }

    /* ========================================
       KEYBOARD SHORTCUTS
    ======================================== */
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Key combinations
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case '1':
                    e.preventDefault();
                    this.switchTab('validation');
                    break;
                case '2':
                    e.preventDefault();
                    this.switchTab('results');
                    break;
                case '3':
                    e.preventDefault();
                    this.switchTab('batch');
                    break;
                case 'b':
                    e.preventDefault();
                    this.toggleSidebar();
                    break;
            }
        }
        
        // Escape key
        if (e.key === 'Escape') {
            if (window.innerWidth < 768 && this.sidebarOpen) {
                this.sidebarOpen = false;
                this.updateSidebarState();
            }
        }
    }

    /* ========================================
       UTILITY METHODS
    ======================================== */
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize the UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.drsUI = new DRSValidatorUI();
});

// Export for global access
window.DRSValidatorUI = DRSValidatorUI;