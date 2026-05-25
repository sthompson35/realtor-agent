/**
 * Realtor Agent Web Interface - Main JavaScript
 */

// Global variables
let currentPage = window.location.pathname;
let refreshInterval = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    startAutoRefresh();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set active navigation
    setActiveNavigation();

    // Initialize tooltips
    initializeTooltips();

    // Initialize popovers
    initializePopovers();

    // Load initial data if on dashboard
    if (currentPage === '/' || currentPage === '/dashboard') {
        loadDashboardData();
    }

    // Show welcome message
    showWelcomeMessage();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Auto-refresh toggle
    const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.addEventListener('change', toggleAutoRefresh);
    }

    // Search functionality
    const searchInput = document.getElementById('global-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }

    // Bot control buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.bot-control-btn')) {
            handleBotControl(e.target);
        }
    });

    // Deal action buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.deal-action-btn')) {
            handleDealAction(e.target);
        }
    });

    // Modal triggers
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-bs-toggle="modal"]')) {
            handleModalTrigger(e.target);
        }
    });

    // Quick action buttons
    document.addEventListener('click', function(e) {
        const button = e.target.closest('[data-action]');
        if (button) {
            handleQuickAction(button.dataset.action, button);
        }
    });
}

/**
 * Set active navigation based on current page
 */
function setActiveNavigation() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const dropdownItems = document.querySelectorAll('.navbar-nav .dropdown-item');
    const normalizedPath = currentPage === '/' ? '/' : currentPage.replace(/\/+$/, '');

    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    dropdownItems.forEach(item => {
        item.classList.remove('active');
    });

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;

        const normalizedHref = href === '/' ? '/' : href.replace(/\/+$/, '');
        const isMatch = normalizedPath === normalizedHref
            || (normalizedHref !== '/' && normalizedPath.startsWith(`${normalizedHref}/`));

        if (isMatch) {
            link.classList.add('active');
        }
    });

    dropdownItems.forEach(item => {
        const href = item.getAttribute('href');
        if (!href || href === '#') return;

        const normalizedHref = href === '/' ? '/' : href.replace(/\/+$/, '');
        const isMatch = normalizedPath === normalizedHref
            || (normalizedHref !== '/' && normalizedPath.startsWith(`${normalizedHref}/`));

        if (isMatch) {
            item.classList.add('active');
        }
    });

    // Mark dropdown toggle as active when one of its items is active
    document.querySelectorAll('.navbar-nav .dropdown').forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const hasActiveChild = dropdown.querySelector('.dropdown-item.active');
        if (toggle && hasActiveChild) {
            toggle.classList.add('active');
        }
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Show welcome message
 */
function showWelcomeMessage() {
    const lastLogin = localStorage.getItem('lastLogin');
    const now = new Date().toISOString();

    if (!lastLogin || isNewDay(lastLogin, now)) {
        showAlert('Welcome back to Realtor Agent!', 'success');
        localStorage.setItem('lastLogin', now);
    }
}

/**
 * Check if it's a new day
 */
function isNewDay(lastLogin, now) {
    const last = new Date(lastLogin);
    const current = new Date(now);
    return last.toDateString() !== current.toDateString();
}

/**
 * Load dashboard data
 */
async function loadDashboardData() {
    try {
        // Show loading state
        showLoadingState();

        // Simulate API calls (replace with real API calls)
        const [stats, deals, bots, excelDashboard, excelLeads, excelContacts, excelTimeline] = await Promise.all([
            fetchDashboardStats(),
            fetchRecentDeals(),
            fetchBotStatus(),
            fetchExcelDashboard(),
            fetchExcelLeads(),
            fetchExcelContacts(),
            fetchExcelDevelopmentTimeline()
        ]);

        // Update dashboard
        updateDashboardStats(stats);
        updateRecentDeals(deals);
        updateBotStatus(bots);
        updateExcelDashboard(excelDashboard);
        updateExcelLeads(excelLeads);
        updateExcelContacts(excelContacts);
        updateExcelDevelopmentTimeline(excelTimeline);
        updateDashboardTimestamp();

        // Hide loading state
        hideLoadingState();

    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showAlert('Failed to load dashboard data', 'danger');
        hideLoadingState();
    }

    function updateDashboardTimestamp() {
        const timestamp = document.getElementById('dashboard-last-updated');
        if (!timestamp) return;
        timestamp.textContent = new Date().toLocaleTimeString([], {
            hour: 'numeric',
            minute: '2-digit'
        });
    }
}

