// NEXUS Assistant Interface - Personal Life Management

class NEXUSAssistant {
    constructor() {
        this.currentTab = 'overview';
        this.socket = io();
        this.calendar = null;
        this.tasks = [];
        this.expenses = [];
        this.contacts = [];
        
        this.init();
    }
    
    init() {
        console.log('🤖 NEXUS Assistant Interface Initializing...');
        
        this.setupEventListeners();
        this.setupWebSocket();
        this.initializeCalendar();
        this.loadData();
        
        console.log('✅ NEXUS Assistant Interface Ready');
    }
    
    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const tabName = btn.dataset.tab;
                this.switchTab(tabName);
            });
        });
        
        // Quick actions
        document.querySelectorAll('.action-button').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.executeAction(action);
            });
        });
        
        // Add buttons
        const addTaskBtn = document.getElementById('addTaskBtn');
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', () => this.showAddTaskModal());
        }
        
        const addExpenseBtn = document.getElementById('addExpenseBtn');
        if (addExpenseBtn) {
            addExpenseBtn.addEventListener('click', () => this.showAddExpenseModal());
        }
        
        const addContactBtn = document.getElementById('addContactBtn');
        if (addContactBtn) {
            addContactBtn.addEventListener('click', () => this.showAddContactModal());
        }
        
        // Task filters
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.filterTasks(btn.dataset.filter);
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
        
        // Contact search
        const contactSearch = document.getElementById('contactSearch');
        if (contactSearch) {
            contactSearch.addEventListener('input', (e) => {
                this.searchContacts(e.target.value);
            });
        }
        
        // Calendar navigation
        const prevMonth = document.getElementById('prevMonth');
        const nextMonth = document.getElementById('nextMonth');
        
        if (prevMonth) {
            prevMonth.addEventListener('click', () => this.navigateCalendar(-1));
        }
        
        if (nextMonth) {
            nextMonth.addEventListener('click', () => this.navigateCalendar(1));
        }
    }
    
    setupWebSocket() {
        this.socket.on('connect', () => {
            console.log('🌐 Assistant connected to NEXUS server');
        });
        
        this.socket.on('assistant_update', (data) => {
            this.handleAssistantUpdate(data);
        });
        
        this.socket.on('data_sync', (data) => {
            this.syncData(data);
        });
    }
    
    switchTab(tabName) {
        console.log('📋 Switching to tab:', tabName);
        
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        const targetTab = document.getElementById(tabName);
        if (targetTab) {
            targetTab.classList.add('active');
        }
        
        this.currentTab = tabName;
        
        // Trigger tab-specific initialization
        this.onTabSwitch(tabName);
    }
    
    onTabSwitch(tabName) {
        switch (tabName) {
            case 'calendar':
                this.refreshCalendar();
                break;
            case 'tasks':
                this.refreshTasks();
                break;
            case 'expenses':
                this.refreshExpenses();
                break;
            case 'health':
                this.refreshHealthData();
                break;
            case 'contacts':
                this.refreshContacts();
                break;
        }
    }
    
    executeAction(action) {
        console.log('⚡ Executing action:', action);
        
        switch (action) {
            case 'add-meeting':
                this.showAddEventModal();
                break;
            case 'add-task':
                this.showAddTaskModal();
                break;
            case 'add-expense':
                this.showAddExpenseModal();
                break;
            case 'log-workout':
                this.showLogWorkoutModal();
                break;
        }
        
        // Show Jarvis animation
        this.showJarvisAnimation();
        setTimeout(() => this.hideJarvisAnimation(), 2000);
    }
    
    initializeCalendar() {
        this.calendar = {
            currentMonth: new Date().getMonth(),
            currentYear: new Date().getFullYear(),
            events: [
                {
                    date: new Date(),
                    title: 'Team Standup',
                    time: '09:00 AM',
                    description: 'Daily team synchronization'
                },
                {
                    date: new Date(),
                    title: 'Client Meeting',
                    time: '02:00 PM',
                    description: 'Project review and feedback'
                }
            ]
        };
        
        this.renderCalendar();
    }
    
    renderCalendar() {
        const calendarGrid = document.getElementById('calendarGrid');
        const currentMonthElement = document.getElementById('currentMonth');
        
        if (!calendarGrid || !currentMonthElement) return;
        
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        currentMonthElement.textContent = `${monthNames[this.calendar.currentMonth]} ${this.calendar.currentYear}`;
        
        // Clear existing calendar
        calendarGrid.innerHTML = '';
        
        // Add day headers
        const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        dayHeaders.forEach(day => {
            const dayHeader = document.createElement('div');
            dayHeader.className = 'calendar-day-header';
            dayHeader.textContent = day;
            calendarGrid.appendChild(dayHeader);
        });
        
        // Get first day of month and number of days
        const firstDay = new Date(this.calendar.currentYear, this.calendar.currentMonth, 1);
        const lastDay = new Date(this.calendar.currentYear, this.calendar.currentMonth + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();
        
        // Add empty cells for days before the first day of the month
        for (let i = 0; i < startingDayOfWeek; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            calendarGrid.appendChild(emptyDay);
        }
        
        // Add days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            
            // Check if this day has events
            const dayDate = new Date(this.calendar.currentYear, this.calendar.currentMonth, day);
            const hasEvents = this.calendar.events.some(event => 
                event.date.toDateString() === dayDate.toDateString()
            );
            
            if (hasEvents) {
                dayElement.classList.add('has-events');
            }
            
            // Highlight today
            const today = new Date();
            if (day === today.getDate() && 
                this.calendar.currentMonth === today.getMonth() && 
                this.calendar.currentYear === today.getFullYear()) {
                dayElement.classList.add('today');
            }
            
            calendarGrid.appendChild(dayElement);
        }
    }
    
    navigateCalendar(direction) {
        this.calendar.currentMonth += direction;
        
        if (this.calendar.currentMonth > 11) {
            this.calendar.currentMonth = 0;
            this.calendar.currentYear++;
        } else if (this.calendar.currentMonth < 0) {
            this.calendar.currentMonth = 11;
            this.calendar.currentYear--;
        }
        
        this.renderCalendar();
    }
    
    refreshCalendar() {
        this.renderCalendar();
        // Update events list
        this.updateEventsList();
    }
    
    updateEventsList() {
        const eventList = document.getElementById('eventList');
        if (!eventList) return;
        
        eventList.innerHTML = '';
        
        this.calendar.events.forEach(event => {
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            eventItem.innerHTML = `
                <div class="event-time">${event.time}</div>
                <div class="event-details">
                    <h5>${event.title}</h5>
                    <p>${event.description}</p>
                </div>
            `;
            eventList.appendChild(eventItem);
        });
    }
    
    refreshTasks() {
        console.log('📋 Refreshing tasks...');
        // Task refresh logic would go here
    }
    
    refreshExpenses() {
        console.log('💰 Refreshing expenses...');
        // Expense refresh logic would go here
    }
    
    refreshHealthData() {
        console.log('🏃 Refreshing health data...');
        // Health data refresh logic would go here
    }
    
    refreshContacts() {
        console.log('👥 Refreshing contacts...');
        // Contact refresh logic would go here
    }
    
    filterTasks(filter) {
        console.log('🔍 Filtering tasks:', filter);
        
        const taskItems = document.querySelectorAll('.task-item');
        taskItems.forEach(item => {
            const classes = item.classList;
            
            switch (filter) {
                case 'all':
                    item.style.display = 'flex';
                    break;
                case 'pending':
                    item.style.display = classes.contains('pending') ? 'flex' : 'none';
                    break;
                case 'completed':
                    item.style.display = classes.contains('completed') ? 'flex' : 'none';
                    break;
                case 'overdue':
                    item.style.display = classes.contains('overdue') ? 'flex' : 'none';
                    break;
            }
        });
    }
    
    searchContacts(query) {
        console.log('🔍 Searching contacts:', query);
        
        const contactItems = document.querySelectorAll('.contact-item');
        contactItems.forEach(item => {
            const name = item.querySelector('h4').textContent.toLowerCase();
            const email = item.querySelector('.contact-email').textContent.toLowerCase();
            
            if (name.includes(query.toLowerCase()) || email.includes(query.toLowerCase())) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    showAddTaskModal() {
        this.showNotification('Add Task modal would open here', 'info');
    }
    
    showAddExpenseModal() {
        this.showNotification('Add Expense modal would open here', 'info');
    }
    
    showAddContactModal() {
        this.showNotification('Add Contact modal would open here', 'info');
    }
    
    showAddEventModal() {
        this.showNotification('Add Event modal would open here', 'info');
    }
    
    showLogWorkoutModal() {
        this.showNotification('Log Workout modal would open here', 'info');
    }
    
    loadData() {
        // Load data from server or local storage
        console.log('📡 Loading assistant data...');
    }
    
    syncData(data) {
        console.log('🔄 Syncing data:', data);
    }
    
    handleAssistantUpdate(data) {
        console.log('🔄 Assistant update received:', data);
    }
    
    showJarvisAnimation() {
        const overlay = document.getElementById('jarvisOverlay');
        if (overlay) {
            overlay.classList.add('active');
        }
    }
    
    hideJarvisAnimation() {
        const overlay = document.getElementById('jarvisOverlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }
    
    showNotification(message, type = 'info') {
        // Reuse notification system from main app
        if (window.nexusApp) {
            window.nexusApp.showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }
}

// Initialize assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.nexusAssistant = new NEXUSAssistant();
});

// Add assistant-specific styles
const assistantStyles = `
/* Assistant-specific styles */
.assistant-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 120px);
    margin: var(--spacing-lg);
}

.assistant-tabs {
    display: flex;
    background: var(--glass-primary);
    backdrop-filter: blur(20px);
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
    border: 1px solid var(--glass-border);
    border-bottom: none;
    overflow-x: auto;
}

.tab-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.7);
    padding: var(--spacing-lg) var(--spacing-xl);
    cursor: pointer;
    transition: all var(--transition-normal);
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 0.9rem;
    font-weight: 500;
    position: relative;
}

.tab-btn::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--primary-color);
    transform: scaleX(0);
    transition: transform var(--transition-normal);
}

.tab-btn:hover,
.tab-btn.active {
    color: white;
    background: var(--glass-secondary);
}

.tab-btn.active::after {
    transform: scaleX(1);
}

.tab-content-container {
    flex: 1;
    background: var(--glass-primary);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 0 0 var(--radius-xl) var(--radius-xl);
    overflow: hidden;
}

.tab-content {
    display: none;
    height: 100%;
    overflow-y: auto;
    padding: var(--spacing-xl);
}

.tab-content.active {
    display: block;
}

/* Overview Tab */
.overview-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: var(--spacing-lg);
    height: 100%;
}

.summary-card,
.quick-actions-card {
    grid-row: span 1;
}

.activity-card {
    grid-column: span 2;
}

.card-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--glass-border);
    background: var(--glass-secondary);
}

.card-header h3 {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 1.1rem;
    font-weight: 600;
}

.card-content {
    padding: var(--spacing-lg);
}

.summary-card,
.quick-actions-card,
.activity-card {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md) 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-item:last-child {
    border-bottom: none;
}

.summary-label {
    color: rgba(255, 255, 255, 0.8);
}

.summary-value {
    font-weight: 600;
    color: var(--primary-color);
}

.action-buttons {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-md);
}

.action-button {
    background: var(--glass-primary);
    border: 1px solid var(--glass-border);
    color: white;
    padding: var(--spacing-lg);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-normal);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
    text-align: center;
}

.action-button:hover {
    background: var(--primary-color);
    border-color: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.action-button i {
    font-size: 1.5rem;
}

.action-button span {
    font-size: 0.875rem;
    font-weight: 500;
}

/* Activity Timeline */
.activity-timeline {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
}

.timeline-item {
    display: flex;
    align-items: flex-start;
    gap: var(--spacing-md);
}

.timeline-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    flex-shrink: 0;
}

.timeline-content p {
    margin-bottom: var(--spacing-xs);
}

.timeline-time {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
}

/* Calendar Styles */
.calendar-container {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--spacing-xl);
    height: 100%;
}

.calendar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-lg);
}

.calendar-nav {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-normal);
    display: flex;
    align-items: center;
    justify-content: center;
}

.calendar-nav:hover {
    background: var(--primary-color);
    border-color: var(--primary-color);
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 1px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.calendar-day-header {
    background: var(--glass-secondary);
    padding: var(--spacing-md);
    text-align: center;
    font-weight: 600;
    font-size: 0.875rem;
}

.calendar-day {
    background: var(--glass-primary);
    padding: var(--spacing-md);
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-normal);
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.calendar-day:hover {
    background: var(--glass-secondary);
}

.calendar-day.today {
    background: var(--primary-color);
    color: white;
    font-weight: 600;
}

.calendar-day.has-events::after {
    content: '';
    position: absolute;
    bottom: 4px;
    left: 50%;
    transform: translateX(-50%);
    width: 6px;
    height: 6px;
    background: var(--accent-color);
    border-radius: 50%;
}

.calendar-day.empty {
    background: transparent;
    cursor: default;
}

.calendar-events h4 {
    margin-bottom: var(--spacing-lg);
    color: var(--primary-color);
}

.event-item {
    display: flex;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: var(--glass-secondary);
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
    border: 1px solid var(--glass-border);
}

.event-time {
    font-weight: 600;
    color: var(--primary-color);
    min-width: 80px;
}

.event-details h5 {
    margin-bottom: var(--spacing-xs);
}

.event-details p {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
}

/* Tasks Styles */
.tasks-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
}

.add-task-btn,
.add-expense-btn,
.add-contact-btn,
.log-workout-btn {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-normal);
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-weight: 500;
}

.add-task-btn:hover,
.add-expense-btn:hover,
.add-contact-btn:hover,
.log-workout-btn:hover {
    background: var(--accent-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.task-filters {
    display: flex;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-lg);
}

.filter-btn {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    color: rgba(255, 255, 255, 0.7);
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-normal);
    font-size: 0.875rem;
}

.filter-btn:hover,
.filter-btn.active {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
}

.task-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    margin-bottom: var(--spacing-md);
    transition: all var(--transition-normal);
}

.task-item:hover {
    background: var(--glass-primary);
    transform: translateX(5px);
}

.task-checkbox {
    position: relative;
}

.task-checkbox input[type="checkbox"] {
    width: 20px;
    height: 20px;
    opacity: 0;
    cursor: pointer;
}

.task-checkbox label {
    position: absolute;
    top: 0;
    left: 0;
    width: 20px;
    height: 20px;
    border: 2px solid var(--glass-border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--transition-normal);
}

.task-checkbox input[type="checkbox"]:checked + label {
    background: var(--primary-color);
    border-color: var(--primary-color);
}

.task-checkbox input[type="checkbox"]:checked + label::after {
    content: '✓';
    position: absolute;
    top: 1px;
    left: 4px;
    color: white;
    font-size: 0.75rem;
    font-weight: bold;
}

.task-content {
    flex: 1;
}

.task-content h4 {
    margin-bottom: var(--spacing-xs);
}

.task-content p {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: var(--spacing-sm);
}

.task-meta {
    display: flex;
    gap: var(--spacing-md);
}

.task-priority {
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
}

.task-priority.high { background: rgba(255, 71, 87, 0.2); color: var(--error-color); }
.task-priority.medium { background: rgba(255, 170, 0, 0.2); color: var(--warning-color); }
.task-priority.low { background: rgba(0, 255, 136, 0.2); color: var(--success-color); }

.task-due {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
}

.task-actions {
    display: flex;
    gap: var(--spacing-sm);
}

.task-action-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: var(--radius-sm);
    transition: all var(--transition-normal);
}

.task-action-btn:hover {
    color: var(--primary-color);
    background: var(--glass-primary);
}

/* Expenses Styles */
.expenses-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
}

.expense-summary {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-lg);
}

.summary-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-lg);
}

.expense-stat {
    text-align: center;
}

.expense-stat h4 {
    margin-bottom: var(--spacing-sm);
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
}

.expense-stat .amount {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--primary-color);
}

.expense-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    margin-bottom: var(--spacing-md);
    transition: all var(--transition-normal);
}

.expense-item:hover {
    background: var(--glass-primary);
    transform: translateX(5px);
}

.expense-icon {
    width: 50px;
    height: 50px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    color: white;
}

.expense-details {
    flex: 1;
}

.expense-details h5 {
    margin-bottom: var(--spacing-xs);
}

.expense-details p {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: var(--spacing-sm);
}

.expense-category {
    font-size: 0.75rem;
    color: var(--primary-color);
    background: rgba(0, 212, 255, 0.1);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
}

.expense-amount {
    text-align: right;
}

.expense-amount .amount {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
}

.expense-amount .date {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
}

/* Health Styles */
.health-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
}

.health-dashboard {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}

.health-card {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-xl);
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    transition: all var(--transition-normal);
}

.health-card:hover {
    background: var(--glass-primary);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px var(--glass-shadow);
}

.health-icon {
    width: 60px;
    height: 60px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: white;
}

.health-info h4 {
    margin-bottom: var(--spacing-sm);
    color: rgba(255, 255, 255, 0.8);
}

.health-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--primary-color);
    margin-bottom: var(--spacing-xs);
}

.health-change {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.6);
}

.recent-workouts h4 {
    margin-bottom: var(--spacing-lg);
    color: var(--primary-color);
}

.workout-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg);
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    margin-bottom: var(--spacing-md);
    transition: all var(--transition-normal);
}

.workout-item:hover {
    background: var(--glass-primary);
    transform: translateX(5px);
}

.workout-type {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.workout-type i {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.workout-details {
    text-align: right;
}

.workout-date {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
    margin-top: var(--spacing-xs);
}

/* Contacts Styles */
.contacts-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
}

.contact-search {
    margin-bottom: var(--spacing-lg);
}

.search-input-wrapper {
    position: relative;
    max-width: 400px;
}

.search-input-wrapper i {
    position: absolute;
    left: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.5);
}

.search-input-wrapper input {
    width: 100%;
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    color: white;
    padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) 40px;
    border-radius: var(--radius-md);
    font-family: var(--font-primary);
    transition: all var(--transition-normal);
}

.search-input-wrapper input:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2);
}

.search-input-wrapper input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.contact-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    margin-bottom: var(--spacing-md);
    transition: all var(--transition-normal);
}

.contact-item:hover {
    background: var(--glass-primary);
    transform: translateX(5px);
}

.contact-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}

.contact-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.contact-info {
    flex: 1;
}

.contact-info h4 {
    margin-bottom: var(--spacing-xs);
}

.contact-info p {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: var(--spacing-xs);
}

.contact-email {
    font-size: 0.75rem;
    color: var(--primary-color);
}

.contact-actions {
    display: flex;
    gap: var(--spacing-sm);
}

.contact-action-btn {
    background: var(--glass-primary);
    border: 1px solid var(--glass-border);
    color: rgba(255, 255, 255, 0.6);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    transition: all var(--transition-normal);
    display: flex;
    align-items: center;
    justify-content: center;
}

.contact-action-btn:hover {
    color: var(--primary-color);
    border-color: var(--primary-color);
    background: var(--glass-secondary);
}

.assistant-status {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.status-dot.online {
    background: var(--success-color);
    box-shadow: 0 0 10px var(--success-color);
    animation: pulse 2s infinite;
}

/* Responsive Design */
@media (max-width: 768px) {
    .overview-grid {
        grid-template-columns: 1fr;
    }
    
    .activity-card {
        grid-column: span 1;
    }
    
    .calendar-container {
        grid-template-columns: 1fr;
    }
    
    .health-dashboard {
        grid-template-columns: 1fr;
    }
    
    .summary-stats {
        grid-template-columns: 1fr;
    }
    
    .action-buttons {
        grid-template-columns: 1fr;
    }
}
`;

// Add assistant styles to document
const assistantStyleSheet = document.createElement('style');
assistantStyleSheet.textContent = assistantStyles;
document.head.appendChild(assistantStyleSheet);