/**
 * Prompt Library JavaScript Implementation
 * Handles all frontend functionality for the System Prompts Library
 */

class PromptLibrary {
    constructor() {
        this.prompts = [];
        this.filteredPrompts = [];
        this.currentEditId = null;
        this.searchDebounceTimer = null;
        this.overviewSearchTimer = null;
        this.overviewVisible = true;
        
        console.log('🚀 PromptLibrary constructor called');
        this.init();
    }
    
    async init() {
        console.log('🔄 Initializing Prompt Library...');
        try {
            await this.loadPrompts();
            await this.loadStats();
            this.bindEvents();
            console.log('✅ Prompt Library initialized successfully');
        } catch (error) {
            console.error('❌ Error initializing Prompt Library:', error);
        }
    }
    
    bindEvents() {
        console.log('🔗 Binding events...');
        
        // Save prompt button
        const saveBtn = document.getElementById('savePromptBtn');
        if (saveBtn) {
            saveBtn.addEventListener('click', (e) => {
                console.log('💾 Save button clicked');
                e.preventDefault();
                this.savePrompt();
            });
            console.log('✅ Save button event bound');
        } else {
            console.error('❌ Save button not found');
        }
        
        // Import button
        const importBtn = document.getElementById('importBtn');
        if (importBtn) {
            importBtn.addEventListener('click', () => this.importPrompts());
            console.log('✅ Import button event bound');
        }
        
        // Search input with debounce
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                clearTimeout(this.searchDebounceTimer);
                this.searchDebounceTimer = setTimeout(() => this.filterPrompts(), 300);
            });
            console.log('✅ Search input event bound');
        }
        
        // Category filter
        const categoryFilter = document.getElementById('categoryFilter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', () => this.filterPrompts());
            console.log('✅ Category filter event bound');
        }
        
        // Clear filters
        const clearFilters = document.getElementById('clearFilters');
        if (clearFilters) {
            clearFilters.addEventListener('click', () => this.clearFilters());
            console.log('✅ Clear filters event bound');
        }
        
        // Modal events
        const addModal = document.getElementById('addPromptModal');
        if (addModal) {
            addModal.addEventListener('show.bs.modal', () => this.resetForm());
            console.log('✅ Modal events bound');
        }
        
        // Form submission on Enter key
        const form = document.getElementById('promptForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                console.log('📝 Form submitted');
                e.preventDefault();
                this.savePrompt();
            });
            console.log('✅ Form submit event bound');
        }
        
        // Overview search
        const overviewSearch = document.getElementById('overviewSearch');
        if (overviewSearch) {
            overviewSearch.addEventListener('input', (e) => {
                clearTimeout(this.overviewSearchTimer);
                this.overviewSearchTimer = setTimeout(() => this.filterOverview(), 200);
            });
            console.log('✅ Overview search event bound');
        }
        
        // Overview toggle
        const overviewToggle = document.getElementById('overviewToggle');
        if (overviewToggle) {
            overviewToggle.addEventListener('click', () => this.toggleOverview());
            console.log('✅ Overview toggle event bound');
        }
        
        console.log('✅ All events bound successfully');
    }
    
    async loadPrompts() {
        try {
            console.log('📊 Loading prompts...');
            this.showLoading('Loading prompts...');
            
            const response = await fetch('/api/prompts');
            const data = await response.json();
            
            console.log('📊 Prompts API response:', data);
            
            if (data.success) {
                this.prompts = data.prompts;
                this.filteredPrompts = [...this.prompts];
                this.renderPrompts();
                this.renderOverview();
                this.updateStats();
                console.log(`✅ Loaded ${this.prompts.length} prompts`);
            } else {
                console.error('❌ API error:', data.error);
                this.showToast('Error loading prompts: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('❌ Error loading prompts:', error);
            this.showToast('Error loading prompts: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async loadStats() {
        try {
            const response = await fetch('/api/prompts/stats');
            const data = await response.json();
            
            if (data.success) {
                const stats = data.stats;
                document.getElementById('totalUsage').textContent = stats.total_usage_last_30days || 0;
                document.getElementById('recentUsage').textContent = stats.total_usage_last_30days || 0;
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
    
    renderPrompts() {
        const container = document.getElementById('promptsContainer');
        
        if (this.filteredPrompts.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="prompt-empty-state">
                        <i class="bi bi-inbox"></i>
                        <h4>No prompts found</h4>
                        <p class="lab-text-muted">Try adjusting your search or filter criteria, or add a new prompt.</p>
                    </div>
                </div>
            `;
            return;
        }
        
        const promptsHtml = this.filteredPrompts.map(prompt => this.renderPromptCard(prompt)).join('');
        container.innerHTML = promptsHtml;
        
        // Bind events for the new cards
        this.bindCardEvents();
    }
    
    renderPromptCard(prompt) {
        const tags = prompt.tags ? prompt.tags.split(',').filter(tag => tag.trim()) : [];
        const tagsHtml = tags.map(tag => 
            `<span class="prompt-tag">${tag.trim()}</span>`
        ).join('');
        
        const description = prompt.description || 'No description available';
        const truncatedContent = prompt.content.length > 300 
            ? prompt.content.substring(0, 300) + '...' 
            : prompt.content;
            
        return `
            <div class="col-lg-6 col-12 mb-4">
                <div class="lab-card prompt-card h-100">
                    <div class="lab-card-header">
                        <div class="lab-card-header-title">
                            <strong>${this.escapeHtml(prompt.name)}</strong>
                            <div class="edit-actions">
                                <button class="lab-btn lab-btn-xs lab-btn-outline" onclick="promptLibrary.editPrompt(${prompt.id})">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="lab-btn lab-btn-xs lab-btn-outline" onclick="promptLibrary.deletePrompt(${prompt.id}, '${this.escapeHtml(prompt.name)}')">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="d-flex gap-2 flex-wrap mt-2">
                            <span class="prompt-tag prompt-category-tag">${prompt.category}</span>
                            <span class="prompt-tag prompt-usage-count">Used ${prompt.usage_count} times</span>
                            ${tagsHtml}
                        </div>
                    </div>
                    <div class="lab-card-body">
                        <p class="lab-text-secondary mb-3">${this.escapeHtml(description)}</p>
                        <div class="system-prompt-content">${this.escapeHtml(truncatedContent)}</div>
                        <div class="prompt-actions">
                            <button class="lab-btn lab-btn-sm lab-btn-outline" onclick="promptLibrary.copyPrompt(${prompt.id})">
                                <i class="bi bi-clipboard lab-btn-icon"></i> Copy
                            </button>
                            <button class="lab-btn lab-btn-sm lab-btn-outline" onclick="promptLibrary.testWithTokenObfuscation(${prompt.id})">
                                <i class="bi bi-shield-check lab-btn-icon"></i> Test Token
                            </button>
                            <button class="lab-btn lab-btn-sm lab-btn-outline" onclick="promptLibrary.testWithSystemSaturation(${prompt.id})">
                                <i class="bi bi-cpu lab-btn-icon"></i> Test Saturation
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    bindCardEvents() {
        // Card events are bound inline with onclick handlers for simplicity
        // This avoids issues with dynamically generated content
    }
    
    async savePrompt() {
        console.log('💾 savePrompt() called');
        
        const promptData = {
            name: document.getElementById('promptName')?.value?.trim() || '',
            content: document.getElementById('promptContent')?.value?.trim() || '',
            category: document.getElementById('promptCategory')?.value?.trim() || 'general',
            description: document.getElementById('promptDescription')?.value?.trim() || '',
            tags: document.getElementById('promptTags')?.value?.trim() || ''
        };
        
        console.log('💾 Form data:', promptData);
        
        // Validation
        if (!promptData.name || !promptData.content) {
            console.log('❌ Validation failed: missing name or content');
            this.showToast('Please fill in the name and content fields', 'error');
            return;
        }
        
        try {
            console.log('💾 Sending request...');
            this.showLoading('Saving prompt...');
            
            const isEdit = this.currentEditId !== null;
            const url = isEdit ? `/api/prompts/${this.currentEditId}` : '/api/prompts';
            const method = isEdit ? 'PUT' : 'POST';
            
            console.log(`💾 ${method} ${url}`);
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(promptData)
            });
            
            const data = await response.json();
            console.log('💾 API response:', data);
            
            if (data.success) {
                const action = isEdit ? 'updated' : 'created';
                this.showToast(`Prompt ${action} successfully!`, 'success');
                console.log(`✅ Prompt ${action} successfully`);
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addPromptModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Reload prompts
                await this.loadPrompts();
                await this.loadStats();
            } else {
                console.error('❌ API error:', data.error);
                this.showToast('Error saving prompt: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('❌ Error saving prompt:', error);
            this.showToast('Error saving prompt: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async editPrompt(id) {
        try {
            const response = await fetch(`/api/prompts/${id}`);
            const data = await response.json();
            
            if (data.success) {
                const prompt = data.prompt;
                
                // Fill form
                document.getElementById('promptId').value = prompt.id;
                document.getElementById('promptName').value = prompt.name;
                document.getElementById('promptContent').value = prompt.content;
                document.getElementById('promptCategory').value = prompt.category;
                document.getElementById('promptDescription').value = prompt.description || '';
                document.getElementById('promptTags').value = prompt.tags || '';
                
                this.currentEditId = id;
                
                // Update modal title
                document.getElementById('addPromptModalLabel').textContent = 'Edit System Prompt';
                
                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('addPromptModal'));
                modal.show();
            } else {
                this.showToast('Error loading prompt: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('Error loading prompt:', error);
            this.showToast('Error loading prompt: ' + error.message, 'error');
        }
    }
    
    deletePrompt(id, name) {
        this.currentEditId = id;
        document.getElementById('deletePromptName').textContent = name;
        
        // Show delete modal
        const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
        modal.show();
        
        // Bind confirm delete event
        document.getElementById('confirmDeleteBtn').onclick = () => this.confirmDelete();
    }
    
    async confirmDelete() {
        if (!this.currentEditId) return;
        
        try {
            this.showLoading('Deleting prompt...');
            
            const response = await fetch(`/api/prompts/${this.currentEditId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast('Prompt deleted successfully!', 'success');
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
                modal.hide();
                
                // Reload prompts
                await this.loadPrompts();
                await this.loadStats();
            } else {
                this.showToast('Error deleting prompt: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('Error deleting prompt:', error);
            this.showToast('Error deleting prompt: ' + error.message, 'error');
        } finally {
            this.hideLoading();
            this.currentEditId = null;
        }
    }
    
    async copyPrompt(id) {
        try {
            const prompt = this.prompts.find(p => p.id === id);
            if (!prompt) {
                this.showToast('Prompt not found', 'error');
                return;
            }
            
            await navigator.clipboard.writeText(prompt.content);
            this.showToast('Prompt copied to clipboard!', 'success');
            
            // Log usage
            await this.logUsage(id, 'copy');
        } catch (error) {
            console.error('Error copying prompt:', error);
            this.showToast('Error copying to clipboard', 'error');
        }
    }
    
    async testWithTokenObfuscation(id) {
        try {
            const prompt = this.prompts.find(p => p.id === id);
            if (!prompt) {
                this.showToast('Prompt not found', 'error');
                return;
            }
            
            // Log usage
            await this.logUsage(id, 'token_obfuscation');
            
            // Navigate to token obfuscation page with prompt
            sessionStorage.setItem('selectedPrompt', JSON.stringify(prompt));
            window.location.href = '/token-obfuscation?prompt=' + encodeURIComponent(prompt.name);
        } catch (error) {
            console.error('Error testing with token obfuscation:', error);
            this.showToast('Error opening token obfuscation test', 'error');
        }
    }
    
    async testWithSystemSaturation(id) {
        try {
            const prompt = this.prompts.find(p => p.id === id);
            if (!prompt) {
                this.showToast('Prompt not found', 'error');
                return;
            }
            
            // Log usage
            await this.logUsage(id, 'system_saturation');
            
            // Navigate to system saturation page with prompt
            sessionStorage.setItem('selectedPrompt', JSON.stringify(prompt));
            window.location.href = '/system-saturation?prompt=' + encodeURIComponent(prompt.name);
        } catch (error) {
            console.error('Error testing with system saturation:', error);
            this.showToast('Error opening system saturation test', 'error');
        }
    }
    
    async logUsage(promptId, tool) {
        try {
            await fetch(`/api/prompts/${promptId}/use`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tool: tool })
            });
        } catch (error) {
            console.error('Error logging usage:', error);
        }
    }
    
    async importPrompts() {
        const content = document.getElementById('importContent').value.trim();
        const sourceName = document.getElementById('importSourceName').value.trim() || 'Manual Import';
        const category = document.getElementById('importCategory').value.trim() || 'imported';
        
        if (!content) {
            this.showToast('Please enter content to import', 'error');
            return;
        }
        
        try {
            this.showLoading('Importing prompts...');
            
            const response = await fetch('/api/prompts/import', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: content,
                    source_name: sourceName,
                    category: category
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(`Successfully imported ${data.imported_count} prompts!`, 'success');
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('importModal'));
                modal.hide();
                
                // Clear form
                document.getElementById('importForm').reset();
                document.getElementById('importSourceName').value = 'Manual Import';
                document.getElementById('importCategory').value = 'imported';
                
                // Reload prompts
                await this.loadPrompts();
                await this.loadStats();
            } else {
                this.showToast('Error importing prompts: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('Error importing prompts:', error);
            this.showToast('Error importing prompts: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    filterPrompts() {
        const search = document.getElementById('searchInput').value.toLowerCase();
        const category = document.getElementById('categoryFilter').value;
        
        this.filteredPrompts = this.prompts.filter(prompt => {
            const matchesSearch = !search || 
                prompt.name.toLowerCase().includes(search) ||
                prompt.content.toLowerCase().includes(search) ||
                (prompt.tags && prompt.tags.toLowerCase().includes(search)) ||
                (prompt.description && prompt.description.toLowerCase().includes(search));
                
            const matchesCategory = !category || prompt.category === category;
            
            return matchesSearch && matchesCategory;
        });
        
        this.renderPrompts();
    }
    
    clearFilters() {
        document.getElementById('searchInput').value = '';
        document.getElementById('categoryFilter').value = '';
        this.filteredPrompts = [...this.prompts];
        this.renderPrompts();
    }
    
    resetForm() {
        console.log('🔄 Resetting form...');
        document.getElementById('promptForm').reset();
        document.getElementById('promptCategory').value = 'general';
        this.currentEditId = null;
        
        // Reset modal title
        document.getElementById('addPromptModalLabel').textContent = 'Add New System Prompt';
    }
    
    updateStats() {
        document.getElementById('totalPrompts').textContent = this.prompts.length;
        
        const categories = [...new Set(this.prompts.map(p => p.category))];
        document.getElementById('totalCategories').textContent = categories.length;
    }
    
    showLoading(text = 'Loading...') {
        const loadingOverlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        
        if (loadingText) loadingText.textContent = text;
        if (loadingOverlay) loadingOverlay.style.display = 'flex';
    }
    
    hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) loadingOverlay.style.display = 'none';
    }
    
    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            console.error('Toast container not found');
            console.log('Message:', message);
            return;
        }
        
        const toastId = 'toast-' + Date.now();
        
        const bgClass = type === 'success' ? 'bg-success' : 
                       type === 'error' ? 'bg-danger' : 'bg-primary';
        
        const toastHtml = `
            <div class="toast ${bgClass} text-white" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header ${bgClass} text-white border-0">
                    <strong class="me-auto">System Prompts</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${this.escapeHtml(message)}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
        toast.show();
        
        // Remove from DOM after hiding
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
    
    renderOverview() {
        const overviewList = document.getElementById('overviewList');
        const overviewCount = document.getElementById('overviewCount');
        
        if (!overviewList || !overviewCount) return;
        
        if (this.prompts.length === 0) {
            overviewList.innerHTML = `
                <div class="overview-empty">
                    <i class="bi bi-inbox"></i>
                    <div class="mt-2">No prompts available</div>
                </div>
            `;
            overviewCount.textContent = '0';
            return;
        }
        
        const overviewHtml = this.prompts.map(prompt => `
            <div class="overview-item" data-prompt-name="${this.escapeHtml(prompt.name).toLowerCase()}" 
                 onclick="promptLibrary.scrollToPrompt(${prompt.id})">
                <div class="overview-item-name">${this.escapeHtml(prompt.name)}</div>
                <div class="overview-item-category">${prompt.category}</div>
                <div class="overview-item-usage">${prompt.usage_count}</div>
            </div>
        `).join('');
        
        overviewList.innerHTML = overviewHtml;
        overviewCount.textContent = this.prompts.length;
    }
    
    filterOverview() {
        const searchTerm = document.getElementById('overviewSearch').value.toLowerCase();
        const overviewItems = document.querySelectorAll('.overview-item');
        let visibleCount = 0;
        
        overviewItems.forEach(item => {
            const promptName = item.getAttribute('data-prompt-name');
            const isVisible = !searchTerm || promptName.includes(searchTerm);
            
            item.style.display = isVisible ? 'flex' : 'none';
            if (isVisible) visibleCount++;
        });
        
        const overviewCount = document.getElementById('overviewCount');
        if (overviewCount) {
            overviewCount.textContent = visibleCount;
        }
        
        // Show empty state if no results
        const overviewList = document.getElementById('overviewList');
        if (visibleCount === 0 && searchTerm) {
            const existingEmpty = overviewList.querySelector('.overview-empty');
            if (!existingEmpty) {
                const emptyHtml = `
                    <div class="overview-empty">
                        <i class="bi bi-search"></i>
                        <div class="mt-2">No prompts match "${this.escapeHtml(searchTerm)}"</div>
                    </div>
                `;
                overviewList.insertAdjacentHTML('beforeend', emptyHtml);
            }
        } else {
            const existingEmpty = overviewList.querySelector('.overview-empty');
            if (existingEmpty) {
                existingEmpty.remove();
            }
        }
    }
    
    toggleOverview() {
        const overviewList = document.getElementById('overviewList');
        const overviewToggle = document.getElementById('overviewToggle');
        const toggleIcon = overviewToggle.querySelector('i');
        
        this.overviewVisible = !this.overviewVisible;
        
        if (this.overviewVisible) {
            overviewList.style.display = 'block';
            toggleIcon.className = 'bi bi-chevron-up';
            overviewToggle.title = 'Hide Overview';
        } else {
            overviewList.style.display = 'none';
            toggleIcon.className = 'bi bi-chevron-down';
            overviewToggle.title = 'Show Overview';
        }
    }
    
    scrollToPrompt(promptId) {
        // First scroll to the main prompt management section
        const promptSection = document.querySelector('.lab-card');
        if (promptSection) {
            promptSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        // Optional: highlight the specific prompt if visible
        setTimeout(() => {
            const promptCards = document.querySelectorAll('.prompt-card');
            promptCards.forEach(card => {
                const editBtn = card.querySelector('[onclick*="editPrompt(' + promptId + ')"]');
                if (editBtn) {
                    card.style.outline = '2px solid var(--lab-highlight)';
                    card.style.borderRadius = 'var(--lab-border-radius)';
                    setTimeout(() => {
                        card.style.outline = '';
                    }, 2000);
                }
            });
        }, 500);
    }
    
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the prompt library when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM loaded, creating PromptLibrary instance...');
    if (typeof window.promptLibrary === 'undefined') {
        window.promptLibrary = new PromptLibrary();
        console.log('✅ PromptLibrary instance created');
    } else {
        console.log('ℹ️ PromptLibrary instance already exists');
    }
});