/**
 * Fetch dashboard statistics
 */
async function fetchDashboardStats() {
    const response = await fetch('/api/stats');
    if (!response.ok) {
        throw new Error('Failed to fetch stats');
    }
    return await response.json();
}

/**
 * Fetch recent deals
 */
async function fetchRecentDeals() {
    const response = await fetch('/api/deals');
    if (!response.ok) {
        throw new Error('Failed to fetch deals');
    }
    const deals = await response.json();
    // Return the first 5 deals or all if less
    return (deals.deals || []).slice(0, 5);
}

/**
 * Fetch bot status
 */
async function fetchBotStatus() {
    const response = await fetch('/api/bots/status');
    if (!response.ok) {
        throw new Error('Failed to fetch bots');
    }
    const bots = await response.json();
    // Response is already an array of bot objects
    return (Array.isArray(bots) ? bots : Object.values(bots)).map(data => ({
        name: data.name || data.display_name,
        status: data.status,
        last_run: data.last_run
    }));
}

/**
 * Update dashboard statistics
 */
function updateDashboardStats(stats) {
    // Update stat cards
    updateStatCard('total-deals', stats.total_deals, 'Total Deals');
    updateStatCard('active-deals', stats.active_deals, 'Active Deals');
    updateStatCard('monthly-revenue', `$${(stats.avg_deal_size || 0).toLocaleString()}`, 'Avg Deal Size');
    updateStatCard('success-rate', `${stats.success_rate || 0}%`, 'Success Rate');
    updateStatCard('avg-deal-size', `$${(stats.avg_deal_size || 0).toLocaleString()}`, 'Avg Deal Size');
    updateStatCard('pending-offers', stats.avg_days_to_close, 'Avg Days to Close');
}

/**
 * Update a stat card
 */
function updateStatCard(id, value, label) {
    const element = document.getElementById(id);
    if (element) {
        element.innerHTML = `
            <div class="stat-value">${value}</div>
            <div class="stat-label">${label}</div>
        `;
    }
}

/**
 * Update recent deals
 */
function updateRecentDeals(deals) {
    const container = document.getElementById('recent-deals-list');
    if (!container) return;

    container.innerHTML = deals.map(deal => `
        <div class="deal-card ${deal.status} fade-in">
            <div class="deal-address">${deal.address}</div>
            <div class="deal-price">$${(deal.contract_price || 0).toLocaleString()}</div>
            <div class="deal-meta">
                <span><i class="fas fa-calendar me-1"></i>${formatDate(deal.created_at)}</span>
                <span class="badge bg-${getStatusColor(deal.status)}">${formatStatus(deal.status)}</span>
            </div>
        </div>
    `).join('');
}

/**
 * Update bot status
 */
