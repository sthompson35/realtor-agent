/**
 * Button Configuration & Action Handler
 * Manages all button states, tasks, and secure API interactions
 */

// ============================================================================
// BUTTON STATE MANAGEMENT
// ============================================================================

class ButtonStateManager {
    constructor() {
        this.states = new Map();
        this.loadingButtons = new Set();
    }

    setState(buttonId, state) {
        this.states.set(buttonId, {
            ...state,
            timestamp: Date.now()
        });
    }

    getState(buttonId) {
        return this.states.get(buttonId);
    }

    setLoading(buttonId, isLoading) {
        const button = document.getElementById(buttonId) || document.querySelector(`[data-button-id="${buttonId}"]`);
        if (!button) return;

        if (isLoading) {
            this.loadingButtons.add(buttonId);
            button.disabled = true;
            button.classList.add('loading');
            
            const originalText = button.innerHTML;
            button.dataset.originalText = originalText;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        } else {
            this.loadingButtons.delete(buttonId);
            button.disabled = false;
            button.classList.remove('loading');
            
            if (button.dataset.originalText) {
                button.innerHTML = button.dataset.originalText;
                delete button.dataset.originalText;
            }
        }
    }

    isLoading(buttonId) {
        return this.loadingButtons.has(buttonId);
    }
}

const buttonStateManager = new ButtonStateManager();

// ============================================================================
// SECURE API CLIENT
// ============================================================================

class SecureAPIClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.requestQueue = [];
        this.maxRetries = 3;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({ error: 'Request failed' }));
                throw new Error(error.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

const apiClient = new SecureAPIClient();

// ============================================================================
// BUTTON ACTION HANDLERS
// ============================================================================

const ButtonActions = {
    // ------------------------------------------------------------------------
    // LEAD GENERATION ACTIONS
    // ------------------------------------------------------------------------
    
    async addLead(data) {
        try {
            const result = await apiClient.post('/leads', data);
            showNotification('Lead added successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to add lead: ' + error.message, 'error');
            throw error;
        }
    },

    async callFSBO(leadId) {
        try {
            const result = await apiClient.post(`/leads/${leadId}/call`, {
                source: 'FSBO',
                timestamp: new Date().toISOString()
            });
            showNotification('Call logged successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to log call: ' + error.message, 'error');
            throw error;
        }
    },

    async callExpired(leadId) {
        try {
            const result = await apiClient.post(`/leads/${leadId}/call`, {
                source: 'Expired',
                timestamp: new Date().toISOString()
            });
            showNotification('Call logged successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to log call: ' + error.message, 'error');
            throw error;
        }
    },

    async doorKnock(data) {
        try {
            const result = await apiClient.post('/leads/door-knock', data);
            showNotification('Door knock activity logged', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to log activity: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // APPOINTMENT ACTIONS
    // ------------------------------------------------------------------------

    async scheduleAppointment(data) {
        try {
            const result = await apiClient.post('/appointments', data);
            showNotification('Appointment scheduled successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to schedule appointment: ' + error.message, 'error');
            throw error;
        }
    },

    async prepareAppointment(apptId) {
        try {
            const result = await apiClient.post(`/appointments/${apptId}/prepare`, {
                prepared_at: new Date().toISOString()
            });
            showNotification('Appointment preparation completed', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to prepare appointment: ' + error.message, 'error');
            throw error;
        }
    },

    async completeAppointment(apptId, data) {
        try {
            const result = await apiClient.post(`/appointments/${apptId}/complete`, data);
            showNotification('Appointment marked as completed', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to complete appointment: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // LISTING ACTIONS
    // ------------------------------------------------------------------------

    async createListing(data) {
        try {
            const result = await apiClient.post('/listings', data);
            showNotification('Listing created successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to create listing: ' + error.message, 'error');
            throw error;
        }
    },

    async updateListingPrice(listingId, newPrice) {
        try {
            const result = await apiClient.put(`/listings/${listingId}/price`, {
                price: newPrice
            });
            showNotification('Listing price updated', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to update price: ' + error.message, 'error');
            throw error;
        }
    },

    async launchMarketing(listingId) {
        try {
            const result = await apiClient.post(`/listings/${listingId}/marketing`, {
                launched_at: new Date().toISOString()
            });
            showNotification('Marketing campaign launched', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to launch marketing: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // CONTRACT ACTIONS
    // ------------------------------------------------------------------------

    async createContract(data) {
        try {
            const result = await apiClient.post('/contracts', data);
            showNotification('Contract created successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to create contract: ' + error.message, 'error');
            throw error;
        }
    },

    async updateContractStatus(contractId, status, notes) {
        try {
            const result = await apiClient.put(`/contracts/${contractId}/status`, {
                status,
                notes
            });
            showNotification('Contract status updated', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to update status: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // CONTACT/CRM ACTIONS
    // ------------------------------------------------------------------------

    async addLend(data) {
        try {
            const result = await apiClient.post('/lending', data);
            showNotification('Lender financing added successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to add lender financing: ' + error.message, 'error');
            throw error;
        }
    },

    async tagContact(contactId, tag) {
        try {
            const result = await apiClient.post(`/contacts/${contactId}/tag`, { tag });
            showNotification('Tag added to contact', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to tag contact: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // GOAL & METRICS ACTIONS
    // ------------------------------------------------------------------------

    async setGoal(data) {
        try {
            const result = await apiClient.post('/goals', data);
            showNotification('Goal set successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to set goal: ' + error.message, 'error');
            throw error;
        }
    },

    async viewMetrics(timeRange = '30d') {
        try {
            const result = await apiClient.get(`/metrics/dashboard?range=${timeRange}`);
            return result;
        } catch (error) {
            showNotification('Failed to load metrics: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // TEAM & LEVERAGE ACTIONS
    // ------------------------------------------------------------------------

    async addTeamMember(data) {
        try {
            const result = await apiClient.post('/team', data);
            showNotification('Team member added successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to add team member: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // BOT ACTIONS
    // ------------------------------------------------------------------------

    async runBot(botName, params = {}) {
        try {
            const result = await apiClient.post(`/bots/${botName}/run`, params);
            showNotification(`Bot ${botName} started successfully`, 'success');
            return result;
        } catch (error) {
            showNotification(`Failed to run bot: ${error.message}`, 'error');
            throw error;
        }
    },

    async toggleBot(botName) {
        try {
            const result = await apiClient.post(`/bots/${botName}/toggle`);
            showNotification(`Bot ${botName} toggled`, 'success');
            return result;
        } catch (error) {
            showNotification(`Failed to toggle bot: ${error.message}`, 'error');
            throw error;
        }
    },

    async runAllBots(onlyActive = true) {
        try {
            const result = await apiClient.post('/bots/run-all', { only_active: onlyActive });
            showNotification(`Successfully ran ${result.successful} of ${result.total_bots} bots`, 'success');
            return result;
        } catch (error) {
            showNotification('Failed to run all bots: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // DEAL ACTIONS
    // ------------------------------------------------------------------------

    async createDeal(data) {
        try {
            const result = await apiClient.post('/deals', data);
            showNotification('Deal created successfully', 'success');
            return result;
        } catch (error) {
            showNotification('Failed to create deal: ' + error.message, 'error');
            throw error;
        }
    },

    async viewMetrics(timeRange = '30d') {
        try {
            const result = await apiClient.get(`/metrics/dashboard?range=${timeRange}`);
            return result;
        } catch (error) {
            showNotification('Failed to load metrics: ' + error.message, 'error');
            throw error;
        }
    },

    // ------------------------------------------------------------------------
    // STRATEGY ACTIONS
    // ------------------------------------------------------------------------

    async loadMarketStrategy(strategyType) {
        try {
            const result = await apiClient.get(`/strategy/markets?type=${strategyType}`);
            return result;
        } catch (error) {
            showNotification('Failed to load market strategy: ' + error.message, 'error');
            throw error;
        }
    },

    async loadLeadStrategy() {
        try {
            const result = await apiClient.get('/strategy/leads');
            return result;
        } catch (error) {
            showNotification('Failed to load lead strategy: ' + error.message, 'error');
            throw error;
        }
    },

    async loadListingStrategy() {
        try {
            const result = await apiClient.get('/strategy/listings');
            return result;
        } catch (error) {
            showNotification('Failed to load listing strategy: ' + error.message, 'error');
            throw error;
        }
    }
};

// ============================================================================
// BUTTON CLICK HANDLER
// ============================================================================

async function handleButtonClick(buttonId, action, params = {}) {
    if (buttonStateManager.isLoading(buttonId)) {
        return;
    }

    try {
        buttonStateManager.setLoading(buttonId, true);
        
        const result = await ButtonActions[action](params);
        
        buttonStateManager.setState(buttonId, {
            lastAction: action,
            lastResult: result,
            status: 'success'
        });

        return result;
    } catch (error) {
        buttonStateManager.setState(buttonId, {
            lastAction: action,
            lastError: error.message,
            status: 'error'
        });
        throw error;
    } finally {
        buttonStateManager.setLoading(buttonId, false);
    }
}

// ============================================================================
// BUTTON INITIALIZATION
// ============================================================================

function initializeButtons() {
    // Lead Generation Buttons
    document.querySelectorAll('[data-action="add-lead"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('addLeadModal');
        });
    });

    document.querySelectorAll('[data-action="call-fsbo"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const leadId = e.target.dataset.leadId;
            await handleButtonClick(btn.id, 'callFSBO', leadId);
        });
    });

    document.querySelectorAll('[data-action="call-expired"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const leadId = e.target.dataset.leadId;
            await handleButtonClick(btn.id, 'callExpired', leadId);
        });
    });

    // Appointment Buttons
    document.querySelectorAll('[data-action="schedule-appointment"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('scheduleAppointmentModal');
        });
    });

    document.querySelectorAll('[data-action="complete-appointment"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const apptId = e.target.dataset.apptId;
            showModal('completeAppointmentModal', { apptId });
        });
    });

    // Listing Buttons
    document.querySelectorAll('[data-action="create-listing"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('createListingModal');
        });
    });

    document.querySelectorAll('[data-action="update-price"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const listingId = e.target.dataset.listingId;
            showModal('updatePriceModal', { listingId });
        });
    });

    // Contract Buttons
    document.querySelectorAll('[data-action="create-contract"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('createContractModal');
        });
    });

    // Contact Buttons
    document.querySelectorAll('[data-action="add-contact"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('addContactModal');
        });
    });

    document.querySelectorAll('[data-action="tag-contact"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const contactId = e.target.dataset.contactId;
            showModal('tagContactModal', { contactId });
        });
    });

    // Goal Buttons
    document.querySelectorAll('[data-action="set-goal"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('setGoalModal');
        });
    });

    // Run All Bots Button
    document.querySelectorAll('[data-action="run-all-bots"]').forEach(btn => {
        btn.addEventListener('click', async () => {
            const result = await handleButtonClick(btn.id, 'runAllBots', true);
            if (result) {
                refreshBotStatus();
            }
        });
    });

    // Quick Actions Buttons
    document.querySelectorAll('[data-action="create-deal"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('createDealModal');
        });
    });

    document.querySelectorAll('[data-action="view-analytics"]').forEach(btn => {
        btn.addEventListener('click', async () => {
            // Navigate to analytics page
            window.location.href = '/analytics';
        });
    });

    document.querySelectorAll('[data-action="add-lend"]').forEach(btn => {
        btn.addEventListener('click', () => {
            showModal('addLendModal');
        });
    });

    // Bot Buttons
    document.querySelectorAll('[data-action="run-bot"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const botName = e.target.dataset.botName;
            await handleButtonClick(btn.id, 'runBot', botName);
        });
    });

    document.querySelectorAll('[data-action="toggle-bot"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const botName = e.target.dataset.botName;
            await handleButtonClick(btn.id, 'toggleBot', botName);
        });
    });

    // Strategy Buttons
    document.querySelectorAll('[data-action="load-market-strategy"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const strategyType = e.target.dataset.strategyType;
            const result = await handleButtonClick(btn.id, 'loadMarketStrategy', strategyType);
            displayMarketStrategy(result);
        });
    });
}

