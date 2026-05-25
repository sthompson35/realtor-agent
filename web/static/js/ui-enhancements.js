/**
 * Form Validation Utilities
 */

class FormValidator {
    constructor() {
        this.validators = {
            required: (value) => value && value.trim() !== '',
            email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
            phone: (value) => /^[\d\s\-\+\(\)]+$/.test(value),
            number: (value) => !isNaN(parseFloat(value)),
            minLength: (value, min) => value && value.length >= min,
            maxLength: (value, max) => value && value.length <= max,
            min: (value, min) => parseFloat(value) >= min,
            max: (value, max) => parseFloat(value) <= max,
            url: (value) => {
                try {
                    new URL(value);
                    return true;
                } catch {
                    return false;
                }
            },
            date: (value) => !isNaN(Date.parse(value)),
            zipcode: (value) => /^\d{5}(-\d{4})?$/.test(value)
        };
    }

    validate(formElement) {
        const errors = {};
        let isValid = true;

        const inputs = formElement.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            const fieldErrors = this.validateField(input);
            if (fieldErrors.length > 0) {
                errors[input.name] = fieldErrors;
                isValid = false;
                this.showFieldError(input, fieldErrors[0]);
            } else {
                this.clearFieldError(input);
            }
        });

        return { isValid, errors };
    }

    validateField(input) {
        const errors = [];
        const value = input.value;
        const rules = this.getValidationRules(input);

        for (const [rule, param] of Object.entries(rules)) {
            if (this.validators[rule]) {
                const isValid = param !== undefined 
                    ? this.validators[rule](value, param)
                    : this.validators[rule](value);
                
                if (!isValid) {
                    errors.push(this.getErrorMessage(rule, input.name, param));
                }
            }
        }

        return errors;
    }

    getValidationRules(input) {
        const rules = {};
        
        if (input.required) rules.required = true;
        if (input.type === 'email') rules.email = true;
        if (input.type === 'tel') rules.phone = true;
        if (input.type === 'number') rules.number = true;
        if (input.type === 'url') rules.url = true;
        if (input.type === 'date') rules.date = true;
        if (input.minLength) rules.minLength = input.minLength;
        if (input.maxLength) rules.maxLength = input.maxLength;
        if (input.min) rules.min = parseFloat(input.min);
        if (input.max) rules.max = parseFloat(input.max);
        if (input.dataset.validation === 'zipcode') rules.zipcode = true;

        return rules;
    }

    getErrorMessage(rule, fieldName, param) {
        const messages = {
            required: `${fieldName} is required`,
            email: 'Please enter a valid email address',
            phone: 'Please enter a valid phone number',
            number: 'Please enter a valid number',
            minLength: `Minimum length is ${param} characters`,
            maxLength: `Maximum length is ${param} characters`,
            min: `Minimum value is ${param}`,
            max: `Maximum value is ${param}`,
            url: 'Please enter a valid URL',
            date: 'Please enter a valid date',
            zipcode: 'Please enter a valid ZIP code'
        };

        return messages[rule] || 'Invalid input';
    }

    showFieldError(input, message) {
        input.classList.add('is-invalid');
        
        let errorElement = input.parentElement.querySelector('.invalid-feedback');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            input.parentElement.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    clearFieldError(input) {
        input.classList.remove('is-invalid');
        
        const errorElement = input.parentElement.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    clearAllErrors(formElement) {
        const inputs = formElement.querySelectorAll('input, select, textarea');
        inputs.forEach(input => this.clearFieldError(input));
    }
}

/**
 * Enhanced Loading States
 */

class LoadingStateManager {
    constructor() {
        this.loadingElements = new Map();
    }

    show(elementId, message = 'Loading...') {
        const element = document.getElementById(elementId);
        if (!element) return;

        const originalContent = element.innerHTML;
        this.loadingElements.set(elementId, originalContent);

        element.disabled = true;
        element.classList.add('loading');
        
        const spinner = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            ${message}
        `;
        
        element.innerHTML = spinner;
    }

    hide(elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const originalContent = this.loadingElements.get(elementId);
        if (originalContent) {
            element.innerHTML = originalContent;
            this.loadingElements.delete(elementId);
        }

        element.disabled = false;
        element.classList.remove('loading');
    }

    showOverlay(containerId, message = 'Loading...') {
        const container = document.getElementById(containerId);
        if (!container) return;

        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">${message}</p>
            </div>
        `;
        
        container.style.position = 'relative';
        container.appendChild(overlay);
    }

    hideOverlay(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const overlay = container.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

/**
 * Enhanced Error Messages
 */

class ErrorMessageManager {
    constructor() {
        this.errorContainer = this.createErrorContainer();
    }

    createErrorContainer() {
        let container = document.getElementById('error-messages');
        if (!container) {
            container = document.createElement('div');
            container.id = 'error-messages';
            container.className = 'error-messages-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'error', duration = 5000) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alert.innerHTML = `
            <strong>${type === 'error' ? 'Error!' : 'Success!'}</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        this.errorContainer.appendChild(alert);

        if (duration > 0) {
            setTimeout(() => {
                alert.classList.remove('show');
                setTimeout(() => alert.remove(), 150);
            }, duration);
        }
    }

    showValidationErrors(errors) {
        const errorList = Object.entries(errors)
            .map(([field, messages]) => `<li><strong>${field}:</strong> ${messages.join(', ')}</li>`)
            .join('');

        this.show(`
            <p>Please fix the following errors:</p>
            <ul>${errorList}</ul>
        `, 'error', 0);
    }

    clear() {
        this.errorContainer.innerHTML = '';
    }
}

// Global instances
const formValidator = new FormValidator();
const loadingStateManager = new LoadingStateManager();
const errorMessageManager = new ErrorMessageManager();

// Export for use in other modules
window.formValidator = formValidator;
window.loadingStateManager = loadingStateManager;
window.errorMessageManager = errorMessageManager;