function updateBotStatus(bots) {
    const container = document.getElementById('bot-status-grid');
    if (!container) return;

    container.innerHTML = bots.map(bot => `
        <div class="bot-card ${bot.status} fade-in">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <div class="bot-name">${formatBotName(bot.name)}</div>
                    <div class="bot-status">
                        <i class="fas fa-circle me-1 ${bot.status === 'active' ? 'text-success' : 'text-secondary'}"></i>
                        ${bot.status === 'active' ? 'Active' : 'Inactive'}
                    </div>
                </div>
                <button class="btn btn-sm btn-outline-primary bot-control-btn"
                        data-bot="${bot.name}"
                        data-action="${bot.status === 'active' ? 'stop' : 'start'}">
                    <i class="fas fa-${bot.status === 'active' ? 'stop' : 'play'}"></i>
                </button>
            </div>
            <div class="bot-metrics">
                <div class="metric">
                    <div class="metric-value">${bot.last_run ? formatDate(bot.last_run) : 'Never'}</div>
                    <div class="metric-label">last run</div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Handle bot control actions
 */
async function handleBotControl(button) {
    const botName = button.dataset.bot;
    const action = button.dataset.action;

    // Show loading state
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    try {
        const response = await fetch(`/api/bots/${botName}/toggle`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to toggle bot');
        }

        const result = await response.json();

        // Update button state based on new status
        const newStatus = result.new_status;
        if (newStatus === 'active') {
            button.innerHTML = '<i class="fas fa-stop"></i>';
            button.dataset.action = 'stop';
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-outline-danger');
        } else {
            button.innerHTML = '<i class="fas fa-play"></i>';
            button.dataset.action = 'start';
            button.classList.remove('btn-outline-danger');
            button.classList.add('btn-outline-primary');
        }

        button.disabled = false;

        // Show success message
        showAlert(`Bot ${botName} ${newStatus === 'active' ? 'started' : 'stopped'} successfully`, 'success');

        // Reload bot status
        loadDashboardData();

    } catch (error) {
        console.error('Error toggling bot:', error);
        showAlert('Failed to toggle bot', 'danger');
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
    }
}

/**
 * Handle deal actions
 */
function handleDealAction(button) {
    const dealId = button.dataset.dealId;
    const action = button.dataset.action;

    showAlert(`Deal ${dealId} ${action} action triggered`, 'info');
}

/**
 * Handle modal triggers
 */
function handleModalTrigger(button) {
    const target = button.dataset.bsTarget;
    const modal = document.querySelector(target);

    if (modal) {
        // Load modal content if needed
        const contentUrl = button.dataset.contentUrl;
        if (contentUrl) {
            loadModalContent(modal, contentUrl);
        }
    }
}

/**
 * Handle quick action buttons
 */
function handleQuickAction(action, button) {
    switch (action) {
        case 'create-deal':
            // Show create deal modal
            const createDealModal = new bootstrap.Modal(document.getElementById('createDealModal'));
            createDealModal.show();
            break;

        case 'scrape-leads':
            // Show scrape leads modal
            const scrapeLeadsModal = new bootstrap.Modal(document.getElementById('scrapeLeadsModal'));
            scrapeLeadsModal.show();
            break;

        case 'run-all-bots':
            showAlert('Bot execution feature coming soon!', 'info');
            break;

        case 'view-metrics':
            window.location.href = '/analytics';
            break;

        case 'add-lead':
            // Show add lead modal
            const addLeadModal = new bootstrap.Modal(document.getElementById('addLeadModal'));
            addLeadModal.show();
            break;

        default:
            showAlert(`Action "${action}" not implemented yet`, 'warning');
    }
}

/**
 * Load modal content
 */
async function loadModalContent(modal, url) {
    try {
        const response = await fetch(url);
        const content = await response.text();

        const modalBody = modal.querySelector('.modal-body');
        if (modalBody) {
            modalBody.innerHTML = content;
        }
    } catch (error) {
        console.error('Error loading modal content:', error);
        showAlert('Failed to load modal content', 'danger');
    }
}

/**
 * Handle search
 */
function handleSearch(event) {
    const query = event.target.value.toLowerCase();

    // Filter visible elements based on search query
    const searchableElements = document.querySelectorAll('.deal-card, .bot-card');

    searchableElements.forEach(element => {
        const text = element.textContent.toLowerCase();
        if (text.includes(query)) {
            element.style.display = '';
        } else {
            element.style.display = 'none';
        }
    });
}

/**
 * Toggle auto-refresh
 */
function toggleAutoRefresh(event) {
    if (event.target.checked) {
        startAutoRefresh();
        showAlert('Auto-refresh enabled', 'success');
    } else {
        stopAutoRefresh();
        showAlert('Auto-refresh disabled', 'info');
    }
}

/**
 * Start auto-refresh
 */
function startAutoRefresh() {
    if (refreshInterval) return;

    refreshInterval = setInterval(() => {
        if (currentPage === '/' || currentPage === '/dashboard') {
            loadDashboardData();
        }
    }, 30000); // Refresh every 30 seconds
}

/**
 * Stop auto-refresh
 */
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

/**
 * Show loading state
 */
function showLoadingState() {
    const loadingElements = document.querySelectorAll('.loading-placeholder');
    loadingElements.forEach(element => {
        element.style.display = '';
        element.classList.add('opacity-75');
        element.setAttribute('aria-busy', 'true');
    });
}

/**
 * Hide loading state
 */
function hideLoadingState() {
    const loadingElements = document.querySelectorAll('.loading-placeholder');
    loadingElements.forEach(element => {
        element.classList.remove('opacity-75');
        element.removeAttribute('aria-busy');
    });
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;

    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show slide-in-left" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    alertContainer.insertAdjacentHTML('beforeend', alertHtml);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

/**
 * Format status
 */
function formatStatus(status) {
    return status.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

/**
 * Get status color
 */
function getStatusColor(status) {
    const colors = {
        'lead': 'info',
        'under_contract': 'warning',
        'closed': 'success',
        'rejected': 'danger'
    };
    return colors[status] || 'secondary';
}

/**
 * Format bot name
 */
function formatBotName(botName) {
    return botName.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

/**
 * Debounce function
 */
function debounce(func, wait) {
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

/**
 * Utility function to format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

/**
 * Utility function to format percentage
 */
function formatPercentage(value) {
    return `${value.toFixed(1)}%`;
}

// ============================================================================
// EXCEL DATA INTEGRATION FUNCTIONS
// ============================================================================

/**
 * Fetch Excel dashboard data
 */
async function fetchExcelDashboard() {
    try {
        const response = await fetch('/api/excel/dashboard');
        if (!response.ok) {
            throw new Error('Failed to fetch Excel dashboard');
        }
        return await response.json();
    } catch (error) {
        console.warn('Excel dashboard not available:', error);
        return { dashboard: { metrics: {}, charts: {}, summary: {} } };
    }
}

/**
 * Fetch Excel leads data
 */
async function fetchExcelLeads() {
    try {
        const response = await fetch('/api/excel/leads');
        if (!response.ok) {
            throw new Error('Failed to fetch Excel leads');
        }
        return await response.json();
    } catch (error) {
        console.warn('Excel leads not available:', error);
        return { leads: [], total_leads: 0 };
    }
}

/**
 * Fetch Excel contacts data
 */
async function fetchExcelContacts() {
    try {
        const response = await fetch('/api/excel/contacts');
        if (!response.ok) {
            throw new Error('Failed to fetch Excel contacts');
        }
        return await response.json();
    } catch (error) {
        console.warn('Excel contacts not available:', error);
        return { contacts: [], total_contacts: 0 };
    }
}

/**
 * Fetch Excel development timeline data
 */
async function fetchExcelDevelopmentTimeline() {
    try {
        const response = await fetch('/api/excel/development-timeline');
        if (!response.ok) {
            throw new Error('Failed to fetch Excel development timeline');
        }
        return await response.json();
    } catch (error) {
        console.warn('Excel development timeline not available:', error);
        return { phases: [], total_phases: 0, additional_info: {} };
    }
}

/**
 * Update Excel dashboard metrics display
 */
function updateExcelDashboard(data) {
    const container = document.getElementById('excel-dashboard-metrics');
    if (!container) return;

    const metrics = data.dashboard?.metrics || {};

    if (Object.keys(metrics).length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted py-3">
                <i class="fas fa-chart-line fa-2x mb-2"></i>
                <p>No dashboard metrics available</p>
            </div>
        `;
        return;
    }

    const metricsHtml = Object.entries(metrics).map(([key, value]) => `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted">${key}</span>
            <span class="fw-bold">${value || 'N/A'}</span>
        </div>
    `).join('');

    container.innerHTML = `
        <div class="excel-metrics">
            ${metricsHtml}
        </div>
        <div class="text-end mt-2">
            <small class="text-muted">Last updated: ${new Date(data.last_updated).toLocaleTimeString()}</small>
        </div>
    `;
}