// ============================================================================
// MODAL MANAGEMENT
// ============================================================================

function showModal(modalId, data = {}) {
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.error(`Modal ${modalId} not found`);
        return;
    }

    // Populate modal with data if needed
    if (data) {
        Object.keys(data).forEach(key => {
            const input = modal.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });
    }

    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
    }
}

// ============================================================================
// NOTIFICATION SYSTEM
// ============================================================================

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container') || createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notification-container';
    container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    document.body.appendChild(container);
    return container;
}

// ============================================================================
// FORM SUBMISSION HANDLERS
// ============================================================================

function setupFormHandlers() {
    // Add Lead Form
    const addLeadForm = document.getElementById('addLeadForm');
    if (addLeadForm) {
        addLeadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addLeadForm);
            const data = Object.fromEntries(formData);
            
            try {
                await ButtonActions.addLead(data);
                hideModal('addLeadModal');
                addLeadForm.reset();
                refreshLeadsList();
            } catch (error) {
                console.error('Form submission error:', error);
            }
        });
    }

    // Create Deal Form
    const createDealForm = document.getElementById('createDealForm');
    if (createDealForm) {
        createDealForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(createDealForm);
            const data = Object.fromEntries(formData);
            
            try {
                await ButtonActions.createDeal(data);
                hideModal('createDealModal');
                createDealForm.reset();
                refreshDealsList();
            } catch (error) {
                console.error('Form submission error:', error);
            }
        });
    }

    // Schedule Appointment Form
    const scheduleApptForm = document.getElementById('scheduleAppointmentForm');
    if (scheduleApptForm) {
        scheduleApptForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(scheduleApptForm);
            const data = Object.fromEntries(formData);
            
            try {
                await ButtonActions.scheduleAppointment(data);
                hideModal('scheduleAppointmentModal');
                scheduleApptForm.reset();
                refreshAppointmentsList();
            } catch (error) {
                console.error('Form submission error:', error);
            }
        });
    }

    // Create Listing Form
    const createListingForm = document.getElementById('createListingForm');
    if (createListingForm) {
        createListingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(createListingForm);
            const data = Object.fromEntries(formData);
            
            try {
                await ButtonActions.createListing(data);
                hideModal('createListingModal');
                createListingForm.reset();
                refreshListingsList();
            } catch (error) {
                console.error('Form submission error:', error);
            }
        });
    }

    // Add Contact Form
    const addContactForm = document.getElementById('addContactForm');
    if (addContactForm) {
        addContactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addContactForm);
            const data = Object.fromEntries(formData);
            
            try {
                await ButtonActions.addContact(data);
                hideModal('addContactModal');
                addContactForm.reset();
                refreshContactsList();
            } catch (error) {
                console.error('Form submission error:', error);
            }
        });
    }

    // Add Lend Form
    const addLendForm = document.getElementById('addLendForm');
    if (addLendForm) {
        addLendForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addLendForm);
            const data = Object.fromEntries(formData);
            
            try {
                await ButtonActions.addLend(data);
                hideModal('addLendModal');
                addLendForm.reset();
                // Refresh relevant data if needed
                showNotification('Lender financing record created', 'success');
            } catch (error) {
                console.error('Form submission error:', error);
            }
        });
    }
}