/**
 * Update Excel leads display
 */
function updateExcelLeads(data) {
    const container = document.getElementById('excel-leads-list');
    const countElement = document.getElementById('excel-leads-count');
    if (!container || !countElement) return;

    const leads = data.leads || [];
    countElement.textContent = `${data.total_leads || 0} leads`;

    if (leads.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted py-3">
                <i class="fas fa-users fa-2x mb-2"></i>
                <p>No leads found in Excel</p>
            </div>
        `;
        return;
    }

    const leadsHtml = leads.slice(0, 5).map(lead => `
        <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
            <div>
                <div class="fw-bold">${lead['Lead ID'] || 'Unknown'}</div>
                <small class="text-muted">${lead['Owner Name'] || ''} ${lead['Property Address/APN'] || ''}</small>
            </div>
            <span class="badge bg-${getStatusColor(lead.Status)}">${lead.Status || 'New'}</span>
        </div>
    `).join('');

    container.innerHTML = `
        ${leadsHtml}
        ${leads.length > 5 ? `<div class="text-center mt-2"><small class="text-muted">Showing 5 of ${leads.length} leads</small></div>` : ''}
    `;
}

/**
 * Update Excel contacts display
 */
function updateExcelContacts(data) {
    const container = document.getElementById('excel-contacts-list');
    const countElement = document.getElementById('excel-contacts-count');
    if (!container || !countElement) return;

    const contacts = data.contacts || [];
    countElement.textContent = `${data.total_contacts || 0} contacts`;

    if (contacts.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted py-3">
                <i class="fas fa-address-book fa-2x mb-2"></i>
                <p>No contacts found in Excel</p>
            </div>
        `;
        return;
    }

    const contactsHtml = contacts.slice(0, 5).map(contact => `
        <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
            <div>
                <div class="fw-bold">${Object.values(contact)[1] || 'Contact'}</div>
                <small class="text-muted">${Object.values(contact)[0] || ''}</small>
            </div>
            <i class="fas fa-user text-muted"></i>
        </div>
    `).join('');

    container.innerHTML = `
        ${contactsHtml}
        ${contacts.length > 5 ? `<div class="text-center mt-2"><small class="text-muted">Showing 5 of ${contacts.length} contacts</small></div>` : ''}
    `;
}

/**
 * Update Excel development timeline display
 */
function updateExcelDevelopmentTimeline(data) {
    const container = document.getElementById('excel-development-timeline');
    const countElement = document.getElementById('excel-timeline-count');
    if (!container || !countElement) return;

    const phases = data.phases || [];
    countElement.textContent = `${data.total_phases || 0} phases`;

    if (phases.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted py-3">
                <i class="fas fa-road fa-2x mb-2"></i>
                <p>No development phases found in Excel</p>
            </div>
        `;
        return;
    }

    const phasesHtml = phases.map((phase, index) => `
        <div class="phase-card mb-4">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h6 class="mb-1">${phase.Phase || `Phase ${index + 1}`}</h6>
                    <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>${phase.Timeframe || 'TBD'} |
                        <i class="fas fa-calendar me-1"></i>${phase['Week Range'] || 'TBD'}
                    </small>
                </div>
                <span class="badge bg-primary">Phase ${index + 1}</span>
            </div>

            <div class="row">
                <div class="col-md-6 mb-3">
                    <h6 class="text-primary mb-2"><i class="fas fa-tasks me-1"></i>Key Activities</h6>
                    <div class="activity-list">
                        ${formatActivities(phase['Key Activities'] || '')}
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <h6 class="text-success mb-2"><i class="fas fa-users me-1"></i>Stakeholders</h6>
                    <p class="mb-2">${phase['Main Stakeholders'] || 'TBD'}</p>

                    <h6 class="text-warning mb-2"><i class="fas fa-dollar-sign me-1"></i>Budget</h6>
                    <p class="mb-0">${phase['Budget Considerations'] || 'TBD'}</p>
                </div>
            </div>
        </div>
    `).join('');

    // Add additional info section
    const additionalInfo = data.additional_info || {};
    const milestonesHtml = additionalInfo.financial_milestones?.map(milestone =>
        `<li class="mb-1">${milestone}</li>`
    ).join('') || '';

    const factorsHtml = additionalInfo.critical_success_factors?.map(factor =>
        `<li class="mb-1">${factor}</li>`
    ).join('') || '';

    const additionalHtml = milestonesHtml || factorsHtml ? `
        <div class="row mt-4">
            <div class="col-12">
                <div class="card bg-light">
                    <div class="card-body">
                        ${milestonesHtml ? `
                            <h6 class="text-primary mb-3"><i class="fas fa-chart-line me-1"></i>Key Financial Milestones</h6>
                            <ul class="mb-3">${milestonesHtml}</ul>
                        ` : ''}
                        ${factorsHtml ? `
                            <h6 class="text-success mb-3"><i class="fas fa-check-circle me-1"></i>Critical Success Factors</h6>
                            <ul class="mb-0">${factorsHtml}</ul>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    ` : '';

    container.innerHTML = `
        <div class="development-timeline">
            ${phasesHtml}
            ${additionalHtml}
        </div>
    `;
}

/**
 * Format activities text with bullet points
 */
function formatActivities(activitiesText) {
    if (!activitiesText) return '<p class="text-muted">No activities specified</p>';

    const activities = activitiesText.split('\n').filter(activity => activity.trim());
    return activities.map(activity =>
        `<div class="activity-item">• ${activity.replace('•', '').trim()}</div>`
    ).join('');
}

/**
 * Get status color for badges
 */
function getStatusColor(status) {
    if (!status) return 'secondary';
    const statusLower = status.toLowerCase();
    if (statusLower.includes('new') || statusLower.includes('lead')) return 'primary';
    if (statusLower.includes('contact') || statusLower.includes('active')) return 'warning';
    if (statusLower.includes('close') || statusLower.includes('won')) return 'success';
    if (statusLower.includes('lost') || statusLower.includes('reject')) return 'danger';
    return 'secondary';
}

// ============================================================================
// PDF PROCESSING FUNCTIONS
// ============================================================================

/**
 * Load PDF Master Guide content
 */
function loadPDFGuide() {
    const overviewElement = document.getElementById('pdf-guide-overview');
    const sectionsElement = document.getElementById('pdf-key-sections');

    if (!overviewElement || !sectionsElement) return;

    // Show loading state
    overviewElement.innerHTML = `
        <div class="text-center text-muted py-4">
            <i class="fas fa-spinner fa-spin fa-2x mb-3"></i>
            <p>Loading Real Estate Investment Master Guide...</p>
        </div>
    `;

    // Load PDF content
    fetch('/api/pdf/master-guide')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            // Update overview
            overviewElement.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="text-primary mb-2">${data.title}</h6>
                        <p class="mb-1"><strong>Pages:</strong> ${data.total_pages}</p>
                        <p class="mb-1"><strong>Total Words:</strong> ${data.summary.total_words.toLocaleString()}</p>
                        <p class="mb-0"><small class="text-muted">Last updated: ${new Date(data.summary.last_updated).toLocaleDateString()}</small></p>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-success mb-2">Key Sections (${data.summary.key_sections.length})</h6>
                        <div class="small">
                            ${data.summary.key_sections.slice(0, 5).map(section =>
                                `<div class="mb-1"><strong>${section.title}</strong></div>`
                            ).join('')}
                            ${data.summary.key_sections.length > 5 ? '<div class="text-muted">...and more</div>' : ''}
                        </div>
                    </div>
                </div>
            `;

            // Update key sections
            sectionsElement.innerHTML = `
                <h6 class="text-muted mb-2">Key Sections:</h6>
                <div class="list-group list-group-flush">
                    ${data.summary.key_sections.map(section => `
                        <div class="list-group-item px-0 py-2">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <strong class="text-dark">${section.title}</strong>
                                    <p class="mb-0 small text-muted">${section.content}</p>
                                </div>
                                <button class="btn btn-sm btn-outline-primary" onclick="RealtorAgent.viewPDFSection('${section.title}')">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            // Store full content for later use
            window.pdfGuideData = data;

            showAlert('PDF Master Guide loaded successfully!', 'success');
        })
        .catch(error => {
            overviewElement.innerHTML = `
                <div class="text-center text-danger py-4">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <p>Failed to load PDF Guide</p>
                    <small class="text-muted">${error.message}</small>
                </div>
            `;
            showAlert('Failed to load PDF Master Guide: ' + error.message, 'error');
        });
}

/**
 * Search PDF content
 */
function searchPDFGuide() {
    const searchInput = document.getElementById('pdf-search-input');
    const resultsElement = document.getElementById('pdf-search-results');
    const contentElement = document.getElementById('pdf-search-content');

    if (!searchInput || !resultsElement || !contentElement) return;

    const query = searchInput.value.trim();
    if (!query) {
        showAlert('Please enter a search term', 'warning');
        return;
    }

    // Show loading
    contentElement.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    resultsElement.style.display = 'block';

    fetch(`/api/pdf/master-guide/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            if (data.total_matches === 0) {
                contentElement.innerHTML = '<div class="text-muted">No matches found for "' + query + '"</div>';
                return;
            }

            contentElement.innerHTML = `
                <div class="mb-2">
                    <strong>${data.total_matches} match${data.total_matches !== 1 ? 'es' : ''} found</strong>
                </div>
                ${data.results.map(result => `
                    <div class="border-start border-primary border-3 ps-3 mb-3">
                        <div class="small text-muted mb-1">Page ${result.page_number}</div>
                        ${result.matches.map(match => `
                            <div class="mb-2">
                                <div class="bg-light p-2 rounded small">
                                    ${match.context.replace(new RegExp(query, 'gi'), '<mark>$&</mark>')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `).join('')}
            `;
        })
        .catch(error => {
            contentElement.innerHTML = '<div class="text-danger">Search failed: ' + error.message + '</div>';
            showAlert('Search failed: ' + error.message, 'error');
        });
}

/**
 * Toggle PDF content viewer
 */
function togglePDFView() {
    const viewer = document.getElementById('pdf-content-viewer');
    const content = document.getElementById('pdf-full-content');

    if (!viewer || !content) return;

    if (viewer.style.display === 'none') {
        // Show viewer
        if (!window.pdfGuideData) {
            showAlert('Please load the PDF guide first', 'warning');
            return;
        }

        // Render full content
        content.innerHTML = `
            <div class="row">
                ${window.pdfGuideData.pages.map(page => `
                    <div class="col-12 mb-4">
                        <div class="card">
                            <div class="card-header">
                                <h6 class="mb-0">Page ${page.page_number} <small class="text-muted">(${page.word_count} words)</small></h6>
                            </div>
                            <div class="card-body">
                                <div class="pdf-content">
                                    ${page.content.split('\n').map(paragraph =>
                                        paragraph.trim() ? `<p class="mb-2">${paragraph}</p>` : ''
                                    ).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        viewer.style.display = 'block';
        viewer.scrollIntoView({ behavior: 'smooth' });
    } else {
        // Hide viewer
        viewer.style.display = 'none';
    }
}

/**
 * View specific PDF section
 */
function viewPDFSection(sectionTitle) {
    if (!window.pdfGuideData) {
        showAlert('Please load the PDF guide first', 'warning');
        return;
    }

    // Find the section in the data
    const section = window.pdfGuideData.summary.key_sections.find(s =>
        s.title === sectionTitle
    );

    if (section) {
        // Show modal or scroll to section
        const modalContent = `
            <div class="modal fade" id="pdfSectionModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${section.title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${section.content}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" onclick="RealtorAgent.togglePDFView()">View Full Guide</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if present
        const existingModal = document.getElementById('pdfSectionModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalContent);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('pdfSectionModal'));
        modal.show();
    }
}

// ============================================================================
// EXCEL LEAD MANAGEMENT FUNCTIONS
// ============================================================================

/**
 * Add a new lead to Excel
 */
function addExcelLead(leadData) {
    return fetch('/api/excel/leads', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(leadData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    });
}

/**
 * Handle add lead form submission
 */
function handleAddLeadForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Convert form data to object
    const leadData = {};
    for (let [key, value] of formData.entries()) {
        if (value.trim()) {  // Only include non-empty values
            leadData[key] = value.trim();
        }
    }

    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Adding Lead...';
    submitBtn.disabled = true;

    // Add the lead
    addExcelLead(leadData)
        .then(result => {
            if (result.success) {
                showAlert(`Lead "${result.lead_id}" added successfully!`, 'success');

                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addLeadModal'));
                if (modal) {
                    modal.hide();
                }

                // Reset form
                form.reset();

                // Refresh leads data
                loadDashboardData();
            } else {
                throw new Error(result.error || 'Failed to add lead');
            }
        })
        .catch(error => {
            console.error('Error adding lead:', error);
            showAlert('Failed to add lead: ' + error.message, 'error');
        })
        .finally(() => {
            // Restore button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
}

/**
 * Handle scrape leads form submission
 */
function handleScrapeLeadsForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const numLeads = parseInt(formData.get('num_leads'));

    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Generating Leads...';
    submitBtn.disabled = true;

    // Show progress alert
    showAlert(`Generating ${numLeads} test leads... This may take a few seconds.`, 'info');

    // Scrape and add leads
    scrapeAndAddLeads(numLeads)
        .then(result => {
            if (result.success) {
                showAlert(`Successfully generated and added ${result.added_leads} test leads to your CRM!`, 'success');

                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('scrapeLeadsModal'));
                if (modal) {
                    modal.hide();
                }

                // Reset form
                form.reset();

                // Refresh leads data
                loadDashboardData();

                // Show summary
                setTimeout(() => {
                    const summary = result.leads.slice(0, 3).map(lead =>
                        `${lead.owner_name} (${lead.source}) - $${lead.estimated_value}`
                    ).join('\n• ');

                    showAlert(`Sample leads added:\n• ${summary}${result.leads.length > 3 ? '\n• ...and more' : ''}`, 'success');
                }, 1000);

            } else {
                throw new Error(result.error || 'Failed to generate leads');
            }
        })
        .catch(error => {
            console.error('Error scraping leads:', error);
            showAlert('Failed to generate leads: ' + error.message, 'error');
        })
        .finally(() => {
            // Restore button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
}

/**
 * Scrape leads from the internet and add to Excel
 */
function scrapeAndAddLeads(numLeads) {
    return fetch('/api/scrape/leads', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ num_leads: numLeads })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    });
}

// Export functions for global use
window.RealtorAgent = {
    showAlert,
    formatCurrency,
    formatPercentage,
    loadDashboardData,
    loadPDFGuide,
    searchPDFGuide,
    togglePDFView,
    viewPDFSection,
    addExcelLead,
    handleAddLeadForm,
    handleScrapeLeadsForm,
    scrapeAndAddLeads
};