// ============================================================================
// DATA REFRESH FUNCTIONS
// ============================================================================

async function refreshLeadsList() {
    try {
        const leads = await apiClient.get('/leads');
        updateLeadsTable(leads);
    } catch (error) {
        console.error('Failed to refresh leads:', error);
    }
}

async function refreshAppointmentsList() {
    try {
        const appointments = await apiClient.get('/appointments');
        updateAppointmentsTable(appointments);
    } catch (error) {
        console.error('Failed to refresh appointments:', error);
    }
}

async function refreshListingsList() {
    try {
        const listings = await apiClient.get('/listings');
        updateListingsTable(listings);
    } catch (error) {
        console.error('Failed to refresh listings:', error);
    }
}

async function refreshContactsList() {
    try {
        const contacts = await apiClient.get('/contacts');
        updateContactsTable(contacts);
    } catch (error) {
        console.error('Failed to refresh contacts:', error);
    }
}

async function refreshDealsList() {
    try {
        const deals = await apiClient.get('/deals');
        updateDealsTable(deals);
    } catch (error) {
        console.error('Failed to refresh deals:', error);
    }
}

async function refreshLeadsList() {
    try {
        const leads = await apiClient.get('/leads');
        updateLeadsTable(leads);
    } catch (error) {
        console.error('Failed to refresh leads:', error);
    }
}

function displayMetricsDashboard(data) {
    // Navigate to analytics page or show modal with metrics
    if (window.location.pathname !== '/analytics') {
        window.location.href = '/analytics';
    }
}

async function refreshBotStatus() {
    try {
        const bots = await apiClient.get('/bots/status');
        updateBotsStatus(bots);
    } catch (error) {
        console.error('Failed to refresh bot status:', error);
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeButtons();
    setupFormHandlers();
    console.log('Button configuration system initialized');
});

// Export for use in other modules
window.ButtonActions = ButtonActions;
window.buttonStateManager = buttonStateManager;
window.apiClient = apiClient;
window.handleButtonClick = handleButtonClick;
